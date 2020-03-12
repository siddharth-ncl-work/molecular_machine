import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics,atomic_mass
from source import rotation,shift_origin,energy


def get_dist_pt_line():
  pt_cords=[3,4,0]
  #3 Angs
  print(vector.get_dist_pt_line(pt_cords,[0,1,0]))
  #5 Angs
  print(vector.get_dist_pt_line(pt_cords,[0,0,1]))
  pt_cords=[1,0,0]
  #0.8165 Angs
  print(vector.get_dist_pt_line(pt_cords,[1,1,1]))

def getMI(rot_axis='x'):
  #Single Atom
  atom_cords=[3,4,0]
  atom_type='c'
  #1.8036E-45 kg.m2
  print(physics.getMI(atom_cords,atom_type,[0,1,0]))
  #5.01E-45 kg.m2
  print(physics.getMI(atom_cords,atom_type,[0,0,1]))
  #1.336E-46 kg.m2 
  atom_cords=[1,0,0]
  print(physics.getMI(atom_cords,atom_type,[1,1,1]))  

  #Whole system
  if rot_axis=='x':
    axis=[1,0,0]
  elif rot_axis=='y':
    axis=[0,1,0]
  elif rot_axis=='z':
    axis=[0,0,1]
  frame1_no=0
  frame2_no=1
  file=open('test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz','r')
  frame1_initial_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_initial_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  frame1_final_cords_df,frame2_final_cords_df=shift_origin.shiftOrigin(frame1_initial_cords_df,frame2_initial_cords_df,process='rotation')
  #frame1
  #ring = 1.46E-43 kg.m2
  #track = 1.65-45 kg.m2
  #MI_artificial={'ring':[1.66465125e-43,8.32325625e-44,8.323256249999998e-44],'track':[1.597027387500013e-45,8.831999703266061e-43,8.835985561608938e-43]}
  for part in ['ring','track']:
    if part=='ring':
      atom_no_list=config.ring_atom_no_list
    if part=='track':
      atom_no_list=config.track_atom_no_list
    cords_list=[]
    mass_list=[]
    for atom_no in atom_no_list:
      atom_cords=frame1_final_cords_df[frame1_final_cords_df['atom_no']==atom_no][['x','y','z']].values[0]
      atom_type=frame1_final_cords_df[frame1_final_cords_df['atom_no']==atom_no]['atom'].values[0].lower()
      mass=atomic_mass.atomic_mass_dict[atom_type]
      mass_list.append(mass)
      cords_list.append(atom_cords) 
    MI=physics._getMI(cords_list,mass_list,axis)
    print(f'{part} MI = {MI}')
  #frame2
  #ring = 1.46E-43 kg.m2
  #track = 1.65-45 kg.m2
  #MI_artificial={'ring':[1.66465125e-43,8.32325625e-44,8.323256249999998e-44],'track':[1.597027387500013e-45,8.831999703266061e-43,8.835985561608938e-43]}
  for part in ['ring','track']:
    if part=='ring':
      atom_no_list=config.ring_atom_no_list
    if part=='track':
      atom_no_list=config.track_atom_no_list
    cords_list=[]
    mass_list=[]
    for atom_no in atom_no_list:
      atom_cords=frame2_final_cords_df[frame2_final_cords_df['atom_no']==atom_no][['x','y','z']].values[0]
      atom_type=frame2_final_cords_df[frame2_final_cords_df['atom_no']==atom_no]['atom'].values[0].lower()
      mass=atomic_mass.atomic_mass_dict[atom_type]
      mass_list.append(mass)
      cords_list.append(atom_cords)
    MI=physics._getMI(cords_list,mass_list,axis)
    print(f'{part} MI = {MI}')

#RKE
def getRKETwoFrames(ideal=False,method='energy_rot_hybrid_1'):
  print(f'ideal = {ideal}\nmethod = {method}')
  if ideal:
    file_path='test_systems/ring_track_two_frames_ideal.xyz'
  else:
    file_path='test_systems/ring_track_two_frames_non_ideal.xyz'
  frame1_no=0
  frame2_no=1

  file=open(file_path,'r')
  RKE=energy.getRKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=method)
  file.close()
  print(f'Ring Absolute RKE = {RKE}')

  file=open(file_path,'r')
  RKE=energy.getRKE(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=method)
  file.close()
  print(f'Track Absolute RKE = {RKE}')

  file=open(file_path,'r')
  RKE=energy.getRKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=method)
  file.close()
  print(f'Ring Relative RKE = {RKE}')

def getRKEMultiFrame(ideal=True,method='energy_rot_hybrid_1'):
  print(f'ideal = {ideal}\nmethod = {method}')
  if ideal:
    file_path='test_systems/ring_track_multi_frame_ideal.xyz'
  else:
    file_path='test_systems/ring_track_multi_frame_non_ideal.xyz'
  frame1_no=50
  frame2_no=52

  file=open(file_path,'r')
  RKE=energy.getRKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=method)
  file.close()
  print(f'Ring Absolute RKE = {RKE}')

  file=open(file_path,'r')
  RKE=energy.getRKE(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=method)
  file.close()
  print(f'Track Absolute RKE = {RKE}')

  file=open(file_path,'r')
  RKE=energy.getRKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=method)
  file.close()
  print(f'Ring Relative RKE = {RKE}')

def getAvgRKE(ideal=True,method='energy_rot_hybrid_1'):
  print(f'ideal = {ideal}\nmethod = {method}')
  if ideal:
    file_path='test_systems/ring_track_multi_frame_ideal.xyz'
  else:
    file_path='test_systems/ring_track_multi_frame_non_ideal.xyz'
  start_frame_no=0
  end_frame_no=99
  step_size=10

  file=open(file_path,'r')
  avg_RKE,data=energy.getAvgRKE(file,start_frame_no,end_frame_no,step_size=step_size,part1='ring',part2='track',type='absolute',method=method,part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Average absolute ring RKE = {avg_RKE}')
  print(data)

  file=open(file_path,'r')
  avg_RKE,data=energy.getAvgRKE(file,start_frame_no,end_frame_no,step_size=step_size,part1='track',part2='track',type='absolute',method=method,part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Average absolute track RKE = {avg_RKE}')
  print(data)

  file=open(file_path,'r')
  avg_RKE,data=energy.getAvgRKE(file,start_frame_no,end_frame_no,step_size=step_size,part1='ring',part2='track',type='relative',method=method,part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net ring relative RKE = {avg_RKE}')
  print(data)

#TKE
def getTKETwoFrames(ideal=False,method='energy_trans_com'):
  print(f'ideal = {ideal}\nmethod = {method}')
  if ideal:
    file_path='test_systems/ring_track_two_frames_ideal.xyz'
  else:
    file_path='test_systems/ring_track_two_frames_non_ideal.xyz'
  frame1_no=0
  frame2_no=1

  file=open(file_path,'r')
  TKE=energy.getTKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=method)
  file.close()
  print(f'Ring Absolute TKE = {TKE}')

  file=open(file_path,'r')
  TKE=energy.getTKE(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=method)
  file.close()
  print(f'Track Absolute TKE = {TKE}')

  file=open(file_path,'r')
  TKE=energy.getTKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=method)
  file.close()
  print(f'Ring Relative TKE = {TKE}')

def getTKEMultiFrame(ideal=True,method='energy_trans_com'):
  print(f'ideal = {ideal}\nmethod = {method}')
  if ideal:
    file_path='test_systems/ring_track_multi_frame_ideal.xyz'
  else:
    file_path='test_systems/ring_track_multi_frame_non_ideal.xyz'
  frame1_no=50
  frame2_no=52

  file=open(file_path,'r')
  TKE=energy.getTKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=method)
  file.close()
  print(f'Ring Absolute TKE = {TKE}')

  file=open(file_path,'r')
  TKE=energy.getTKE(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=method)
  file.close()
  print(f'Track Absolute TKE = {TKE}')

  file=open(file_path,'r')
  TKE=energy.getTKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=method)
  file.close()
  print(f'Ring Relative TKE = {TKE}')

def getAvgTKE(ideal=True,method='energy_trans_com'):
  print(f'ideal = {ideal}\nmethod = {method}')
  if ideal:
    file_path='test_systems/ring_track_multi_frame_ideal.xyz'
  else:
    file_path='test_systems/ring_track_multi_frame_non_ideal.xyz'
  start_frame_no=0
  end_frame_no=99
  step_size=10

  file=open(file_path,'r')
  avg_TKE,data=energy.getAvgTKE(file,start_frame_no,end_frame_no,step_size=step_size,part1='ring',part2='track',type='absolute',method=method,part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Average absolute ring TKE = {avg_TKE}')
  print(data)

  file=open(file_path,'r')
  avg_TKE,data=energy.getAvgTKE(file,start_frame_no,end_frame_no,step_size=step_size,part1='track',part2='track',type='absolute',method=method,part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Average absolute track TKE = {avg_TKE}')
  print(data)

  file=open(file_path,'r')
  avg_TKE,data=energy.getAvgTKE(file,start_frame_no,end_frame_no,step_size=step_size,part1='ring',part2='track',type='relative',method=method,part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net ring relative TKE = {avg_TKE}')
  print(data)

#get_dist_pt_line()
getMI()
#getRKETwoFrames()
#getRKEMultiFrame()
#getAvgRKE()

#getTKETwoFrames()
#getTKEMultiFrame()
#getAvgTKE()

