#!/usr/bin/python3
import os
import re
import shutil
from pathlib import Path
import pandas as pd
import sys
#Importing necessary modules

## START OF ESEARCH ##
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

    print('Searching protein database, please wait...')
#Tells user the search is sarting

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
            return esearch_input()
#If the number of sequences is greater than 1000, then it prints there were too many seqeunces and returns out of the function after deleting the temp file.

        elif esearch_temp4 < 3:
            print('WARNING: Too few seuqences detected, please try a different query.')
            os.remove(esearch_path2+'/esearch_temp.txt')
            return esearch_input()
#If there were less than 3 sequence (Minimum for clusalto according to ebi website) then it prints a warning and returns the function after deleting the temp file.

        else:
            os.remove(esearch_path2+'/esearch_temp.txt')
            os.system(esearch_cmd2)
            return protein_name_arg, taxonID
#If there at more than 3 but less than 1000 sequences, then esearch_cmd2 is ran which fetches the file and outputs it in fasta format after deleting the temp file.
    else:
        os.remove(esearch_path2+'/error.txt')
        print('Invalid search input, please try again.')
        return esearch_input()
#Ending the function

protein_name_arg, taxonID= esearch_input()
#Calling the function

output_file_name = protein_name_arg+'_'+taxonID+'.fasta' 
#Assigning the output_file_name variable.

#if os.path.exists(esearch_path2+'sequence_len_test'):
#    protein_name_arg, taxonID = esearch_input()
#    os.remove(esearch_path2+'sequence_len_test')
#    output_file_name = protein_name_arg+'_'+taxonID+'.fasta' 
#If the sequence_len_test file has been created then the file was either over 1000 or less than 3 sequences long. This re-calls the function then redefines the output_file_name variable so the user can input a different search query/

#if os.path.exists(esearch_path3+"/"+output_file_name):
#    if os.stat(esearch_path3+"/"+output_file_name).st_size == 0:
#        os.remove(esearch_path3+'/'+output_file_name)
#        print('Function input invalid, please try again')
#        protein_name_arg, taxonID = esearch_input()
#       output_file_name = protein_name_arg+'_'+taxonID+'.fasta' 

#If the esearch failed, the function will still create an output fasta file, but it will be empty. This checks if the output file is empty. If it is, it deletes the output file and tells the user the function input was invalid and asks to try again. It then calls the function again and redefines the output_file_name variable.

#    else:
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
#Prints the organism name column to the screen, due panda being nice it ranks them in order of frequency automatically. Then prints the number of organisms in the file.

def user_input(question= 'There are '+str(number_of_organisms)+' organisms represented in the FASTA file, do you want to continue to clustalo alignment?'):
    reply = str(input(question+' [y/n]: ')).lower().strip()
    if reply[0] == 'y':
        csv_arg = fasta_path3+'/'+fasta_file+'.csv'
        df.to_csv(csv_arg, sep='\t')
#Outputs dataframe to csv file.

        return True
    if reply[0] == 'n':
        return False
    else:
        return user_input("Invalid response, please try again.")
user_input()
#Asks user if they would like to continue to clustalo alignment based on the number of organsims represented in the fasta file.

## START OF CLUSTALO ##
print('Starting clustalo alignment...')
#Tells the user clustalo alignment is starting

clustalo_path1 = os.environ['HOME']
os.chdir(clustalo_path1+'/ICA2')
clustalo_path2 = os.getcwd()
clustalo_path3 = clustalo_path2+'/clusalto_output'
if os.path.exists(clustalo_path3) :
    shutil.rmtree(clustalo_path3)
os.mkdir(clustalo_path3)
fasta_file_name = fasta_file
fasta_file_name_only = fasta_file_name.replace('.fasta', '')
#Defining variables that will be used for clustalo command.

clustalo_arg1 = esearch_path3+'/'+fasta_file_name
clustalo_arg2 = clustalo_path3+'/'+fasta_file_name_only+'.msf'
#If I put these paths into the below clustalo_input variable without defining them as variables first it would not work. Defined these variables as a fix.

clustalo_input = f"clustalo -i {clustalo_arg1} -o {clustalo_arg2} --outfmt=msf --wrap=80 --force --threads=32"
os.system(clustalo_input)
#Defines the clustalo input as a variable and runs it with os.system. --outfmt=msf outputs in msf format for plotcon to work. --threads=32 is to speed it up by multithreading. --force overwrites the file if it already exists. --wrap=80 tells it to allow 80 residues before a line wrap in the output file.

print('clustalo alignment complete, saving msf file to clustalo_output directory...')
#Prints that clustalo alignment is complete and has been saved to the output directory.

def clustalo_input_question(question3= 'Do you want to continue to plotcon?'):
    reply = str(input(question3+' [y/n]: ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        print('Exiting script...')
        return False
    else:
        return clustalo_input_question("Invalid response, please try again.")
clustalo_input_question()
#Asks user if they would like to continue to plotcon analysis, if not then the script exists.

## START OF PLOTCON ##
print('Starting plotcon analysis...')
#Tells user that plotcon is starting.

plotcon_path1 = os.environ['HOME']
os.chdir(plotcon_path1+'/ICA2')
plotcon_path2 = plotcon_path1+'/ICA2/plotcon_output'
if os.path.exists(plotcon_path2):
    shutil.rmtree(plotcon_path2)
os.mkdir(plotcon_path2)
msf_file_name = fasta_file_name_only+'.msf'
msf_file_name_only = msf_file_name.replace('.fasta.msf', '')
#Defining the variables I will use in the plotcon command.

plotcon_arg1 = clustalo_arg2
plotcon_arg2 = plotcon_path2+'/'+msf_file_name_only
#Similarly to the clustalo command, plotcon would not work without me defining these paths as variables before being used in the plotcon_input variables. 

plotcon_input1 = f"plotcon -sequences {plotcon_arg1} -graph png -winsize 4 -goutfile {plotcon_arg2} >/dev/null"
#First plotcon input that is run. It saves the plot as a png in the plotcon_output directory.

plotcon_input2 = f"plotcon -sequences {plotcon_arg1} -graph x11 -winsize 4 -goutfile {plotcon_arg2} >/dev/null"
#Second plotcon input that is run. Instead of saving the plot, it runs it as a pop up on the screen if the display supports it.

os.system(plotcon_input1) 
print('PNG of plot saved to plotcon_output directory')
#Calling the first input command for plotcon and telling user where the file was saved.

def plotcon_input_question(question3= 'Do you want to view the plot now?'):
    reply = str(input(question3+' [y/n]: ')).lower().strip()
    if reply[0] == 'y':
        os.system(plotcon_input2)
        return True
    if reply[0] == 'n':
        print('To view plot, download the png file from the plotcon_output directory')
        return False
    else:
        return plotcon_input_question("Invalid response, please try again.")
plotcon_input_question()
#Asks the user if they would like the view the plotcon plot now. If the answer is "y", then the 2nd plotcon input is run and a pop up of the plot is displayed if supported.

## START OF PROSITE DATABASE SCAN ##
os.chdir(esearch_path1+'/ICA2')
prosite_path2 = os.getcwd()
prosite_path3 = prosite_path2+'/split_fasta_dir'
prosite_path4 = esearch_path3+'/'+output_file_name
if os.path.exists(prosite_path3):
    shutil.rmtree(prosite_path3)
os.mkdir(prosite_path3)
seqretsplit_cmd = f"seqretsplit -sequence {prosite_path4} -outseq *.fasta -osdirectory2 {prosite_path3}"
os.system(seqretsplit_cmd)


