"""Script to calculate the Entropy of translation options
based on phrases from a Moses phrase table (unzipped)."""

import argparse
import sys
import os
from os import listdir
from os.path import isfile, join
import math
from scipy.stats import entropy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
import codecs
import gzip


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Read probabilities from phrase table and compute entropy of translation solutions.')
    parser.add_argument('phraseTable',
                    help='Phrase table.')
    parser.add_argument('outputFile',
                    help='Output file. Phrases scored based on highest entropy')
    return parser


def read_table(phrase_table):
    """Reads phrase table and stores in a dictionary:
    source phrase: target phrase: combined (inverse+direct) probability"""
    phrases = dict()
    all_ps = dict()
    with open(phrase_table) as t:
        for line in t:
            line = line.strip().split('|||')
            en = line[0]
            de = line[1]
            probs = line[2].strip().split(' ')
            inverse_p = float(probs[0])
            direct_p = float(probs[2])
            combi_p = inverse_p+direct_p / 2
            # This is useful for tracking the ps to the target translation options
            #phrases[en] = {de: combi_p}
            # We calculate entropy based on this dict
            all_ps.setdefault(en, []).append(combi_p)
        return all_ps


def give_entropies(all_ps, output_file):
    """Given a dictionary of en phrases and all their ps,
    computes Entr of all solutions and writes to output file based on highest Entr"""
    entr_sorted = dict()
    with open(output_file, 'w') as w:
        for key, value in all_ps.iteritems():
            #options = len(all_ps[key])
            entr = calc_entropy(value)
            #print(entr)
            #entr = entr/options
            entr_sorted[key] = entr
        for key, value in reversed(sorted(entr_sorted.iteritems(), key=lambda (k, v): (v, k))):
            w.write(str(value) + '\t' + key + '\n')
        return w


def calc_entropy(value):
    """Calculates the entropy as -sum(prob*math.log(prob))"""
    entrop = entropy(value)
    return entrop


def plot_entropy(output_file, N):
    """Creates bar plot of words with highest entropy. N=n-first words"""
    fig, ax = plt.subplots()
    with codecs.open(output_file,'r','utf-8') as f:
        x=[]
        y=[]
        for i in range(N):
            line = f.next().rstrip().split('\t')
            x.append(line[1])
            y.append(line[0])
        index = np.arange(N)
    bar_width = 0.65
    opacity = 0.4
    ax.bar(index, y, bar_width,
           color='r', alpha=opacity)#g for DE, r for ES
    ax.set_xlabel('Phrases')
    ax.set_ylabel('Entropy')
    ax.set_title('Phrases with the highest entropy')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(x, rotation=90)
    ax.legend()

    fig.tight_layout()
    #plt.plot(*zip(*sorted(stats.items())))
    plt.show()



if __name__ == "__main__":
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])
    phrase_table=args.phraseTable
    output_file=args.outputFile
    give_entropies(read_table(phrase_table), output_file)
    plot_entropy(output_file, 150)