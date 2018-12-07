try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass
import re
from os.path import isfile, join

def get_logps(orig, mix):
    """Find sentences for which the mixed LM does (much) better
    pp is actually logbase10 probability"""
    counter = 0
    mlines=list()
    with open(orig, 'r') as o, open(mix, 'r') as m:
        for lo, lm in zip(o,m):
            counter +=1
            ppo = lo.split(':')[1].split(' ')[1]
            ppm = lm.split(':')[1].split(' ')[1]
            print('Line ' + str(counter) + ':' + ppo, ppm)
            if ppm>ppo and abs(float(ppm))-abs(float(ppo))>abs(4):
                mlines.append(counter)#, lo, lm))
            if counter==141901:#spanish141901:de 167040
                break
        print(len(mlines))
        return mlines


def get_sents(mlines, file_s):
    """Find the above sentences in source and target"""
    with open(file_s, 'r') as s:
        for i, line in enumerate(s, 1):
            #print(i, line.rstrip())
            if i in mlines:
                print(line.rstrip())

outputs = '/home/alina/pCloudDrive/UniSaarland/01_Projects/B7/02_data/bilm/output_pos'
orig = join(outputs, 'epuds.orig.transall.es.pos.pp')
mix = join(outputs, 'epuds.mix1.transall.pos.es.pp')#epuds.orig1.transall.pos.en.pp')
#mix = 'eno-eso.pp'orig.4.pp
mlines = get_logps(orig, mix)
get_sents(mlines, '/home/alina/pCloudDrive/UniSaarland/01_Projects/B7/02_data/bilm/DNU/epuds.en-es.es') #de/epuds.en-de.de.train')