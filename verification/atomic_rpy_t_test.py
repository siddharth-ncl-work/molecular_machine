import math
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from lib.basic_operations import vector,physics
from source import rotation,translation,shift_origin
from helper_functions import createSystem


def atomic_r_t():
  
  frame1_no=0
  frame2_no=1
  file=open('test_systems/ring_track_two_frames.xyz','r')
  
  '''
  frame1_no=225
  frame2_no=1157
  file=open(config.test_file_path,'r')
  '''
  x=[1,0,0]
  y=[0,1,0]
  z=[0,0,1]
  frame1_cords_df=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords_df=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  file.close()
  new_x=[]
  new_y=[]
  new_z=[]
  for atom_no in list(frame1_cords_df['atom_no'].values):
    frame1_atom_cords=frame1_cords_df[frame1_cords_df['atom_no']==atom_no][['x','y','z']].values[0]
    frame2_atom_cords=frame2_cords_df[frame2_cords_df['atom_no']==atom_no][['x','y','z']].values[0]
    rpy=rotation.getRPYAngles(frame1_atom_cords,frame2_atom_cords)
    translation_vector=translation.getAtomicDisplacement(frame1_atom_cords,frame2_atom_cords)
    frame1_atom_cords_df=frame1_cords_df[frame1_cords_df['atom_no']==atom_no]
    df=rotation.rotateAlongAxis(frame1_atom_cords_df,x,rpy[0])
    df=rotation.rotateAlongAxis(df,y,rpy[1])
    df=rotation.rotateAlongAxis(df,z,rpy[2])
    output_df=translation.translateAlongAxis(df,translation_vector,vector.getMag(translation_vector))
    new_x.append(output_df[output_df['atom_no']==atom_no]['x'].values[0])
    new_y.append(output_df[output_df['atom_no']==atom_no]['y'].values[0])
    new_z.append(output_df[output_df['atom_no']==atom_no]['z'].values[0])
  combined_df=frame2_cords_df.copy()
  combined_df.rename(columns={'x':'x_old','y':'y_old','z':'z_old'},inplace=True)
  combined_df['x_new']=new_x
  combined_df['y_new']=new_y
  combined_df['z_new']=new_z
  print(frame1_cords_df)
  combined_df=combined_df[['frame','atom','atom_no','x_old','x_new','y_old','y_new','z_old','z_new']]
  print(combined_df)

atomic_r_t() 
    
    
 
 
