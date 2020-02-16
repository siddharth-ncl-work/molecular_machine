import sys
import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

import config
from source import rotation,translation,energy,init


def task0():
  '''
  Rotational Directionality: Net Relative Rotation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_net_relative_rotation,rotation_data=rotation.getNetRotation(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.rotation_method)
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK0 COMPLETE\n')
    output_file.write(f'Ring Net Relative Rotaion = {ring_net_relative_rotation} degrees\n')
    output_file.write('-'*80+'\n\n')
  rotation_data_file_path=os.path.join(output_dir_path,'rotation_data.csv')
  pd.DataFrame.from_dict(rotation_data).to_csv(rotation_data_file_path,index=False)
  x=rotation_data['frame_no']
  y=rotation_data['rotation']
  title='Ring Net Relative Rotation'+f'({config.input_system_name,config.input_subsystem_name})'
  ylabel='rotation (degrees)'
  plot(x,y,output_dir_path=output_dir_path,title=title,ylabel=ylabel)
  print(f'Ring Net Relative Rotaion = {ring_net_relative_rotation} degrees')  
  return ring_net_relative_rotation

def task1():
  '''
  Efficiency = avg_RKE/(avg_RKE+avg_TKE)
  Average RKE: Average Rotational Kinetic Energy of the ring between two frames/time steps
  Average TKE: Average Translation Kinetic Energy of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_avg_rel_RKE,RKE_data=energy.getAvgRKE(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.RKE_method) 
  with open(input_file_path,'r') as input_file:
    ring_avg_rel_TKE,TKE_data=energy.getAvgTKE(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.TKE_method) 
  efficiency=ring_avg_rel_RKE*100/(ring_avg_rel_RKE+ring_avg_rel_TKE)
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK1 COMPLETE\n')
    output_file.write(f'Efficiency = {efficiency} %\n')
    output_file.write(f'Ring avg relative RKE = {ring_avg_rel_RKE} J\n')
    output_file.write(f'Ring avg relative TKE = {ring_avg_rel_TKE} J\n')
    output_file.write('-'*80+'\n\n')
  RKE_data_file_path=os.path.join(output_dir_path,'RKE_data.csv')
  TKE_data_file_path=os.path.join(output_dir_path,'TKE_data.csv')
  pd.DataFrame.from_dict(RKE_data).to_csv(RKE_data_file_path,index=False)
  pd.DataFrame.from_dict(TKE_data).to_csv(TKE_data_file_path,index=False)
  x=RKE_data['frame_no']
  y=RKE_data['RKE']
  title='Ring Average Relative RKE'+f'({config.input_system_name,config.input_subsystem_name})'
  ylabel='average RKE (J)'
  plot(x,y,output_dir_path=output_dir_path,title=title,ylabel=ylabel)
  x=TKE_data['frame_no']
  y=TKE_data['TKE']
  title='Ring Average Relative TKE'
  ylabel='average TKE (J)'
  plot(x,y,output_dir_path=output_dir_path,title=title,ylabel=ylabel)
  print(f'Efficiency = {efficiency} %')

def task2():
  '''
  Translational Directionality: Net Relative Translation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_net_relative_translation,translation_data=translation.getNetTranslation(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.translation_method)
  input_file.close()
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK2 COMPLETE\n')
    output_file.write(f'Ring Net Relative Translation = {ring_net_relative_translation} m\n')
    output_file.write('-'*80+'\n\n')
  translation_data_file_path=os.path.join(output_dir_path,'translation_data.csv')
  pd.DataFrame.from_dict(translation_data).to_csv(translation_data_file_path,index=False)
  x=translation_data['frame_no']
  y=translation_data['translation']
  title='Ring Net Relative Translation'+f'({config.input_system_name,config.input_subsystem_name})'
  ylabel='translation (m)'
  plot(x,y,output_dir_path=output_dir_path,title=title,ylabel=ylabel)
  print(f'Ring Net Relative Translation = {ring_net_relative_translation} m')
  return ring_net_relative_translation

def plot(x,y,output_dir_path='',title='',ylabel=''):
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y)
  plt.title(title)
  plt.xlabel('Frame number')
  plt.ylabel(ylabel)
  #plt.ylim(-360, 360)
  #plt.xlim(0,10)
  plt.savefig(output_dir_path+'/'+'_'.join(title.split())+'.png')
  if config.show_plot:
   plt.show()


tasks={'0':task0,'1':task1,'2':task2}
task_name={'0':'Ring Net Relative Rotation','1':'Ring Average Relative TKE','2':'Ring Net Relative Translation'}

read_from='system_info.csv'

if read_from=='config.py':
  path_dict=init.initTask(read_from)
  input_file_path=path_dict['input_file_path']
  output_file_path=path_dict['output_file_path']
  output_dir_path=path_dict['output_dir_path']
  print(f'ring_atom_no_list={config.ring_atom_no_list}')
  print(f'track_atom_no_list={config.track_atom_no_list}')
  for task_no in config.tasks.split('+'):
    print(f'Running Task{task_no}....')
    tasks[task_no]()
    print(f'Task{task_no} Complete.')
elif read_from=='system_info.csv':
  system_info_df=pd.read_csv('test_system_info.csv')
  print(system_info_df)
  summary_data={'System':[],'Sub-System':[],'scr':[]}
  for task_no in config.tasks.split('+'):
    summary_data[task_name[task_no]]=[]
  for i,row in system_info_df.iterrows():
    path_dict=init.initTask(read_from,row)
    input_file_path=path_dict['input_file_path']
    output_file_path=path_dict['output_file_path']
    output_dir_path=path_dict['output_dir_path']
    print(f'ring_atom_no_list={config.ring_atom_no_list}')
    print(f'track_atom_no_list={config.track_atom_no_list}')
    summary_data['System'].append(config.input_system_name)
    summary_data['Sub-System'].append(config.input_subsystem_name)
    summary_data['scr'].append(config.input_scr_dir_name)
    for task_no in config.tasks.split('+'):
      print(f'Running Task{task_no}....')
      value=tasks[task_no]()
      print(f'Task{task_no} Complete.')
      summary_data[task_name[task_no]].append(value)
  summary_data_df=pd.DataFrame.from_dict(summary_data)
  print(summary_data_df)
  summary_data_df.to_csv(config.output_parent_dir_path+'/summary_data.csv',index=False)
