#!/usr/bin/env python3
import sys
import yaml

def main(argv):
    fp = argv[1]
    with open(fp) as f:
        hymn = yaml.safe_load(f)
    for s in hymn['stanzas']:
        if(s['flextext']):
            print(s['flextext'])

if __name__ == "__main__":
    sys.exit(main(sys.argv))
