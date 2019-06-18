#!/usr/bin/env python3
import sys
import yaml


def main(argv):
    for fp in argv[1:]:
        with open(fp) as f:
            hymn = yaml.safe_load(f)
        for s in hymn['stanzas']:
            if(s['flextext']):
                print(s['flextext'])
    return 0


if __name__ == "__main__": # pragma: no cover
    sys.exit(main(sys.argv))
