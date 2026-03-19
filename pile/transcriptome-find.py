#!/usr/bin/env python3

import sys
from pile import Defaults, process_file_or_literal
from pile.fasta import read_fasta_as_dict


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("transcriptome")
    parser.add_argument("transcript")
    parser.add_argument("-p", "--protein", action="store_true", default=False, help="Look for a protein accession, by default look for accession in transcript file")
    parser.add_argument("-f", "--file", action="store_true", default=False)
    parser.add_argument("--exact", action="store_true", default=False)
    args = parser.parse_args()

    if args.protein:
        fasta_fn = Defaults.transcriptome_proteins_fasta(Defaults.workspace(), args.transcriptome)
    else:
        fasta_fn = Defaults.transcriptome_fasta(Defaults.workspace(), args.transcriptome)
    entries = read_fasta_as_dict(fasta_fn)

    accessions = []
    process_file_or_literal(not args.file, args.transcript, lambda v: accessions.append(v))

    for accession in accessions:
        if accession in entries:
            print(f">{accession}\n{entries[accession]}")
        elif args.exact:
            raise Exception(f"Cannot find sequence with accession {accession}")
        else:
            found = False
            for k,v in entries.items():
                if "_"+accession.lower()+"_" in k.lower():
                    print(f">{k}\n{v}")
                    found = True
            if not found:
                for k,v in entries.items():
                    if accession.lower() in k.lower() or k.lower() in accession.lower():
                        print(f">{k}\n{v}")
                        found = True
            if not found:
                raise Exception(f"Cannot find sequence with accession {accession}")
