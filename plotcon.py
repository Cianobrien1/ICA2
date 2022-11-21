#!/usr/bin/python3
import os
path1 = os.environ['HOME']
os.system('rm -fr ~/ICA2/plotcon_output')
os.system('mkdir -p ~/ICA2/plotcon_output')
path2 = path1+'/ICA2/clustalo_output'
path3 = path1+'/ICA2/plotcon_output'
msf_file_list = os.listdir(path2)
msf_file_name = msf_file_list[0]
msf_file_name_only = msf_file_name.replace('.fasta.msf', '')
plotcon_arg1 = path2+'/'+msf_file_name
plotcon_arg2 = path3+'/'+msf_file_name_only
plotcon_input = f"plotcon -sequences {plotcon_arg1} -graph png -winsize 4 -goutfile {plotcon_arg2}"
os.system(plotcon_input) 
