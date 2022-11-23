#!/usr/bin/python3
import os
import re
import shutil
from pathlib import Path
import pandas as pd
#Importing necessary modules

esearch_path1 = os.environ['HOME']
Path(esearch_path1+'/ICA2').mkdir(parents = True, exist_ok=True)
os.chdir(esearch_path1+'/ICA2')
esearch_path2 = os.getcwd()
esearch_path3 = esearch_path2+'/esearch_output'
#Defining the paths to be used in the script
if os.path.exists(esearch_path3):
    shutil.rmtree(esearch_path3)
os.makedirs(esearch_path3)
#Removes the output directory if it exits, then creates the output directory and any parent directories necessary

def esearch_input () :
#Defines the esearch_input function.

    protein_name_in= input('Enter protein name: ')
    taxonID= input('Enter taxon ID: ')
#Takes user input for protein name, then taxon ID

    protein_name_arg = protein_name_in.replace(" ", "_")
#Replaces the spaces with underscore so I can use it to name the output file

    esearch_cmd1 =  f"esearch -db protein -query '{protein_name_in}[PROTEIN]' 2>~/ICA2/error.txt | efilter -query txid'{taxonID}'[ORGANISM] NOT PARTIAL 2>~/ICA2/error.txt | grep '<Count>' > ~/ICA2/esearch_temp.txt"
#First esearch command used to find the number of sequences. 2>~/ICA2/error.txt creates an error.txt file to pass the errors to if user enters an incorrect sequence

    esearch_cmd2 =  f"esearch -db protein -query '{protein_name_in}[PROTEIN]' 2>/dev/null | efilter -query txid'{taxonID}'[ORGANISM] NOT PARTIAL 2>/dev/null | efetch -format fasta 2>/dev/null > ~/ICA2/esearch_output/{protein_name_arg}_{taxonID}.fasta"
#esearch command that takes the input from the user as the arguements for the search. 2>/dev/null mutes error messages as to not spam the screen if incorrect input has been entered. efilter allows for the search to be narrowed to a single taxon. NOT PARTIAL removes partial sequences. Used f-string formatting to define the variable.

    os.system(esearch_cmd1)
#Calling the esearch_cmd variable defined above
    if os.stat(esearch_path1+'/ICA2/error.txt').st_size == 0:
        esearch_temp1 = open(esearch_path2+'/esearch_temp.txt')
        esearch_temp2 = esearch_temp1.read()
        esearch_temp3 = re.split(r"<|>", esearch_temp2)
        esearch_temp4 = int(esearch_temp3[2])
        os.remove(esearch_path2+'/error.txt')
#If the erorr.txt file has content (if the esearch command returned an error) then the sequence count is found and defined as the esearch_temp4 varaible. The intinsure it is an integer before being passed to the next if statment. Regex is used to split the <Count> line in the output file made by the esearch_cmd1 variable at '<' and '>'. The index of the number of sequences is known, which can then be defined to a varible to be used below.

        if esearch_temp4 > 1000:
            print('WARNING: Too many sequences detected, please narrow search paramters or try a different query.')
            os.remove(esearch_path2+'/esearch_temp.txt')
            return protein_name_arg, taxonID, protein_name_in
#If the number of sequences is greater than 1000, then it prints there were too many seqeunces and returns out of the function after deleting the temp file.

        elif esearch_temp4 < 3:
            print('WARNING: Only 1 seuqence detected, please try a different query.')
            os.remove(esearch_path2+'/esearch_temp.txt')
            return protein_name_arg, taxonID, protein_name_in
#If there were less than 3 sequence (Minimum for clusalto according to ebi website) then it prints a warning and returns the function after deleting the temp file.

        else:
            os.remove(esearch_path2+'/esearch_temp.txt')
            os.system(esearch_cmd2)
            return protein_name_arg, taxonID, protein_name_in
#If there at more than 3 but less than 1000 sequences, then esearch_cmd2 is ran which fetches the file and outputs it in fasta format after deleting the temp file.
    else:
        os.system(esearch_cmd2)
        os.remove(esearch_path2+'/error.txt')
        return protein_name_arg, taxonID, protein_name_in
#Ending the function

protein_name_arg, taxonID, protein_name_in = esearch_input()
#Calling the function

output_file_name = protein_name_arg+'_'+taxonID+'.fasta' 
#Assigning the output_file_name variable.

if os.stat(esearch_path3+"/"+output_file_name).st_size == 0:
    os.remove(esearch_path3+'/'+output_file_name)
    print('Function input invalid, please try again')
    esearch_input()
#If the esearch failed, the function will still create an output fasta file, but it will be empty. This checks if the output file is empty. If it is, it deletes the output file and tells the user the function input was invalid and asks to try again. It then calls the function again. 

else:
    print("Fasta file has been saved in esearch_output directory as "+output_file_name)
#If the file contains text, it tells the user the file has been saved in the esearch_output directory

## START OF FASTA -> DATAFRAME/CSV ##
fasta_path1 = os.environ['HOME']
os.chdir(fasta_path1+'/ICA2')
fasta_path2 = os.getcwd()
Path(fasta_path2+'/csv_file_dir').mkdir(parents=True, exist_ok=True)
shutil.rmtree(fasta_path2+'/csv_file_dir')
os.mkdir(fasta_path2+'/csv_file_dir')
fasta_path3 = fasta_path2+'/csv_file_dir'
#Since ~ wont work for homespace, I assign the path using os.environ['HOME'] + the name of the directroy I want to target to generalise the script

fasta_file = output_file_name
#Listing the directory gives the name of the file in list format

my_file = open(esearch_path3+'/'+fasta_file) 
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
Organism_count = df['Organism'].value_counts()
print(Organism_count)
number_of_organisms = len(df['Organism'].value_counts())

def user_input(question= 'There are '+str(number_of_organisms)+' organisms represented in the FASTA file, do you want to continue? [y/n]'):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        csv_arg = fasta_path3+'/'+fasta_file+'.csv'
        df.to_csv(csv_arg, sep='\t')
        #Outputs the dataframe to a csv file
        return False
    else:
        return user_input("Invalid response, please try again.")
user_input()



