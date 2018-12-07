"""Extract the actual text from EP-UdS tmx files to single txt files (e.g. for KLDs)"""

import argparse
import sys
import os
from os import listdir
from os.path import isfile, join
from lxml import etree
import xml.etree.ElementTree as ET
import codecs


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Extract sentence-split raw text from EPIC.')
    parser.add_argument('inputDirectory',
                    help='Path to the input directory.')
    parser.add_argument('outputDirectory',
                    help='Path to the output directory.')
    return parser


def read_files(i_dir, o_dir):
    """Reads one by one the files in the dir and writes to
    same-named sentence-per-line files in out_dir (for parallel)."""
    for f in listdir(i_dir):

        path2file=join(i_dir, f)
        out_path2file=join(o_dir,f)
        if isfile(join(i_dir, f)):
            print('from file '+f)
            with codecs.open(path2file, 'r', 'utf-8') as i, codecs.open(out_path2file,'w', 'utf-8') as out:
                tree = etree.parse(i)
                root = tree.getroot()
                for sent in root.iter('s'):
                    # for sentence-aligned: 's', if paragraphs change to 'p'
                    sent = sent.text.strip()
                    out.write(sent + '\n')


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])
    source_path=args.inputDirectory
    target_path=args.outputDirectory
    read_files(source_path, target_path)
    #extract_lm(source_path, target_path)
