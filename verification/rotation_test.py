import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from lib.basic_operations import vector
from source import rotation,shift_origin
from helper_functions import createSystem,getIntersectionPoints


def rotateAlongAxis():
  test_system_file_path='test_systems/multi_atom_system.xyz'
  test_system_df=io.readFile(test_system_file_path)
  axis=[1,1,1]
  axis=vector.getUnitVec(axis)
  theta=math.radians(124)
  output_df=rotation.rotateAlongAxis(test_system_df,axis,theta)
  test_system_cords_list=list(test_system_df[['x','y','z']].values)
  output_cords_list=list(output_df[['x','y','z']].values)
  cords_list=[]
  cords_list.extend(test_system_cords_list)
  cords_list.extend(output_cords_list)
  test_system_atom_list=list(test_system_df['atom'].values)
  output_atom_list=list(output_df['atom'].values)
  atom_list=[]
  atom_list.extend(test_system_atom_list)
  atom_list.extend(output_atom_list)
  intersection_points_list,intersection_atom_list=getIntersectionPoints(test_system_cords_list,axis)
  cords_list.extend(intersection_points_list)
  atom_list.extend(intersection_atom_list)
  output_file_path='output/rotate_along_axis.xyz'
  createSystem(cords_list,atom_list,output_file_path)
 
def getOneAtomRPYAngles():
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  initial_cords=[5.2,4,0]
  print(initial_cords)
  atom_data={'atom':['c'],'atom_no':[0],'x':initial_cords[0],'y':initial_cords[1],'z':initial_cords[2]}
  initial_df=pd.DataFrame.from_dict(atom_data)
  df=rotation.rotateAlongAxis(initial_df,x,math.radians(0))
  df=rotation.rotateAlongAxis(df,y,math.radians(0))
  final_df=rotation.rotateAlongAxis(df,z,math.radians(0))
  final_cords=final_df[['x','y','z']].values[0]
  print(final_cords)

  rpy=rotation.getRPYAngles(initial_cords,final_cords)
  rpy_d=map(math.degrees,rpy)
  for angle in rpy_d:
    print(angle)
  df=rotation.rotateAlongAxis(initial_df,x,rpy[0])
  df=rotation.rotateAlongAxis(df,y,rpy[1])
  df=rotation.rotateAlongAxis(df,z,rpy[2])  
  print(df[['x','y','z']].values[0])
 
#rot_atomic_r_t is not suitable for track 
def rot_atomic_r_t():
  frame1_no=0
  frame2_no=1
  file=open('test_systems/ring_track_two_frames.xyz','r')
  
  frame1_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos) 
  file.close()
  _rotation=rotation.rot_atomic_r_t(frame1_cords_df,frame2_cords_df,part='ring')
  print(_rotation)

def rot_atomic_r_t_2():
  frame1_no=0
  frame2_no=1
  file=open('test_systems/ring_track_two_frames.xyz','r')
  frame1_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  file.close()
  _rotation=rotation.rot_atomic_r_t_2(frame1_cords_df,frame2_cords_df,part='ring')
  print(_rotation)

def getRotationTwoFrames():
  file_path='test_systems/ring_track_two_frames.xyz'
  frame1_no=0
  frame2_no=1
  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t_2')
  file.close()
  print(f'Ring Absolute Rotation = {_rotation}')

  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method='rot_atomic_r_t_2')
  file.close()
  print(f'Track Absolute Rotation = {_rotation}')
 
  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method='rot_atomic_r_t_2')
  file.close()
  print(f'Ring Relative Rotation = {_rotation}')

def getRotationMultiFrame():
  file_path='test_systems/ring_track_multi_frame.xyz'
  frame1_no=50
  frame2_no=52
  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t_2')
  file.close()
  print(f'Ring Absolute Rotation = {_rotation}')

  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method='rot_atomic_r_t_2')
  file.close()
  print(f'Track Absolute Rotation = {_rotation}')

  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method='rot_atomic_r_t_2')
  file.close()
  print(f'Ring Relative Rotation = {_rotation}')


def getNetRotation():
  file_path='test_systems/ring_track_multi_frame.xyz'
  start_frame_no=0
  end_frame_no=99

 
  file=open(file_path,'r')
  net_ring_rotation=rotation.getNetRotation(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t_2',part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net absolute ring rotation = {net_ring_rotation}')
 
  file=open(file_path,'r')
  net_ring_rotation=rotation.getNetRotation(file,start_frame_no,end_frame_no,step_size=1,part1='track',part2='track',type='absolute',method='rot_atomic_r_t_2',part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net absolute track rotation = {net_ring_rotation}')

  file=open(file_path,'r')
  net_ring_rotation=rotation.getNetRotation(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='relative',method='rot_atomic_r_t_2',part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net ring rotation = {net_ring_rotation}')

    
#rotateAlongAxis() 
#getRPYAngles()
#rot_atomic_r_t_2()
#getRotation()
getRotationMultiFrame()
getNetRotation()
