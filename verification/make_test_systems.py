import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from source import rotation,translation,init,shift_origin
from helper_functions import createSystem,getRingDf,getTrackDf


def oneAtomSystemArtificial():
  file_path='test_systems/one_atom_system_artificial_system.xyz'
  cords_list=[[3,0,0]]
  atom_list=['c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)

def multiAtomSystemArtificial():
  file_path='test_systems/multi_atom_system_artificial_system.xyz'
  cords_list=[[3,3,0],[-6,5,-7]]
  atom_list=['c','c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)
 
def ringCordsArtificial():
  file_path='test_systems/ring_artificial_system.xyz'
  n=20
  r=5
  initial_cords=[0,r,0]
  atom_data={'atom':['c'],'atom_no':[0],'x':initial_cords[0],'y':initial_cords[1],'z':initial_cords[2]}
  initial_df=pd.DataFrame.from_dict(atom_data)
  theta=2*math.pi/n
  ring_cords_list=[initial_cords]
  for i in range(1,n): 
    df=rotation.rotateAlongAxis(initial_df,[1,0,0],theta*i)
    ring_cords_list.append(df[['x','y','z']].values[0])
  ring_atom_list=['c']*n
  createSystem(ring_cords_list,ring_atom_list,file_path,add_axes=False)
  return ring_cords_list 
  
def trackCordsArtificial():
  file_path='test_systems/track_artificial_system.xyz'
  n=18
  initial_cords=[0,0,0]
  track_cords_list=[initial_cords]
  x=0
  for i in range(1,n):
    x+=1 
    if i%2==0:
      y=0.5
    else:
      y=-0.5   
    track_cords_list.append([x,y,0])
  ring_atom_list=['c']*n
  createSystem(track_cords_list,ring_atom_list,file_path,add_axes=False)
  return track_cords_list
 
def ringTrackAtOriginIdealArtificial():
  file_path='test_systems/ring_track_at_origin_ideal_artificial_system.xyz'
  ring_cords_list=ringCordsArtificial()
  track_cords_list=trackCordsArtificial()
  cords_list=[]
  atom_list=[]
  cords_list.extend(ring_cords_list)
  cords_list.extend(track_cords_list)
  atom_list=len(cords_list)*['c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)
  
def ringTrackAtOriginNonIdealArtificial():
  file_path='test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
  ring_cords_list=ringCordsArtificial()
  track_cords_list=trackCordsArtificial()
  cords_list=[]
  atom_list=[]
  cords_list.extend(ring_cords_list)
  cords_list.extend(track_cords_list)
  atom_list=len(cords_list)*['c']
  total_ring_atoms=len(ring_cords_list)
  total_track_atoms=len(track_cords_list)
  atom_list[:total_ring_atoms//2]=['Si']*(total_ring_atoms//2)
  atom_list[-total_track_atoms//2:]=['s']*(total_track_atoms//2)
  createSystem(cords_list,atom_list,file_path,add_axes=False)

def ringTrackTwoFramesIdealArtificial():
  output_file_path='test_systems/ring_track_two_frames_ideal_artificial_system.xyz'
  output_file=file=open(output_file_path,'w')
  x=[1,0,0]

  ring_theta=45
  track_theta=35
  ring_distance=2
  track_distance=1

  input_system_file_path='test_systems/ring_track_at_origin_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(range(config.ring_start_atom_no,config.ring_end_atom_no+1))]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_theta)) 
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(range(config.track_start_atom_no,config.track_end_atom_no+1))]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(track_theta))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])

  #transform both frames
  axis=[1,1,1]
  theta=45.24
  distance=1.67
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)

  io.writeFileMd(output_file,frame1_final_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_final_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()

def ringTrackTwoFramesNonIdealArtificial(ring_rpy=[0,0,0],track_rpy=[20.6,0,0]):
  output_file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]

  ring_distance=2
  track_distance=1

  input_system_file_path='test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.ring_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(ring_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(ring_rpy[2]))
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.track_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(track_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(track_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(track_rpy[2]))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])
  #transform both frames 
  axis=[-10.2,-42,-6]
  theta=60.5
  distance=5.3
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)
  
  output_file=open(output_file_path,'w')
  io.writeFileMd(output_file,frame1_final_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_final_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()

def ringTrackMultiFrameIdealArtificial():
  output_file_path='test_systems/ring_track_multi_frame_ideal_artificial_system.xyz'
  output_file=open(output_file_path,'w')
  x=[1,0,0]

  total_frames=100
  ring_theta=0
  track_theta=0
  ring_d_theta=1
  track_d_theta=-0.5
  ring_distance=0
  track_distance=0
  ring_d_distance=0.1
  track_d_distance=-0.05

  input_system_file_path='test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  for curr_frame_no in range(total_frames):
    #ring
    input_system_ring_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(ring_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_ring_cords_df,x,math.radians(ring_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
    #track
    input_system_track_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(track_atom_no_list)]
    df=rotation.rotateAlongAxis(input_system_track_cords_df,x,math.radians(track_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
    #frame
    curr_frame_cords_df=pd.concat([curr_frame_ring_cords_df,curr_frame_track_cords_df])
    #transform frames
    axis=[1,1,1]
    theta=45.24
    distance=1.67
    curr_frame_cords_df=rotation.rotateAlongAxis(curr_frame_cords_df,axis,math.radians(theta))
    curr_frame_cords_df=translation.translateAlongAxis(curr_frame_cords_df,axis,distance)
    io.writeFileMd(output_file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    ring_theta+=ring_d_theta
    ring_distance+=ring_d_distance
    track_theta+=track_d_theta
    track_distance+=track_d_distance
  output_file.close()
    
def ringTrackMultiFrameNonIdealArtificial():
  pass

def ringTrackAtOriginSemiReal():
  file_path='test_systems/ring_track_at_origin_semi_real_system.xyz'
  frame1_no=0
  frame2_no=1000

  with open(config.test_file_path,'r') as file:
    frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  io.writeFile(file_path,frame1_cords)

def ringTrackTwoFramesSemiReal(ring_rpy=[0,0,0],track_rpy=[0,0,0]):
  output_file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  
  ring_distance=2
  track_distance=1
  
  input_system_file_path='test_systems/ring_track_at_origin_semi_real_system.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.ring_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(ring_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(ring_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(ring_rpy[2]))
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(config.track_atom_no_list)]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(track_rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(track_rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(track_rpy[2]))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,track_distance)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])

  #transform both frames
  axis=[-10.2,-42,-6]
  theta=60.5
  distance=5.3
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)
  output_file=open(output_file_path,'w')
  io.writeFileMd(output_file,frame1_final_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(output_file,frame2_final_cords_df,1,frame_no_pos=config.frame_no_pos)
  output_file.close()


if __name__=='__main__':
  #oneAtomSystemArtificial() 
  #multiAtomSystemArtificial()
  #rpyOneAtomSystemArtificial()
  #ringCordsArtificial()
  #trackCordsArtificial()
  #ringTrackTwoFramesIdealArtificial()
  ringTrackAtOriginNonIdealArtificial()
  init.initConfig('test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz',ring_atom_no=0,track_atom_no=30)
  ringTrackTwoFramesNonIdealArtificial()
  #ringTrackMultiFrameIdealArtificial()
  ringTrackAtOriginSemiReal()
  init.initConfig(config.test_file_path)
  ringTrackTwoFramesSemiReal()
