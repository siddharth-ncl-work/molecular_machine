import time
import os
import sys
import importlib
import subprocess
from datetime import datetime
sys.path.extend(['.','..'])

from source import extract_molecule
import config


def initConfig(system_file_path,**kwargs):
  print(f"initializing from '{system_file_path}'") 
  if len(kwargs)==0:
    ring_atom_no=config.ring_atom_no
    track_atom_no=config.track_atom_no
    ref_axis_atom1_no=config.ref_axis_atom1_no
    ref_axis_atom2_no=config.ref_axis_atom2_no 
  else:
    ring_atom_no=kwargs['ring_atom_no']
    track_atom_no=kwargs['track_atom_no'] 
    ref_axis_atom1_no=kwargs['ref_axis_atom1_no']
    ref_axis_atom2_no=kwargs['ref_axis_atom2_no']
  ring_atom_no_list=extract_molecule.extractMolecule(system_file_path,atom_no=ring_atom_no)
  track_atom_no_list=extract_molecule.extractMolecule(system_file_path,atom_no=track_atom_no)
  config_file_path=f'{config.code_dir_path}/config.py'
  data=None
  with open(config_file_path,'r') as file:
    data=file.readlines()
  for i,line in enumerate(data):
    if 'ring_atom_no_list' in line:
      pos=i
      break
  data[pos]=f'ring_atom_no_list={ring_atom_no_list}\n'
  for i,line in enumerate(data):
    if 'track_atom_no_list' in line:
      pos=i
      break
  data[pos]=f'track_atom_no_list={track_atom_no_list}\n'
  for i,line in enumerate(data):
    if 'ref_axis_atom1_no' in line:
      pos=i
      break
  data[pos]=f'ref_axis_atom1_no={ref_axis_atom1_no}\n'
  for i,line in enumerate(data):
    if 'ref_axis_atom2_no' in line:
      pos=i
      break
  data[pos]=f'ref_axis_atom2_no={ref_axis_atom2_no}\n'
  with open(config_file_path,'w') as file:
    file.write(''.join(data))
  importlib.reload(config)

def initTask():
  input_file_path=os.path.join(config.input_parent_dir_path,config.input_system_name,config.input_subsystem_name,config.input_file_name)
  initConfig(input_file_path)
  output_dir_path=os.path.join(config.output_parent_dir_path,config.input_system_name,config.input_subsystem_name,config.input_file_name.split('.')[0])
  if not os.path.isdir(output_dir_path):
    print(f'Directory does not exits\nCreating {output_dir_path}')
    subprocess.run(['mkdir',os.path.join(config.output_parent_dir_path,config.input_system_name)])
    subprocess.run(['mkdir',os.path.join(config.output_parent_dir_path,config.input_system_name,config.input_subsystem_name)])
    subprocess.run(['mkdir',os.path.join(config.output_parent_dir_path,config.input_system_name,config.input_subsystem_name,config.input_file_name.split('.')[0])])
  else:
    print(f'{output_dir_path} already exits')
  config_file_path=f'{config.code_dir_path}/config.py'
  subprocess.run(['cp',config_file_path,output_dir_path])
  output_file_path=os.path.join(output_dir_path,'code_output.txt')
  with open(output_file_path,'a') as output_file:
    output_file.write('#'*80+'\n')
    output_file.write(str(datetime.today())+'\n')
    output_file.write('config.py\n')
    with open(config_file_path,'r') as config_file:
      data=config_file.readlines()
    output_file.write(''.join(data))
    output_file.write('-'*80+'\n')
    output_file.write(f'step size = {config.step_size}\n')
  path_dict={'input_file_path':input_file_path,'output_dir_path':output_dir_path,'output_file_path':output_file_path}
  return path_dict


if __name__=='__main__':
  #initConfig(config.test_file_path)
  print(initTask())
  print(f'ring_atom_no_list={config.ring_atom_no_list}')
  print(f'track_atom_no_list={config.track_atom_no_list}')

