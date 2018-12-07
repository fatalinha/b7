# -*- coding: utf-8 -*-

import argparse
import glob, os
import sys
from os.path import isfile, join
from lxml import etree
import xml.etree.ElementTree as ET
import codecs



def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Extract interventions from EP-UdS sentence aligned, translationese-filtered xml.')
    parser.add_argument('sourceDirectory',
                    help='Path to the source language directory.')
    parser.add_argument('targetDirectory',
                    help='Path to the target language directory.')
    parser.add_argument('interventionDirectory',
                        help='Path to the intervention directory (write).')
    return parser

# def create_dic(f):
# A function to create a dictionary # do not open file here
# Create dictionary (key=intervention id, value=list of strings)
# Get root
# for line in root finding interventions:
#    find id attribute
#    pass id as key
#    make list = []
#    for sent in intervention finding s:
#        append sent in list of values
# return dic

def create_dic(f):
    ids = {}
    tree = etree.parse(f)
    root = tree.getroot()
    for intervention in root.iter('intervention'):
        id = intervention.get('id')
        sentences=[]
        for sent in intervention.iter('s'):
            sentences.append(sent.text.lstrip())
        ids[id]=sentences
    for key, value in sorted(ids.items()): #can this be done earlier?
        if value==[]:#len(value)==0
            del ids[key]
    return ids


def read_files(source_path, target_path, interventions):
    trg_filenames = sorted(os.listdir(target_path))
    """count = 0
    for trg_filename in trg_filenames:
        filename = trg_filename.split('.')[0]
        try:
            os.path.isfile(source_path+filename+'.EN.xml')
        except:
            print('Source file '+filename+' is missing')
        count+=1
    print(str(count)+' files')
"""
    counter=0
    for trg_filename in trg_filenames:
        filename = trg_filename.split('.')[0]
        trg_file = join(target_path,filename+'.ES.xml')#to be changed based on the files/lang
        src_file = join(source_path,filename+'.EN.xml')
        #print(trg_file, src_file)
        with codecs.open(trg_file, 'r', 'utf-8') as trg, codecs.open(src_file, 'r', 'utf-8') as src:
            dict_trg = create_dic(trg)
            dict_src = create_dic(src)
            for key in dict_trg.keys():
                if key in dict_src.keys():
                    with codecs.open(interventions + filename + '.' + key + '.en',
                                     'w', 'utf-8') as src_w, codecs.open(
                            interventions + filename + '.' + key + '.es', 'w',
                            'utf-8') as trg_w: # Change language
                        for sent_src in dict_src[key]:
                            src_w.write(sent_src)  # write value-trg in trg output
                        for sent_trg in dict_trg[key]:
                            trg_w.write(sent_trg)  # write value-src in src output
                else:
                    counter+=1
                    print("Intervention " + key + " in file " + trg_file + " not in target!")
    print(counter)


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])
    source_path=args.sourceDirectory
    target_path=args.targetDirectory
    interventions = args.interventionDirectory
    read_files(source_path, target_path, interventions)

# Usage:  python3 extractinterventions.py /home/alina/pCloudDrive/UniSaarland/01_Projects/B7/02_data/europarl-uds/xml_translationese/en/originals_ns/ /home/alina/pCloudDrive/UniSaarland/01_Projects/B7/02_data/europarl-uds/xml_translationese/es/translations_from_en_n/ /home/alina/Desktop/interventions_es/