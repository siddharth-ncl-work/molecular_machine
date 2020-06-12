import os
import sys
sys.path.extend(['.','..'])

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics
from source import init
import make_test_systems

#matplotlib global parameters
plt.rc('figure',figsize=(16,9))
plt.rc('figure',dpi=72)
plt.rc('axes', titlesize=40)     
plt.rc('axes', labelsize=30) 
plt.rc('legend', fontsize=20)
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
plt.rc('axes', linewidth=2)
plt.rc('font', weight='bold')
plt.rc('xtick.major',size=10)
plt.rc('xtick.major',width=1.5)
plt.rc('ytick.major',size=10)
plt.rc('ytick.major',width=1.5)
plt.rc('xtick.minor',visible=False,bottom=False)
plt.rc('font', family='Liberation Serif')
plt.rc('axes',titlepad=20)
plt.rc('lines',markersize=8)


def task8(input_file_path,system='',system_name=''):
  global output_dir_path
  '''
  center of mass motion
  '''
  com_data={'frame_no':[],'com_x':[],'com_y':[],'com_z':[],'dcom_x':[],'dcom_y':[],'dcom_z':[]}
  with open(input_file_path,'r') as input_file:
    init_frame_cords=io.readFileMd(input_file,0,frame_no_pos=config.frame_no_pos)
    init_com=physics.getCom(init_frame_cords)
  with open(input_file_path,'r') as input_file:
    pbar=tqdm(range(0+config.step_size,total_frames,config.step_size))
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
      pbar.set_description(f"dcom = {[round(com_data['dcom_x'][-1],2),round(com_data['dcom_y'][-1],2),round(com_data['dcom_z'][-1],2)]} A")
  com_data_file_path=os.path.join(f'{output_dir_path}',f'com_data_{system_name}.csv')
  com_data_df=pd.DataFrame.from_dict(com_data)
  com_data_df.to_csv(com_data_file_path,index=False)
  print(com_data_df[['dcom_x','dcom_y','dcom_z']].values.min())
  ylim=(com_data_df[['dcom_x','dcom_y','dcom_z']].values.min()-1,com_data_df[['dcom_x','dcom_y','dcom_z']].values.max()+1)
  plot(com_data['frame_no'],com_data['dcom_x'],output_dir_path=output_dir_path,title='dcom_x',xlabel='Frame No',ylabel='delta_com',ylim=ylim,\
new_figure=True,save=False,label='x')
  plot(com_data['frame_no'],com_data['dcom_y'],output_dir_path=output_dir_path,title='dcom_y',xlabel='Frame No',ylabel='delta_com',ylim=ylim,\
new_figure=False,save=False,label='y')
  plot(com_data['frame_no'],com_data['dcom_z'],output_dir_path=output_dir_path,title=f'delta_com ({system_name})',xlabel='Frame No',\
ylabel=f'delta_com',ylim=ylim,new_figure=False,save=True,label='z')
  return 'DONE'

def plot(x,y,output_dir_path='',title='',xlabel='',ylabel='',ylim=None,new_figure=True,save=True,label=''):
  if new_figure:
    plt.figure(figsize=(16,8),dpi=72)
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y,label=label)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ylim(ylim)
  plt.legend()
  plt.grid()
  if save:
    plt.savefig(os.path.join(output_dir_path,'_'.join(title.split())+'.jpg'))
    plt.show()

#/home/vanka/ruchi/molecular_motor/case_1/ring/scr_finished/coors.xyz
#/home/vanka/ruchi/molecular_motor/case_1/ring_without_dielectric/scr_finish/coors.xyz

system_name='without_dielectric'

parent_output_dir_path=f'output/get_com_test_results'
try:
  os.mkdir(parent_output_dir_path)
except FileExistsError:
  print(f'Already exists: {parent_output_dir_path}')

output_dir_path=f'{parent_output_dir_path}/{system_name}'
try:
  os.mkdir(output_dir_path)
except FileExistsError:
  print(f'Already exists: {output_dir_path}')

input_file_path='/home/vanka/ruchi/molecular_motor/case_1/ring_without_dielectric/scr_finish/coors.xyz'
test_file_path=f'test_systems/only_ring_{system_name}_get_com_test_system.xyz'
total_frames=10000
distance=10 #Angs
make_test_systems.onlyRingGetComTestSystem(input_file_path=input_file_path,output_file_path=test_file_path,total_frames=total_frames,distance=distance)
task8(input_file_path=test_file_path,system_name=system_name)
