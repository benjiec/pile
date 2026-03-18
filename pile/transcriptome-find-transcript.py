#!/usr/bin/env python3

import sys
from pile import Defaults
from pile.fasta import read_fasta_as_dict


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("transcriptome")
    parser.add_argument("transcript")
    parser.add_argument("--exact", action="store_true", default=False)
    args = parser.parse_args()

    fasta_fn = Defaults.transcriptome_fasta(Defaults.workspace(), args.transcriptome)
    entries = read_fasta_as_dict(fasta_fn)

    if args.transcript in entries:
        print(entries[args.transcript])
    elif args.exact:
        raise Exception("Cannot find sequence")
    else:
        for k,v in entries.items():
            if "_"+args.transcript.lower()+"_" in k.lower():
                print(v)
                sys.exit(0)
        for k,v in entries.items():
            if args.transcript.lower() in k.lower():
                print(v)
                sys.exit(0)
        raise Exception("Cannot find sequence")
