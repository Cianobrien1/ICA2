#!/usr/bin/python3
import os
import re
import shutil
from pathlib import Path
#Importing necessary modules

path1 = os.environ['HOME']
Path(path1+'/ICA2').mkdir(parents = True, exist_ok=True)
os.chdir(path1+'/ICA2')
path2 = os.getcwd()
path3 = path2+'/esearch_output'
#Defining the paths to be used in the script
if os.path.exists(path3):
    shutil.rmtree(path3)
os.makedirs(path3)
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
    if os.stat(path1+'/ICA2/error.txt').st_size == 0:
        esearch_temp1 = open(path2+'/esearch_temp.txt')
        esearch_temp2 = esearch_temp1.read()
        esearch_temp3 = re.split(r"<|>", esearch_temp2)
        esearch_temp4 = int(esearch_temp3[2])
        os.remove(path2+'/error.txt')
#If the erorr.txt file has content (if the esearch command returned an error) then the sequence count is found and defined as the esearch_temp4 varaible. The intinsure it is an integer before being passed to the next if statment. Regex is used to split the <Count> line in the output file made by the esearch_cmd1 variable at '<' and '>'. The index of the number of sequences is known, which can then be defined to a varible to be used below.

        if esearch_temp4 > 1000:
            print('WARNING: Too many sequences detected, please narrow search paramters or try a different query.')
            os.remove(path2+'/esearch_temp.txt')
            return protein_name_arg, taxonID, protein_name_in
#If the number of sequences is greater than 1000, then it prints there were too many seqeunces and returns out of the function after deleting the temp file.

        elif esearch_temp4 < 3:
            print('WARNING: Only 1 seuqence detected, please try a different query.')
            os.remove(path2+'/esearch_temp.txt')
            return protein_name_arg, taxonID, protein_name_in
#If there were less than 3 sequence (Minimum for clusalto according to ebi website) then it prints a warning and returns the function after deleting the temp file.

        else:
            os.remove(path2+'/esearch_temp.txt')
            os.system(esearch_cmd2)
            return protein_name_arg, taxonID, protein_name_in
#If there at more than 3 but less than 1000 sequences, then esearch_cmd2 is ran which fetches the file and outputs it in fasta format after deleting the temp file.
    else:
        os.system(esearch_cmd2)
        os.remove(path2+'/error.txt')
        return protein_name_arg, taxonID, protein_name_in
#Ending the function

protein_name_arg, taxonID, protein_name_in = esearch_input()
#Calling the function

output_file_name = protein_name_arg+'_'+taxonID+'.fasta' 
#Assigning the output_file_name variable.

if os.stat(path3+"/"+output_file_name).st_size == 0:
    os.remove(path3+'/'+output_file_name)
    print('Function input invalid, please try again')
    esearch_input()
#If the esearch failed, the function will still create an output fasta file, but it will be empty. This checks if the output file is empty. If it is, it deletes the output file and tells the user the function input was invalid and asks to try again. It then calls the function again. 

else:
    print("Fasta file has been saved in esearch_output directory as "+output_file_name)
#If the file contains text, it tells the user the file has been saved in the esearch_output directory


## OLD CODE ##
#with open(path2+"/"+output_file_name) as output_file_data:
#    output_file_content = output_file_data.read()
#    output_file_seq_count = output_file_content.count('>')
#    if output_file_seq_count < 2:
#        print('WARNING: Only 1 seuqence detected in fasta file')
#    if output_file_seq_count > 1000:
#        print('Sequence count has exceeded 1000, deleting extra sequences')
#        out_file_content2 = out_file_content.replace('>', '000', 1000)
#        out_file_content3 = out_file_content2.split('>', 1)
#        out_file_content4 = out_file_content3[0]
#        out_file_content5 = out_file_content4.replace('000', '>')
#        out_file_truncated = open(path2+"/"+output_file_name, 'w') 
#        out_file_truncated.write(out_file_content5)
#        out_file_truncated.close()
## OLD CODE ##
        


