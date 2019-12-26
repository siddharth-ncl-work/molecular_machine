import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from source import rotation,translation
from helper_functions import createSystem,getRingDf,getTrackDf


def oneAtomSystem():
  file_path='test_systems/one_atom_system.xyz'
  cords_list=[[3,0,0]]
  atom_list=['c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)

def multiAtomSystem():
  file_path='test_systems/multi_atom_system.xyz'
  cords_list=[[3,3,0],[-6,5,-7]]
  atom_list=['c','c']
  createSystem(cords_list,atom_list,file_path,add_axes=False)
 
def ringCords():
  file_path='test_systems/ring.xyz'
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
  
def trackCords():
  file_path='test_systems/track.xyz'
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
 
def ringTrackAtOrigin():
  file_path='test_systems/ring_track_at_origin.xyz'
  ring_cords_list=ringCords()
  track_cords_list=trackCords()
  cords_list=[]
  atom_list=[]
  cords_list.extend(ring_cords_list)
  cords_list.extend(track_cords_list)
  atom_list=len(cords_list)*['c']
  #atom_list[0]=atom_list[-1]='n'
  createSystem(cords_list,atom_list,file_path,add_axes=False)
  
def ringTrackTwoFrames():
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  ringTrackAtOrigin()

  rpy=[45,0,0]
  distance=2.56

  input_system_file_path='test_systems/ring_track_at_origin.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  frame1_initial_cords_df=input_system_cords_df.copy()
  #ring
  frame1_ring_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(range(config.ring_start_atom_no,config.ring_end_atom_no+1))]
  df=rotation.rotateAlongAxis(frame1_ring_cords_df,x,math.radians(rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
  frame2_initial_ring_cords_df=translation.translateAlongAxis(df,x,distance)
  #track
  frame1_track_cords_df=frame1_initial_cords_df[frame1_initial_cords_df['atom_no'].isin(range(config.track_start_atom_no,config.track_end_atom_no+1))]
  df=rotation.rotateAlongAxis(frame1_track_cords_df,x,math.radians(rpy[0]))
  df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
  df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
  frame2_initial_track_cords_df=translation.translateAlongAxis(df,x,distance)
  #frame2
  frame2_initial_cords_df=pd.concat([frame2_initial_ring_cords_df,frame2_initial_track_cords_df])
   
  #transform both frames
  axis=[-1,2,-2]
  theta=0
  distance=0
  frame1_final_cords_df=rotation.rotateAlongAxis(frame1_initial_cords_df,axis,math.radians(theta))
  frame2_final_cords_df=rotation.rotateAlongAxis(frame2_initial_cords_df,axis,math.radians(theta))
  frame1_final_cords_df=translation.translateAlongAxis(frame1_final_cords_df,axis,distance)
  frame2_final_cords_df=translation.translateAlongAxis(frame2_final_cords_df,axis,distance)
  
  file=open('test_systems/ring_track_two_frames.xyz','w')
  io.writeFileMd(file,frame1_final_cords_df,0,frame_no_pos=config.frame_no_pos)
  io.writeFileMd(file,frame2_final_cords_df,1,frame_no_pos=config.frame_no_pos)
  file.close()

def ringTrackMultiFrame():
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  ringTrackAtOrigin()

  total_frames=100
  ring_theta=0
  ring_distance=0
  ring_d_theta=1.5
  ring_d_distance=0.1
  track_theta=0
  track_distance=0
  track_d_theta=-0.75
  track_d_distance=-0.05

  input_system_file_path='test_systems/ring_track_at_origin.xyz'
  input_system_cords_df=io.readFile(input_system_file_path)
  file=open('test_systems/ring_track_multi_frame.xyz','w')
  for curr_frame_no in range(total_frames):
    #ring
    input_system_ring_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(range(config.ring_start_atom_no,config.ring_end_atom_no+1))]
    df=rotation.rotateAlongAxis(input_system_ring_cords_df,x,math.radians(ring_theta))
    #df=rotation.rotateAlongAxis(df,y,math.radians(rpy[1]))
    #df=rotation.rotateAlongAxis(df,z,math.radians(rpy[2]))
    curr_frame_ring_cords_df=translation.translateAlongAxis(df,x,ring_distance)
    #track
    input_system_track_cords_df=input_system_cords_df[input_system_cords_df['atom_no'].isin(range(config.track_start_atom_no,config.track_end_atom_no+1))]
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
    io.writeFileMd(file,curr_frame_cords_df,curr_frame_no,frame_no_pos=config.frame_no_pos)

    ring_theta+=ring_d_theta
    ring_distance+=ring_d_distance
    track_theta+=track_d_theta
    track_distance+=track_d_distance
  file.close()
    

if __name__=='__main__':
  #oneAtomSystem()  


  #multiAtomSystem()
  #rpyOneAtomSystem()
  #ringCords()
  #trackCords()
  #ringTrackAtOrigin()
  #ringTrackTwoFrames()
  ringTrackMultiFrame()
