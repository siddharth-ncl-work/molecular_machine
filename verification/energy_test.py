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

def getMI():
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
  #
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  frame1_no=0
  frame2_no=1
  file=open('test_systems/ring_track_two_frames_non_ideal.xyz','r')
  frame1_initial_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_initial_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  frame1_final_cords_df,frame2_final_cords_df=shift_origin.shiftOrigin(frame1_initial_cords_df,frame2_initial_cords_df)
  #frame1
  #ring = 1.46E-43 kg.m2
  #track = 1.65-45 kg.m2
  for part in ['ring','track']:
    if part=='ring':
      atom_no_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    if part=='track':
      atom_no_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
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
  for part in ['ring','track']:
    if part=='ring':
      atom_no_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    if part=='track':
      atom_no_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
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


get_dist_pt_line()
getMI()

