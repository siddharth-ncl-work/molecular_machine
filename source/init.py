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
  config_file_path=f'{config.code_dir_path}/config.py'
  print(f"initializing from '{system_file_path}'") 
  if 'input_parent_dir_path' in kwargs.keys():
    input_parent_dir_path=kwargs['input_parent_dir_path']
  else:
    input_parent_dir_path=config.input_parent_dir_path
  if 'input_system_name' in kwargs.keys():
    input_system_name=kwargs['input_system_name']
  else:
    input_system_name=config.input_system_name
  if 'input_subsystem_name' in kwargs.keys():
    input_subsystem_name=kwargs['input_subsystem_name']
  else:
    input_subsystem_name=config.input_subsystem_name
  if 'input_scr_dir_name' in kwargs.keys():
    input_scr_dir_name=kwargs['input_scr_dir_name']
  else:
    input_scr_dir_name=config.input_scr_dir_name
  if 'ring_atom_no' in kwargs.keys():
    ring_atom_no=kwargs['ring_atom_no']
  else:
    ring_atom_no=config.ring_atom_no
  if 'track_atom_no' in kwargs.keys():
    track_atom_no=kwargs['track_atom_no']
  else:
    track_atom_no=config.track_atom_no
  if 'ref_axis_atom1_no' in kwargs.keys():
    ref_axis_atom1_no=kwargs['ref_axis_atom1_no']
  else:
    ref_axis_atom1_no=config.ref_axis_atom1_no
  if 'ref_axis_atom2_no' in kwargs.keys():
    ref_axis_atom2_no=kwargs['ref_axis_atom2_no']
  else:
    ref_axis_atom2_no=config.ref_axis_atom2_no
  if 'start_frame_no' in kwargs.keys():
    start_frame_no=kwargs['start_frame_no']
  else:
    start_frame_no=config.start_frame_no
  if 'end_frame_no' in kwargs.keys():
    end_frame_no=kwargs['end_frame_no']
  else:
    end_frame_no=config.end_frame_no
  if 'frame_no_pos' in kwargs.keys():
    frame_no_pos=int(kwargs['frame_no_pos'])
  else:
    frame_no_pos=int(config.frame_no_pos)
  if 'system_type' in kwargs.keys():
    system_type=kwargs['system_type']
  else:
    system_type=config.system_type

  data=None
  with open(config_file_path,'r') as file:
    data=file.readlines()
  for i,line in enumerate(data):
    if 'input_parent_dir_path' in line:
      pos=i
      break
  data[pos]=f'input_parent_dir_path="{input_parent_dir_path}"\n'
  for i,line in enumerate(data):
    if 'input_system_name' in line:
      pos=i
      break
  data[pos]=f'input_system_name="{input_system_name}"\n'
  for i,line in enumerate(data):
    if 'input_subsystem_name' in line:
      pos=i
      break
  data[pos]=f'input_subsystem_name="{input_subsystem_name}"\n'
  for i,line in enumerate(data):
    if 'input_scr_dir_name' in line:
      pos=i
      break
  data[pos]=f'input_scr_dir_name="{input_scr_dir_name}"\n'
  for i,line in enumerate(data):
    if 'ring_atom_no' in line:
      pos=i
      break
  data[pos]=f'ring_atom_no={ring_atom_no}\n'
  for i,line in enumerate(data):
    if 'track_atom_no' in line:
      pos=i
      break
  data[pos]=f'track_atom_no={track_atom_no}\n'
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
  for i,line in enumerate(data):
    if 'start_frame_no' in line:
      pos=i
      break
  data[pos]=f'start_frame_no={start_frame_no}\n'
  for i,line in enumerate(data):
    if 'end_frame_no' in line:
      pos=i
      break
  data[pos]=f'end_frame_no={end_frame_no}\n'
  for i,line in enumerate(data):
    if 'frame_no_pos' in line:
      pos=i
      break
  data[pos]=f'frame_no_pos={frame_no_pos}\n'
  for i,line in enumerate(data):
    if 'system_type' in line:
      pos=i
      break
  data[pos]=f'system_type="{system_type}"\n'
  with open(config_file_path,'w') as file:
    file.write(''.join(data))
  importlib.reload(config)

  ring_atom_no_list=extract_molecule.extractMolecule(system_file_path,atom_no=ring_atom_no)
  track_atom_no_list=extract_molecule.extractMolecule(system_file_path,atom_no=track_atom_no)
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
  with open(config_file_path,'w') as file:
    file.write(''.join(data))
  importlib.reload(config)
  


def initTask(read_from,row=None):
  if read_from=='config.py':
    print('config.py')
    input_file_path=os.path.join(config.input_parent_dir_path,config.input_system_name,config.input_subsystem_name,'scr','coors.xyz')
    initConfig(input_file_path)
  elif read_from=='system_info.csv':
    print('system_info.csv')
    input_file_path=os.path.join(row['input_parent_dir_path'],row['input_system_name'],row['input_subsystem_name'],row['input_scr_dir_name'],'coors.xyz')
    initConfig(input_file_path,input_parent_dir_path=row['input_parent_dir_path'],input_system_name=row['input_system_name'],input_subsystem_name=row['input_subsystem_name'],input_scr_dir_name=row['input_scr_dir_name'],ring_atom_no=row['ring_atom_no'],track_atom_no=row['track_atom_no'],ref_axis_atom1_no=row['ref_axis_atom1_no'],ref_axis_atom2_no=row['ref_axis_atom2_no'],start_frame_no=row['start_frame_no'],end_frame_no=row['end_frame_no'],frame_no_pos=row['frame_no_pos'],system_type=row['system_type'])
  output_dir_path=os.path.join(config.output_parent_dir_path,config.input_system_name,config.input_subsystem_name,config.input_scr_dir_name)
  if not os.path.isdir(output_dir_path):
    print(f'Directory does not exits\nCreating {output_dir_path}')
    subprocess.run(['mkdir',os.path.join(config.output_parent_dir_path,config.input_system_name)])
    subprocess.run(['mkdir',os.path.join(config.output_parent_dir_path,config.input_system_name,config.input_subsystem_name)])
    subprocess.run(['mkdir',os.path.join(config.output_parent_dir_path,config.input_system_name,config.input_subsystem_name,config.input_scr_dir_name)])
  else:
    print(f'{output_dir_path} already exits')
  config_file_path=f'{config.code_dir_path}/config.py'
  subprocess.run(['cp',config_file_path,output_dir_path])
  output_file_path=os.path.join(output_dir_path,'code_output.txt')
  with open(output_file_path,'a') as output_file:
    output_file.write('#'*80+'\n')
    output_file.write(str(datetime.today())+'\n')
    output_file.write('****config.py****\n')
    with open(config_file_path,'r') as config_file:
      data=config_file.readlines()
    output_file.write(''.join(data))
    output_file.write('-'*80+'\n')
    #output_file.write(f'step size = {config.step_size}\n')
  path_dict={'input_file_path':input_file_path,'output_dir_path':output_dir_path,'output_file_path':output_file_path}
  return path_dict


if __name__=='__main__':
  print(config.ref_axis_atom1_no)
  initConfig(config.test_file_path,ref_axis_atom1_no=-568)
  print(config.ref_axis_atom1_no)
  '''
  print(initTask())
  print(f'ring_atom_no_list={config.ring_atom_no_list}')
  print(f'track_atom_no_list={config.track_atom_no_list}')
  '''
