#!/usr/bin/python3
import os
import sys
import subprocess
#def esearch_input (protein_name_in = input('Enter protein name: '), taxonID = input('Enter taxon ID: ')) :
   # protein_name_arg = protein_name_in.replace(" ", "_")
   #esearch_cmd =  f"esearch -db protein -query '{protein_name_in}' | efilter -query txid'{taxonID}'[ORGANISM] | efetch -format fasta > {protein_name_arg}_{taxonID}.fasta"
   # os.system(esearch_cmd)
   # output = print(protein_name_arg+"_"+taxonID+".fasta saved")
   # return output 
#esearch_input()
protein_name_in= input('Enter protein name: ')
taxonID = input('Enter taxon ID: ')
protein_name_arg = protein_name_in.replace(" ","_")
esearch_cmd =  f"esearch -db protein -query '{protein_name_in}[PROTEIN]' | efilter -query txid'{taxonID}'[ORGANISM] | efetch -format fasta > {protein_name_arg}_{taxonID}.fasta"
subprocess.call(esearch_cmd, shell=True)
print(protein_name_arg+"_"+taxonID+".fasta saved")

