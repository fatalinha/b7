from polyglot.text import Text
import os
from os import listdir
from os.path import isfile, join


path = '/home/alina/pCloudDrive/UniSaarland/01_Projects/B7/02_data/bilm/dede/'

for file_s in listdir(path):
    path2f = join(path, file_s)
    file_s_id = os.path.basename(file_s)
    file_pos = file_s_id+'.pos'
    with open(path2f, 'r') as word, open(file_pos, 'w') as pos:
        print('Tagging file '+file_pos)
        for line in word:
            text = Text(line.rstrip(), hint_language_code='en')
            pos_text = text.pos_tags
            words, tags = zip(*pos_text)
            pos.write(' '.join(tag for tag in tags)+'\n')
            #tags = text.words[0].pos_tag

