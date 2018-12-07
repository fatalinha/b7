# Entropy script reading lexical probabilities from lexical table.

import math
from scipy.stats import entropy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
import codecs
import argparse
import sys
import os


# TODO: add translation options in trg

def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Read probabilities from lex files and compute entropy of translation solutions.')
    parser.add_argument('lex_e2f',
                    help='Lexical table e2f.')
    parser.add_argument('lex_f2e',
                        help='Lexical table f2e.')
    parser.add_argument('outputFile',
                    help='Output file. Phrases scored based on highest entropy.')
    return parser


def read_file(e2f, f2e, ofile):
    with open(e2f, 'r') as e2f, open(f2e, 'r') as f2e, open(ofile,'w')as w:
        ps = dict()
        for line in e2f:
            line = line.rstrip().split(' ')
            e = line[0] #0 for e2f, 1 for f2e
            f = line[1]
            pe2f = line[2]
            for line2 in f2e:
                line2 = line2.rstrip().split(' ')
                if line2[0]==f and line2[1]==e:
                    pf2e = line[2]
            newp = (float(pe2f) + float(pf2e)) / 2
            ps.setdefault(e, []).append(newp)

        entr_sorted = dict()
        for key, value in ps.iteritems():
            entr = calc_entropy(value)
            entr_sorted[key] = entr
        for key, value in reversed(sorted(entr_sorted.iteritems(), key=lambda (k, v): (v, k))):
            w.write(str(value) + ' ' + key + '\n')
        return w


def plot_entropy(ofile, N):
    # Creates bar plot of words with highest entropy. N=n-first words
    fig, ax = plt.subplots()
    with codecs.open(ofile,'r','utf-8') as f:
        x = []
        y = []
        for i in range(N):
            line = f.next().rstrip().split(' ')
            x.append(line[1])
            y.append(line[0])
        index = np.arange(N)
    bar_width = 0.65
    opacity = 0.4
    ax.bar(index, y, bar_width,
           color='g', alpha=opacity) #g for DE, r for ES
    ax.set_xlabel('Words')
    ax.set_ylabel('Entropy')
    ax.set_title('Words with the highest entropy')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(x, rotation=45)
    ax.legend()

    fig.tight_layout()
    #plt.plot(*zip(*sorted(stats.items())))
    plt.show()


def calc_entropy(value):
    # -sum(prob*math.log(prob))
    entrop = entropy(value)
    return entrop

if __name__ == "__main__":
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])
    e2f = args.lex_e2f
    f2e = args.lex_f2e
    output_file = args.outputFile
    read_file(e2f, f2e, output_file)
    plot_entropy(output_file, 100)
