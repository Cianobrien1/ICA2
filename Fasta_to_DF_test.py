#!/usr/bin/python3
import pandas as pd
import re
import os
import sys
path1 = os.getcwd()
path2 = path1+"/esearch_output"
os.chdir(path2)
file_name = os.listdir()
fasta_file = file_name[0]
my_file = open(fasta_file) 
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
        line3 = line2[1:]
        line4 = ' '.join(line3)
        name.append(line4)
        organism.append(edit.group(1)) 
    else:
        seq.append(eachline)
	
s_name = pd.Series(name)
s_id = pd.Series(id)
s_organism = pd.Series(organism)
s_seq = pd.Series(seq)

df = pd.DataFrame({'ID' : s_id, 'Name' : s_name, 'Organism' : s_organism, 'Sequence' : s_seq})
df.to_csv('dataframetest', sep='\t')

