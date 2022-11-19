#!/usr/bin/python3
import pandas as pd
import os 
import sys
import subprocess
import re
my_file = open('4890_PDH.fasta')
id = []
name = []
organism = []
seq = []
for eachline in my_file:
    if eachline.startswith('>'):
        line = eachline.split()
        id.append(line[0])
        edit = re.search('(\[.+\])', eachline)
        line1 = eachline.replace(edit.group(1), '')
        line2 = line1.split()
        name.append(line2[1:])
        edit1 = re.search('(>.+\[)', eachline)
        line3 = eachline.replace(edit1.group(1), '')
        line4 = line3.replace(']', '')
        organism.append(line4)
    else:
        seq.append(eachline)
	
s_name = pd.Series(name)
s_id = pd.Series(id)
s_organism = pd.Series(organism)
s_seq = pd.Series(seq)

df = pd.DataFrame({'ID' : s_id, 'Name' : s_name, 'Organism' : s_organism, 'Sequence' : s_seq})
df.to_csv('dataframetest', sep='\t')

