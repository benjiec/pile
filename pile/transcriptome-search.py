#!/usr/bin/env python3

import os
import subprocess
from pile import Defaults, process_file_or_literal
from pile.fasta import read_fasta_as_dict


def bowtie2_search_sequence(fn, queries):

    query_text = []
    for i,s in enumerate(queries):
        query_text.append(f">query_{i}\n{s}\n")
    query_text = "".join(query_text)

    cmd = f"bowtie2 --local -x {fn} -f -U - | samtools view -F 4 | cut -f3 | sort -u"

    result = subprocess.run(
        cmd,
        input=query_text,
        shell=True,
        capture_output=True,
        text=True
    )

    hit_ids = result.stdout.splitlines()
    return hit_ids


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("transcriptome")
    parser.add_argument("sequence_file")
    parser.add_argument("--no-fasta", action="store_true", default=False)
    args = parser.parse_args()

    tx_fn = Defaults.transcriptome_fasta(Defaults.workspace(), args.transcriptome)
    if not os.path.exists(tx_fn+".1.bt2"):
        raise Exception("Cannot find bowtie index")

    query_sequences = []
    if args.no_fasta:
        process_file_or_literal(False, args.sequence_file, lambda s: query_sequences.append(s))
    else:
        queries = read_fasta_as_dict(args.sequence_file)
        query_sequences.extend(queries.values())

    hit_ids = bowtie2_search_sequence(tx_fn, query_sequences)
    for hit in hit_ids:
        print(hit)
