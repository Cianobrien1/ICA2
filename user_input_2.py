#!/usr/bin/python3
import os
import sys
import subprocess
path = "esearch_output"
os.system("rm -fr ~/ICA2/esearch_output")
os.system("mkdir -p ~/ICA2/esearch_output")
os.chdir(path)
def esearch_input () :
    protein_name_in= input('Enter protein name: ')
    taxonID= input('Enter taxon ID: ')
    protein_name_arg = protein_name_in.replace(" ", "_")
    esearch_cmd =  f"esearch -db protein -query '{protein_name_in}[PROTEIN]' 2>/dev/null | efilter -query txid'{taxonID}'[ORGANISM] 2>/dev/null | efetch -format fasta 2>/dev/null > ~/ICA2/esearch_output/{protein_name_arg}_{taxonID}.fasta"
    os.system(esearch_cmd)
    return 
esearch_input()
dir_content = os.listdir()
output_file_name = dir_content[0]
if os.stat(output_file_name).st_size == 0:
    os.system('rm -fr {output_file_name}')
    print('Function input invalid, please try again')
    esearch_input()
else:
    print("Fasta file has been saved in esearch_output directory as "+output_file_name)
