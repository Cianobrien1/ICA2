#!/usr/bin/python3
import pandas as pd
import re
import os
#Importing the moduels I will need for the script

path1 = os.environ['HOME']
path2 = path1+"/ICA2/esearch_output"
#Since ~ wont work for homespace, I assign the path using os.environ['HOME'] + the name of the directroy I want to target to generalise the script

file_name = os.listdir(path2)
#Listing the directory gives the name of the file in list format

fasta_file = file_name[0]
#fasta_file is being assigned as the first namein the list above, which is just the file name in string format

my_file = open(path2+"/"+fasta_file) 
#opening the fasta file for the script to work on

id = []
name = []
organism = []
seq = []
#Defining the lists I will be using in the for loop below


for eachline in my_file:
    if eachline.startswith('>'):
#This checks if the line starts which ">" indicating it is the title of the fasta sequence
        line = eachline.split()
        id.append(line[0])
#Splits the line into a list, then since the accession number is the first item in the list, I add it directly to the ID list defined earlier
        edit = re.search('(\[.+\])', eachline)
        line1 = eachline.replace(edit.group(1), '')
        line2 = line1.split()
        line3 = line2[1:]
        line4 = ' '.join(line3) 
        name.append(line4)
#Since the protein name can vary in terms of number of words, and so can the organism name, this is requried to generliase the script. It finds the organism name with regex. It then removes the organism name from the line, so that the only remaining are the ID and the protein name. Since protein name will always be 2nd place in the list, I can append from 2nd place until the end of the list to the name list defined earlier without adding the organsim name too. the join line simply make it look nicer in the title of the columns in the dataframe and csv made below
        organism.append(edit.group(1)) 
#Regex found the organism name above, this appends the name to the predefined list
    else:
        seq.append(eachline)
#If the line does not start with ">" then it is a sequence, so it simply appends the sequence to the sequence list
	
s_name = pd.Series(name)
s_id = pd.Series(id)
s_organism = pd.Series(organism)
s_seq = pd.Series(seq)
#Converts the lists to series

df = pd.DataFrame({'ID' : s_id, 'Name' : s_name, 'Organism' : s_organism, 'Sequence' : s_seq})
#Creates a dataframe with the series

df.to_csv(path2+"/"+fasta_file+'.csv', sep='\t')
#Outputs the dataframe to a csv file

