import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics
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
  rpy=[30,60,40]
  initial_cords=[-3.14563190e-16,  8.90589436e-01,  4.54808153e-01]
  print(f'Input RPY = {rpy} Degrees')
  print(f'Initial coordinates = {initial_cords}')
  atom_data={'atom':['c'],'atom_no':[0],'x':initial_cords[0],'y':initial_cords[1],'z':initial_cords[2]}
  initial_df=pd.DataFrame.from_dict(atom_data)
  df=rotation.rotateAlongAxis(initial_df,x,math.radians(rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
  final_df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
  final_cords=final_df[['x','y','z']].values[0]
  print(f'Final coordinates = {final_cords}')
  rpy=rotation.getRPYAngles(initial_cords,final_cords,unit='degrees')
  print(f'RPY angle from code = {rpy} degrees')
  df=rotation.rotateAlongAxis(initial_df,x,math.radians(rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
  _final_cords=df[['x','y','z']].values[0]  
  print(f'Final coordinate using rpy on initial cords = {_final_cords}')

#rot_atomic_r_t is not suitable for track 
def rot_atomic_r_t(ideal=True):
  frame1_no=0
  frame2_no=1
  if ideal:
    file=open('test_systems/ring_track_two_frames_ideal.xyz','r')
  else:
    file=open('test_systems/ring_track_two_frames_non_ideal.xyz','r')
  frame1_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos) 
  file.close()
  _rotation=rotation.rot_atomic_r_t(frame1_cords_df,frame2_cords_df,part='ring')
  print(_rotation)

def rot_atomic_r_t_2(ideal=True):
  frame1_no=0
  frame2_no=1
  if ideal:
    file=open('test_systems/ring_track_two_frames_ideal.xyz','r')
  else:
    file=open('test_systems/ring_track_two_frames_non_ideal.xyz','r')
  frame1_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  file.close()
  _rotation=rotation.rot_atomic_r_t_2(frame1_cords_df,frame2_cords_df,part='ring')
  print(_rotation)

def getRotationTwoFrames(system='artificial',method='rot_atomic_r_t_2'):
  print(f'system = {system}\nmethod = {method}')
  if system=='semi-real':
    file_path='test_systems/ring_track_two_frames_ideal.xyz'
  elif system=='artificial':
    file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
  frame1_no=0
  frame2_no=1

  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=method)
  file.close()
  print(f'Ring Absolute Rotation = {_rotation}')

  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=method)
  file.close()
  print(f'Track Absolute Rotation = {_rotation}')
 
  file=open(file_path,'r')
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=method)
  file.close()
  print(f'Ring Relative Rotation = {_rotation}')

def getRotationMultiFrame(ideal=True):
  if ideal:
    file_path='test_systems/ring_track_multi_frame_ideal.xyz'
  else:
    file_path='test_systems/ring_track_multi_frame_non_ideal.xyz'
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

def getNetRotation(ideal=True,method='rot_hybrid_1'):
  if ideal:
    file_path='test_systems/ring_track_multi_frame_ideal.xyz'
  else:
    file_path='test_systems/ring_track_multi_frame_non_ideal.xyz'
  start_frame_no=0
  end_frame_no=99
  step_size=10

  file=open(file_path,'r')
  net_ring_rotation,data=rotation.getNetRotation(file,start_frame_no,end_frame_no,step_size=step_size,part1='ring',part2='track',type='absolute',method='rot_hybrid_1',part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net absolute ring rotation = {net_ring_rotation}')
  print(data)

  file=open(file_path,'r')
  net_track_rotation,data=rotation.getNetRotation(file,start_frame_no,end_frame_no,step_size=step_size,part1='track',part2='track',type='absolute',method='rot_hybrid_1',part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net absolute track rotation = {net_track_rotation}')
  print(data)

  file=open(file_path,'r')
  net_ring_rotation,data=rotation.getNetRotation(file,start_frame_no,end_frame_no,step_size=step_size,part1='ring',part2='track',type='relative',method='rot_hybrid_1',part1_atom_list=[],part2_atom_list=[])
  file.close()
  print(f'Net ring relative rotation = {net_ring_rotation}')
  print(data)

def getNearestAtomList():
  c=8
  r=2
  track_atom_list=range(config.track_start_atom_no,config.track_end_atom_no)
  #single frame
  file_path='test_systems/ring_track_at_origin_non_ideal.xyz'
  cords=io.readFile(file_path)
  atom_list=rotation.getNearestAtomList(cords,[c,0,0],[1,0,0],r)
  print(atom_list)
  atom_list=filter(lambda x:x in track_atom_list,atom_list)
  print(list(atom_list))
  #two frames  
  file_path='test_systems/ring_track_two_frames_non_ideal.xyz'
  with open(file_path,'r') as file:
    frame1_cords=io.readFileMd(file,0,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,1,frame_no_pos=config.frame_no_pos)
  trans_axis=[0,0,0]
  ring_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  cog1=physics.getCog(frame1_cords,atom_list=ring_atom_list)
  cog2=physics.getCog(frame2_cords,atom_list=ring_atom_list)
  trans_axis[0]=cog2[0]-cog1[0]
  trans_axis[1]=cog2[1]-cog1[1]
  trans_axis[2]=cog2[2]-cog1[2]
  trans_axis_uv=vector.getUnitVec(trans_axis)
  cog1[0]=cog1[0]+c*trans_axis_uv[0]
  cog1[1]=cog1[1]+c*trans_axis_uv[1]
  cog1[2]=cog1[2]+c*trans_axis_uv[2]
  atom_list=rotation.getNearestAtomList(frame1_cords,cog1,trans_axis,r)
  print(atom_list)
  atom_list=filter(lambda x:x in track_atom_list,atom_list)
  print(list(atom_list))

def rot_part_atomic_r_t_3():
  file_path='test_systems/ring_track_two_frames_non_ideal.xyz'
  with open(file_path,'r') as file:
    frame1_cords=io.readFileMd(file,0,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,1,frame_no_pos=config.frame_no_pos)
  _rotation=rotation.rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part='ring')
  print(f'ring rotation ={_rotation}')
  _rotation=rotation.rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part='track')
  print(f'track rotation ={_rotation}')

#rotateAlongAxis() 
#getOneAtomRPYAngles()
#rot_atomic_r_t_2()
getRotationTwoFrames(system='artificial',method='rot_part_atomic_r_t_3')
#getRotationMultiFrame()
#getNetRotation()
#getNearestAtomList()
#rot_part_atomic_r_t_3()
