#!/usr/bin/env python3

from pile import run_command, Defaults
from pile.bowtie_index import bowtie2_index


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("transcriptome")
    parser.add_argument("--unclustered", action="store_true", default=False)
    args = parser.parse_args()

    if args.unclustered:
        fn = Defaults.transcriptome_fasta(Defaults.workspace(), args.transcriptome)
    else:
        fn = Defaults.transcriptome_cluster_fasta(Defaults.workspace(), args.transcriptome)

    bowtie2_index(fn)
