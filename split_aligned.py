#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import glob, os
import sys
import codecs
import re
import argparse
from os.path import  join


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Split the hunalign output into sentence-aligned corpus.')
    parser.add_argument('alignedDirectory',
                    help='Path to the directory containing the aligned files.')
    parser.add_argument('outputDirectory',
                    help='Path to the output directory.')
    parser.add_argument('base',
                        help='Basename for the corpus.')
    parser.add_argument('languagePair',
                        help='Language pair, e.g. en-es.')
    return parser


def split(aligned, target_path, base, lp):
    '''Splits the aligned files based on language, writes to one big file.'''
    sl, tl = lp.split('-')[0], lp.split('-')[1]
    source_file = join(target_path, base + sl)
    target_file = join(target_path, base + tl)
    print('Creating corpus ' + source_file, target_file)
    with codecs.open(source_file,'w','utf-8') as src, codecs.open(target_file,'w','utf-8') as trg:
        for file in sorted(glob.glob(join(aligned,"*.aligned"))):
            counter=0
            with codecs.open(file, 'r', 'utf-8') as f:
                for line in f:
                    if '~~~' in line:
                        line = re.sub('~~~', '', line)
                    line = line.split('\t')
                    if float(line[0])>-0.29:
                        #Unaligned sentences have score -0.3, we leave those out
                        counter += 1
                        src.write(line[1]+'\n')
                        trg.write(line[2])
            print('Done with ' + file +'. Number of lines: ' + str(counter))



if __name__ == "__main__":
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])
    aligned = args.alignedDirectory
    target_path = args.outputDirectory
    base = args.base
    lp = args.languagePair
    split(aligned, target_path, base, lp)

# Usage: python3 split_aligned.py /home/alina/Desktop/aligned/ /home/alina/Desktop/ epuds.en-de. en-de