#!/usr/bin/env python3
import fileinput
import json
import os.path
import pyphen
import re
import sys
import unicodedata
import yaml

from nltk.corpus import cmudict
from nltk.tokenize import SyllableTokenizer

from hyphenator import wordSyl


def main(argv):
    """ Script to convert plain text into flextext.
    argv[1] is the meter, like 8.6.8.6.
    argv[2] is the file to use as a template, or '-' for no file.
    argv[3] is the dictionary of hyphenations.
    argv[4] is the two-letter language code, or '-' for undetermined.
    additional arguments are used as input if they are present
    the flextext is sent to stdout
    stderr is a YAML document including warnings and alternate verses
    """
    if(len(argv) < 2):
        error("Usage %s" % main.__doc__)
        return
    # Make meter an inverted list of the syllable counts so "1.2.3.4" =>
    # ['4','3','2','1'].
    meter = argv[1].split('.')[::-1]
    templateFile = argv[2] if len(argv) > 2 else '-'
    lang = argv[4] if len(argv) > 4 else 'en'
    mst = MultiSylT(argv[3] if len(argv) > 3 else '-', lang=lang)
    success = True
    i = 0
    for line in fileinput.input(argv[5:]):
        i += 1
        try:
            length = int(meter.pop())
        except BaseException:
            error("Out of lines in meter.")
            return
        line = line.replace("\n", "")
        syllabized = syllabizeLine(line, length, mst, lang=lang)
        if(syllabized):
            print(syllabized[0])
            if(len(syllabized) > 1):
                message('alternates', i)
                messageData('data', syllabized)
        else:
            success = False
            print('')
            error("Unable to syllabize '%s' to %d syllables" % (line, length))
    return 0 if success else 1


def syllabizeLine(line, n, mst, lang=None):
    if lang and lang != mst.lang:
        mst.changeLang(lang)
    if lang in ['zh', 'ja', 'ko'] and not romanized(line):
        # multiTokenize is not needed: CJK is usually 1 syllable per character.
        sentence = ""
        prevPunc = True
        for character in line:
            # P = Punctuation, S = Symbol, Z = Separator
            if unicodedata.category(character)[0] in 'PSZ':
                if unicodedata.category(character)[0] != 'Z':
                    sentence += character
                prevPunc = True
            elif prevPunc:
                sentence += " " + character
                prevPunc = False
            else:
                sentence += " -- " + character
                prevPunc = False
        return [sentence.strip(' -')]
    else:
        sentences = []
        ts = []
        words = [x for x in line.split(' ') if x != '']
        for word in words:
            if(word.strip(wordSyl.puncs) == ''):
                warning("Word '%s' consists only of punctuation" % word)
            else:
                ts.append(mst.multiTokenize(word))
        recurse('', ts, n, sentences, lang)
        return sentences


def recurse(string, ts, n, sentences, lang):
    if len(ts) == 0:
        if n == 0:
            sentences.append(string.strip(' '))
        return
    for tokenization in ts[0]:
        if(len(tokenization) <= n):
            newstring = string + ' -- '.join(tokenization) + ' '
            recurse(newstring, ts[1:], n - len(tokenization), sentences, lang)
        elif lang in ['es']:
            # This tokenization doesn't fit, or there are more words left,
            # So we need to smash some syllables together.
            vowels = r"aeiouáéíóúüy"
            # In Spanish, the H has no sound.
            ignores = "h"
            newstring = string + ' -- '.join(tokenization) + ' '
            oldstring = newstring
            newN = n
            # Smash syllables until there's enough room for this word.
            while newN < len(tokenization):
                newstring = re.sub(
                    r"([" + vowels + "][" + ignores + "]?)"
                    + " "
                    + "([" + ignores + "]?[" + vowels + r"])",
                    r"\1~\2",
                    oldstring,
                    count=1,
                    flags=re.IGNORECASE)
                if newstring.count('~') != (oldstring.count('~') + 1):
                    # No syllable could be smashed, so we give up.
                    return
                oldstring = newstring
                newN = newN + 1
            recurse(newstring, ts[1:], newN
                    - len(tokenization), sentences, lang)


def romanized(line):
    """Return true if this uses latin characters."""
    return bool(re.match(r"[a-zA-Z]", line))


def message(key, msg):
    """Write a message as a yaml object item of an array."""
    sys.stderr.write("- " + key + ": " + json.dumps(msg) + "\n")


def messageData(key, data):
    """Write additional attributes into the last message object."""
    sys.stderr.write("  " + key + ": " + json.dumps(data) + "\n")


def error(msg):
    message('error', msg)


def warning(msg):
    message('warning', msg)


class MultiSylT(object):
    def __init__(self, dictName, lang=None):
        # Sonority Sequencing Tokenizer defaults to 26 latin letters,
        # english pronunciation.
        self.SSP = SyllableTokenizer()
        self.changeLang(lang)
        self.dict = {"words": []}
        if (dictName == '-'):
            dictName = os.path.dirname(__file__) + "/dict.yaml"
        try:
            with open(dictName) as f:
                self.dict = yaml.safe_load(f)
        except BaseException:
            error("%s could not be loaded." % dictName)
        # CMU Pronunciation dictionary includes 119K+ english words plus some
        # proper nouns using the latin alphabet, occasionally with punctuation.
        self.d = cmudict.dict()

    def changeLang(self, lang):
        if lang not in pyphen.LANGUAGES:
            lang = 'en'
        self.pyphen = pyphen.Pyphen(lang=lang)
        self.lang = lang

    def multiTokenize(self, originalWord):
        """ Return options for tokenizing a word. """
        word = self.deformat(originalWord)
        tokenizations = []
        # If the word exists in our dictionary, include those tokenizations.
        if(word in self.dict['words']):
            tokenizations += self.dict['words'][word]

        # Otherwise, use an algorithm to get word split up into syllables
        tokenized = self.SSP.tokenize(word)
        splitter = "\t"
        hyphenated = self.pyphen.inserted(word, splitter).split(splitter)

        if self.lang == 'en':
            tokenizations = self._addMatchingSylCount(
                word, tokenizations, tokenized, hyphenated)
        elif self.lang == 'es':
            # Sonority Sequencing doesn't work well with strong and weak vowels
            esTokenized = self._spanishTokenize(word)
            if esTokenized not in tokenizations:
                tokenizations.append(esTokenized)
            # Hunspell tokenizations are not as accurate as our tokenized ones:
            # only include them if the syllable count matches.
            if hyphenated not in tokenizations and len(
                    hyphenated) == len(esTokenized):
                tokenizations.append(hyphenated)
        else:
            if tokenized not in tokenizations:
                tokenizations.append(tokenized)
            if hyphenated not in tokenizations:
                tokenizations.append(hyphenated)
        return list(map(self.reformat, tokenizations, [
                    originalWord for x in range(0, len(tokenizations))]))

    def _addMatchingSylCount(self, word, tokenizations, tokenized, hyphenated):
        sylCounts = self.nsyl(word)
        # If the tokenized or hyphenated version has the same number of
        # syllables as one of the CMU STT pronunciations, but we don't
        # already have that syllable-count represented, include it.
        lh = len(hyphenated)
        if(lh in sylCounts and lh not in map(len, tokenizations)):
            tokenizations.append(hyphenated)
        lt = len(tokenized)
        if(lt in sylCounts and lt not in map(len, tokenizations)):
            tokenizations.append(tokenized)
        if(1 in sylCounts and [word] not in tokenizations):
            tokenizations.append([word])

        # Fallback if there are no tokenizations.
        if(len(tokenizations) == 0):
            warning("%s has %d syllables," % (str(hyphenated), len(hyphenated))
                    + ' expected: '
                    + (" or ".join(map(str, sylCounts)) or "???")
                    )
            tokenizations.append(hyphenated)
        return tokenizations

    def _spanishTokenize(self, word):
        """ Make sure spanish hyphenated syllable counts are correct
        https://www.spanishdict.com/guide/spanish-syllables-and-syllabification-rules
        """
        # Accented vowels always get their own syllable.
        accentedVowels = "áéíóú"
        # Two strong vowels together are split into different syllables.
        strongVowels = "aeo"
        # Weak vowels can blend with each other, or with strong vowels.
        weakVowels = "iuü"
        vowels = accentedVowels + strongVowels + weakVowels

        # Split certain vowel pairs, and let SSP do the rest.
        newWord = ""
        prevLetter = " "
        for letter in word:
            if (letter in vowels and prevLetter in accentedVowels) or \
               (letter in accentedVowels and prevLetter in vowels) or \
               (letter in strongVowels and prevLetter in strongVowels):
                newWord += "-" + letter
            else:
                newWord += letter
            prevLetter = letter
        # TODO: Fix tokenization for double-r and double-l
        tokenized = self.SSP.tokenize(newWord)
        return list(filter(lambda syl: syl != '-', tokenized))

    def deformat(self, word):
        return re.sub(
            "[" + wordSyl.smartSingles + "]",
            "'",
            word.lower().strip(
                wordSyl.puncs))

    def reformat(self, oldTokenized, template):
        # Since tokenized is mutable, create a duplicate of it.
        tokenized = list(oldTokenized)

        # Match the case
        plainTemp = template.strip(wordSyl.puncs)
        if(plainTemp and plainTemp.isupper()):
            tokenized[0] = tokenized[0].upper()
        elif(plainTemp and plainTemp[0].isupper()):
            tokenized[0] = tokenized[0][0].upper() + tokenized[0][1:]

        # Prepend/append the punctuations
        match = re.search(r"^[" + wordSyl.puncs + r"]+", template)
        starting = match.group(0) if match else ''
        match = re.search(r"[" + wordSyl.puncs + r"]+$", template)
        ending = match.group(0) if match else ''
        tokenized[0] = starting + tokenized[0]
        tokenized[-1] = tokenized[-1] + ending

        # Replace smart single-quotes
        dumbPlaceholder = "\n"
        splitter = "\t"
        templateNoDumb = template.replace("'", dumbPlaceholder)
        for letter in templateNoDumb:
            if letter in wordSyl.smartSingles + dumbPlaceholder:
                tokenized = splitter.join(tokenized).replace(
                    "'", letter, 1).split(splitter)
        tokenized = splitter.join(tokenized).replace(
            dumbPlaceholder, "'").split(splitter)

        return tokenized

    def nsyl(self, word):
        """Get the number of syllables a word should be
        from the CMU Pronunciation dictionary.
        Returned as a list to account for variants."""
        if word in self.d:
            return [len(list(y for y in x if y[-1].isdigit()))
                    for x in self.d[word.lower()]]
        return []


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
