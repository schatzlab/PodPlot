#!/usr/bin/env python
import bisect
import argparse
import time

import matplotlib.pyplot as plt


def log(message):
    """ Log messages to standard output. """
    print(time.ctime() + ' --- ' + message, flush=True)


if __name__ == "__main__":
    whale = """\n _V__       _V__       _V__       _V__\n(____\/{   (____\/{   (____\/{   (____\/{\n"""

    parser = argparse.ArgumentParser(description='Plot minimum read length vs. coverage or % sequence. Coverage is plotted when -g is specified. ')
    parser.add_argument("fai", metavar="<fai.fofn>", type=str, help="A list of fai files. First column is the fai file and second column is the label.")
    parser.add_argument("-g", metavar="<genome_size>", type=int, default=0, help="expected genome size (no prefix symbols).")
    #parser.add_argument("-y", action='store_true', default=False, help="Instead of covearage, y-axis is percentage of sequence.")

    args = parser.parse_args()
    fai_fofn = args.fai
    genome_size = args.g
    #y = args.y

    print(whale)

    # Get all of the fai files
    labels = dict()
    with open(fai_fofn, 'r') as f:
        for line in f:
            fai_file, label = line.rstrip().split("\t")
            labels[fai_file] = label

    # Compute coverages and plot
    MEDIUM_SIZE = 18
    BIGGER_SIZE = 100

    plt.figure(figsize=(7, 7))
    xvals = list(range(0, 105000, 5000))

    for fai in labels:
        log("Calculating coverage for " + fai)
        read_lens = []
        with open(fai, 'r') as f:
            for line in f:
                header, rlen, x, y, z = line.rstrip().split("\t")
                read_lens.append(int(rlen))

        sorted_lens = sorted(read_lens, reverse=True)
        seqsums = dict()
        for i in range(len(xvals)):
            seqsums[i] = 0

        for i in sorted_lens:
            idx = bisect.bisect_right(xvals, i)
            for j in range(idx):
                seqsums[j] += i

        covs = dict()
        percs = dict()

        if genome_size:
            for i in seqsums:
                covs[i] = seqsums[i] / genome_size
            # Plot for this iteration
            plt.scatter([xvals[i] for i in covs.keys()], covs.values(), s=100, alpha=0.5)
            plt.plot([xvals[i] for i in covs.keys()], covs.values(), label=labels[fai], linewidth=3, alpha=0.5)
        else:
            total_seq = sum(sorted_lens)
            for i in seqsums:
                percs[i] = (seqsums[i] / total_seq) * 100
            plt.scatter([xvals[i] for i in percs.keys()], percs.values(), s=100, alpha=0.5)
            plt.plot([xvals[i] for i in percs.keys()], percs.values(), label=labels[fai], linewidth=3, alpha=0.5)

    plt.legend(loc=1, prop={'size': 10})
    #plt.rc('axes', labelsize=BIGGER_SIZE)
    #plt.rc('xtick', labelsize=MEDIUM_SIZE)
    #plt.rc('ytick', labelsize=MEDIUM_SIZE)
    plt.xlabel("Min Read Length (bp)")
    if genome_size:
        plt.ylabel("Coverage (X)")
    else:
        plt.ylabel("Percentage of Total Sequence")
    plt.grid()
    plt.savefig("podplot")
    log("Goodbye!")
