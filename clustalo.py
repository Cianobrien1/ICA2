#!/usr/bin/python3
import os
path1 = os.environ['HOME']
path2 = path1+"/ICA2/esearch_output"
path3 = path1+"/ICA2/clustalo_output"
os.system('rm -fr ~/ICA2/clustalo_output')
os.system('mkdir -p ~/ICA2/clustalo_output')
fasta_file_list = os.listdir(path2)
fasta_file_name = fasta_file_list[0]
clustalo_arg1 = path2+'/'+fasta_file_name
clustalo_arg2 = path3+'/'+fasta_file_name+'.msf'
clustalo_input = f"clustalo -i {clustalo_arg1} -o {clustalo_arg2} --outfmt=msf --wrap=80 --force --threads=6"
os.system(clustalo_input)
