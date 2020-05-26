import sys
import os
import subprocess
import importlib
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics
from source import rotation,translation,energy,init


def task0():
  '''
  Rotational Directionality: Net Relative Rotation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_net_relative_rotation,rotation_data=rotation.getNetRotation(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.rotation_method,system_type=config.system_type)
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK0 COMPLETE\n')
    output_file.write(f'Ring Net Relative Rotaion = {ring_net_relative_rotation} degrees\n')
    output_file.write('-'*80+'\n\n')
  rotation_data_file_path=os.path.join(output_dir_path,'rotation_data.csv')
  pd.DataFrame.from_dict(rotation_data).to_csv(rotation_data_file_path,index=False)
  x=rotation_data['frame_no']
  y=rotation_data['rotation']
  title='Ring Relative Rotation'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Frame number'
  ylabel='Rotation (degrees)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  print(f'Ring Net Relative Rotaion = {ring_net_relative_rotation} degrees')  
  return ring_net_relative_rotation

def task1():
  '''
  Rotational Directionality: Net Relative Rotation of the ring between two frames/time steps
  Translational Directionality: Net Relative Translation of the ring between two frames/time steps  
  Efficiency = avg_RKE/(avg_RKE+avg_TKE)
  Average RKE: Average Relative Rotational Kinetic Energy of the ring between two frames/time steps
  Average TKE: Average Relative Translation Kinetic Energy of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_avg_rel_RKE,RKE_data=energy.getAvgRKE(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.RKE_method) 
  with open(input_file_path,'r') as input_file:
    ring_avg_rel_TKE,TKE_data=energy.getAvgTKE(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.TKE_method) 
  efficiency=ring_avg_rel_RKE*100/(ring_avg_rel_RKE+ring_avg_rel_TKE)
  ring_net_relative_rotation=RKE_data['ring_relative_rotation'].sum()
  ring_net_relative_translation=TKE_data['ring_relative_translation'].sum()
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK1 COMPLETE\n')
    output_file.write(f'Ring Net Relative Rotaion = {ring_net_relative_rotation} degrees')
    output_file.write(f'Ring Net Relative Translation = {ring_net_relative_translation} m\n')
    output_file.write(f'Ring avg relative RKE = {ring_avg_rel_RKE} J\n')
    output_file.write(f'Ring avg relative TKE = {ring_avg_rel_TKE} J\n')
    output_file.write(f'Efficiency = {efficiency} %\n')
    output_file.write('-'*80+'\n\n')
  RKE_data_file_path=os.path.join(output_dir_path,'RKE_data.csv')
  TKE_data_file_path=os.path.join(output_dir_path,'TKE_data.csv')
  pd.DataFrame.from_dict(RKE_data).to_csv(RKE_data_file_path,index=False)
  pd.DataFrame.from_dict(TKE_data).to_csv(TKE_data_file_path,index=False)
  x=RKE_data['frame_no']
  y=RKE_data['RKE']
  title='Ring Average Relative RKE'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Frame number'
  ylabel='average RKE (J)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  x=TKE_data['frame_no']
  y=TKE_data['TKE']
  title='Ring Average Relative TKE'
  xlabel='Frame number'
  ylabel='average TKE (J)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  x=RKE_data['frame_no']
  y=RKE_data['ring_relative_rotation']
  title='Ring Relative Rotation'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Frame number'
  ylabel='Rotation (degrees)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  x=TKE_data['frame_no']
  y=TKE_data['ring_relative_translation']
  title='Ring Relative Translation'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Frame number'
  ylabel='Translation (m)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  print(f'Efficiency = {efficiency} %')

def task2():
  '''
  Translational Directionality: Net Relative Translation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_net_relative_translation,translation_data=translation.getNetTranslation(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.translation_method)
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK2 COMPLETE\n')
    output_file.write(f'Ring Net Relative Translation = {ring_net_relative_translation} m\n')
    output_file.write('-'*80+'\n\n')
  translation_data_file_path=os.path.join(output_dir_path,'translation_data.csv')
  pd.DataFrame.from_dict(translation_data).to_csv(translation_data_file_path,index=False)
  x=translation_data['frame_no']
  y=translation_data['translation']
  title='Ring Relative Translation'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Frame number'
  ylabel='Translation (m)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  print(f'Ring Net Relative Translation = {ring_net_relative_translation} m')
  return ring_net_relative_translation

def task3():
  '''
  Rotational Directionality: Direct Relative Rotation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_relative_rotation=rotation.getRotation(input_file,config.start_frame_no,config.end_frame_no,part1='ring',part2='track',type='relative',method=config.rotation_method)
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK3 COMPLETE\n')
    output_file.write(f'Ring Relative Rotaion = {ring_relative_rotation} degrees\n')
    output_file.write('-'*80+'\n\n')
  print(f'Ring Relative Rotaion = {ring_relative_rotation} degrees')
  return ring_relative_rotation

def task4():
  '''
  Translational Directionality: Direct Relative Translation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_relative_translation=translation.getTranslation(input_file,config.start_frame_no,config.end_frame_no,part1='ring',part2='track',type='relative',method=config.translation_method)
  input_file.close()
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK4 COMPLETE\n')
    output_file.write(f'Ring Relative Translation = {ring_relative_translation} m\n')
    output_file.write('-'*80+'\n\n')
  print(f'Ring Relative Translation = {ring_relative_translation} m')
  return ring_relative_translation

def task5():
  '''
  Robustness Test wrt 'step_size' parameter: Ring Net Relative Rotation Vs step_size 
  '''
  data={'step_size':[],'Ring_Net_Relative_Rotation':[]}
  step_size_list=[1,2,5,8,10,15,20,30,40,50,100]
  end_frame_no=min(config.start_frame_no+100000,config.end_frame_no)
  for step_size in step_size_list:
    with open(f'{config.code_dir_path}/config.py','r') as file:
      data=file.readlines()
    for i,line in enumerate(data):
      if 'step_size' in line:
        pos=i
        break
    data[pos]=f'step_size={step_size}\n' 
    with open(f'{config.code_dir_path}/config.py','w') as file:
      file.write(''.join(data))
    importlib.reload(config)
    print(config.step_size)
    with open(input_file_path,'r') as input_file:
      ring_net_relative_rotation,_=rotation.getNetRotation(input_file,config.start_frame_no,end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.rotation_method)
    data['step_size'].append(step_size)
    data['Ring_Net_Relative_Rotation'].append(ring_net_relative_rotation)
  average_ring_net_relative_rotation=np.mean(data['Ring_Net_Relative_Rotation'])
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK5 COMPLETE\n')
    output_file.write(f'Start frame no={start_frame_no}')
    output_file.write(f'End frame no={end_frame_no}')
    output_file.write(f'Step size list={step_size_list}')
    output_file.write(f'<Ring Net Relative Rotation> = {average_ring_net_relative_rotation} degrees\n')
    output_file.write('-'*80+'\n\n')
  data_file_path=os.path.join(output_dir_path,'ring_net_relative_rotation_vs_step_size_data.csv')
  pd.DataFrame.from_dict(data).to_csv(data_file_path,index=False)
  x=data['step_size']
  y=data['Ring_Net_Relative_Rotation']
  title='Ring_Net_Relative_Rotation_vs_Step_size'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Step size'
  ylabel='Ring Net Relative Rotation (D)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  print(f'<Ring Net Relative Rotation> = {average_ring_net_relative_rotation} D')
  return average_ring_net_relative_rotation

def task6():
  '''
  Robustness Test wrt 'track_range' parameter: Ring Net Relative Rotation Vs track_range
  '''
  data={'track_range':[],'Ring_Net_Relative_Rotation':[]}
  track_range_list=[1,2,5,8,10,15,20,30,40,50,100]
  end_frame_no=min(config.start_frame_no+100000,config.end_frame_no)
  for track_range in track_range_list:
    with open(f'{config.code_dir_path}/config.py','r') as file:
      data=file.readlines()
    for i,line in enumerate(data):
      if 'track_range' in line:
        pos=i
        break
    data[pos]=f'track_range={track_range}\n'
    with open(f'{config.code_dir_path}/config.py','w') as file:
      file.write(''.join(data))
    importlib.reload(config)
    print(config.track_range)
    with open(input_file_path,'r') as input_file:
      ring_net_relative_rotation,_=rotation.getNetRotation(input_file,config.start_frame_no,end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='relative',method=config.rotation_method)
    data['track_range'].append(track_range)
    data['Ring_Net_Relative_Rotation'].append(ring_net_relative_rotation)
  average_ring_net_relative_rotation=np.mean(data['Ring_Net_Relative_Rotation'])
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK5 COMPLETE\n')
    output_file.write(f'Start frame no={start_frame_no}')
    output_file.write(f'End frame no={end_frame_no}')
    output_file.write(f'Track range list={track_range_list}')
    output_file.write(f'<Ring Net Relative Rotation> = {average_ring_net_relative_rotation} degrees\n')
    output_file.write('-'*80+'\n\n')
  data_file_path=os.path.join(output_dir_path,'ring_net_relative_rotation_vs_step_size_data.csv')
  pd.DataFrame.from_dict(data).to_csv(data_file_path,index=False)
  x=data['track_range']
  y=data['Ring_Net_Relative_Rotation']
  title='Ring_Net_Relative_Rotation_vs_Track_Range'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Track Range (A)'
  ylabel='Ring Net Relative Rotation (deg)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  print(f'<Ring Net Relative Rotation> = {average_ring_net_relative_rotation} deg')
  return average_ring_net_relative_rotation
 

def task7():
  '''
  Rotational Directionality: Net absolute  Rotation of the ring between two frames/time steps
  '''
  with open(input_file_path,'r') as input_file:
    ring_net_absolute_rotation,rotation_data=rotation.getNetRotation(input_file,config.start_frame_no,config.end_frame_no,step_size=config.step_size,part1='ring',part2='track',type='absolute',method=config.rotation_method,system_type=config.system_type)
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK0 COMPLETE\n')
    output_file.write(f'Ring Net Absolute Rotaion = {ring_net_absolute_rotation} degrees\n')
    output_file.write('-'*80+'\n\n')
  rotation_data_file_path=os.path.join(output_dir_path,'rotation_data.csv')
  pd.DataFrame.from_dict(rotation_data).to_csv(rotation_data_file_path,index=False)
  x=rotation_data['frame_no']
  y=rotation_data[f'net_absolute_rotation']
  title='Ring Net Absolute Rotation'+f'({config.input_system_name},{config.input_subsystem_name})'
  xlabel='Frame number'
  ylabel='Rotation (degrees)'
  plot(x,y,output_dir_path=output_dir_path,title=title,xlabel=xlabel,ylabel=ylabel)
  print(f'Ring Net Absolute Rotaion = {ring_net_absolute_rotation} degrees')
  return ring_net_absolute_rotation


def task8():
  '''
  center of mass motion
  '''
  com_data={'frame_no':[],'com_x':[],'com_y':[],'com_z':[],'dcom_x':[],'dcom_y':[],'dcom_z':[]}
  with open(input_file_path,'r') as input_file:
    init_frame_cords=io.readFileMd(input_file,config.start_frame_no,frame_no_pos=config.frame_no_pos)
    init_com=physics.getCom(init_frame_cords)
  with open(input_file_path,'r') as input_file:
    pbar=tqdm(range(config.start_frame_no+config.step_size,config.end_frame_no+1,config.step_size))
    for curr_frame_no in pbar:
      frame_cords=io.readFileMd(input_file,curr_frame_no,frame_no_pos=config.frame_no_pos)
      com=physics.getCom(frame_cords)
      com_data['frame_no'].append(curr_frame_no)
      com_data['com_x'].append(com[0])
      com_data['com_y'].append(com[1])
      com_data['com_z'].append(com[2])
      com_data['dcom_x'].append(com[0]-init_com[0])
      com_data['dcom_y'].append(com[1]-init_com[1])
      com_data['dcom_z'].append(com[2]-init_com[2])
  with open(output_file_path,'a') as output_file:
    output_file.write('TASK8 COMPLETE\n')
    output_file.write(f"Average dcom = [{np.mean(com_data['dcom_x'])},{np.mean(com_data['dcom_y'])},{np.mean(com_data['dcom_z'])}] \n")
    output_file.write('-'*80+'\n\n')
  com_data_file_path=os.path.join(output_dir_path,'com_data.csv')
  pd.DataFrame.from_dict(com_data).to_csv(com_data_file_path,index=False)

  ylim=(-5,5)
  plot(com_data['frame_no'],com_data['dcom_x'],output_dir_path=output_dir_path,title='dcom_x',xlabel='Frame No',ylabel='com',ylim=ylim)
  plot(com_data['frame_no'],com_data['dcom_y'],output_dir_path=output_dir_path,title='dcom_y',xlabel='Frame No',ylabel='com',ylim=ylim)
  plot(com_data['frame_no'],com_data['dcom_z'],output_dir_path=output_dir_path,title='dcom_z',xlabel='Frame No',ylabel='com',ylim=ylim)
  return 'DONE'

def plot(x,y,output_dir_path='',title='',xlabel='',ylabel='',ylim=None):
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  if ylim is not None:
    ymax=max(max(ylim),max(y))
    ymin=min(min(ylim),min(y))
    plt.ylim(ymin,ymax)
  #plt.xlim(0,10)
  plt.grid()
  plt.savefig(os.path.join(output_dir_path,'_'.join(title.split())+'.jpg'))
  if config.show_plot:
    plt.show()


tasks={'0':task0,'1':task1,'2':task2,'3':task3,'4':task4,'5':task5,'6':task6,'7':task7,'8':task8}
task_name={'0':'Ring_Net_Relative_Rotation',
	   '1':'Ring_Average_Relative_KE',
           '2':'Ring_Net_Relative_Translation',
           '3':'Ring_Relative_Rotation',
           '4':'Ring_Relative_Translation',
           '5':'Ring_Net_Relative_Rotation_vs_Step_size',
           '6':'Ring_Net_Relative_Rotation_vs_Track_Range',
           '7':'Ring_Net_Absolute_Rotation',
           '8':'com_motion'}

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
  system_info_df=pd.read_csv('system_info.csv')
  print(system_info_df)
  summary_data={'System':[],'Sub_System':[],'scr':[],'Start_Frame_No':[],'End_Frame_No':[]}
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
    summary_data['Sub_System'].append(config.input_subsystem_name)
    summary_data['scr'].append(config.input_scr_dir_name)
    summary_data['Start_Frame_No'].append(config.start_frame_no)
    summary_data['End_Frame_No'].append(config.end_frame_no)
    for task_no in config.tasks.split('+'):
      print(f'Running Task{task_no}....')
      value=tasks[task_no]()
      print(f'Task{task_no} Complete.')
      summary_data[task_name[task_no]].append(value)
  summary_data_df=pd.DataFrame.from_dict(summary_data)
  print(summary_data_df)
  with open(config.output_parent_dir_path+'/summary_data.csv','a') as summary_file:
    summary_file.write(str(datetime.today())+'\n\n')
    summary_data_df.to_csv(summary_file,mode='a') 
    summary_file.write('#'*80+'\n')
