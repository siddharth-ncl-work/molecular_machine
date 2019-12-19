from math import cos,sin,acos,asin
import numpy as np

from lib.io_chem import io
from lib.basic_operations import vector
from source.shift_origin import shiftOrigin
import config


def getNetRotation(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  net_rotation=0
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=config.frame_no_pos)
  for curr_frame_no in range(start_frame_no+1,end_frame_no+1,step_size):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=config.frame_no_pos)
    rotation=_getRotation(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_rotation+=rotation    
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
  return net_rotation

def getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  return _getRotation(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getRotation(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  rotation=0
  if type=='absolute':
    if method=='rot_atomic_r_t':
      rotation=rot_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)    
    elif method=='rot_atomc_t_r':
      print('to be implemented in future')
    else:
      print('Please provide an appropriate method')
  elif type=='relative':
    if method=='rot_atomic_r_t':
      part1_rotation=rot_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_atomic_r_t(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_atomic_t_r':
      print('to be implemented in future')
    else:
      print('Please provide an appropriate method')
  return rotation

def rot_atomic_r_t(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  part_rotation=0
  if part=='ring':
    _atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part=='track':
    _atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
  if config.axis=='x':
    axis=0
  elif config.axis=='y':
    axis=1
  elif config.axis=='z':
    axis=2
  frame1_cords,frame2_cords=shiftOrigin(frame1_cords,frame2_cords)
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]  
    atom_rotation=getRPYAngles(frame1_atom_cords,frame2_atom_cords,axis=config.axis)
    #getRPYAngles with new prev_frame_cords
    #translate cords of prev_frame
    part_rotation+=atom_rotation[axis]
  avg_part_rotation=part_rotation/len(_atom_list)
  return avg_part_rotation

def atomic_t_r(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  pass
  #translate cords of prev_frame
  #getRPYAngles with new prev_frame_cords

def getRotMat(axis,theta):
  R=np.zeros((3,3))
  s=vector.getUnitVec(axis)
  t=theta
  vv=(1-cos(t))
  R[0][0]=s[0]*s[0]*vv+cos(t)
  R[0][1]=s[0]*s[1]*vv-s[2]*sin(t)
  R[0][2]=s[0]*s[2]*vv+s[1]*sin(t)
  R[1][0]=s[0]*s[1]*vv+s[2]*sin(t)
  R[1][1]=s[1]*s[1]*vv+cos(t)
  R[1][2]=s[1]*s[2]*vv-s[0]*sin(t)
  R[2][0]=s[0]*s[2]*vv-s[1]*sin(t)
  R[2][1]=s[1]*s[2]*vv+s[0]*sin(t)
  R[2][2]=s[2]*s[2]*vv+cos(t)
  return R

def rotateAlongAxis(cords,axis,theta):
  new_cords=cords.copy()
  R=getRotMat(axis,theta)
  _cords=cords[['x','y','z']].values
  new_cords[['x','y','z']]=np.matmul(_cords,R.T)
  return new_cords

def getRPYAngles(v1,v2,axis='x'):
  rpy=np.zeros(3)
  s=vector.getCrossProduct(v1,v2) 
  s=vector.getUnitVec(s)
  theta=vector.getAngleR(v1,v2)
  R=getRotMat(s,theta)
  if axis=='x':
    rpy[1]=asin(-1*R[2][0])
    rpy[0]=asin(R[2][1]/cos(rpy[1]))
    rpy[2]=asin(R[1][0]/cos(rpy[1]))
  elif axis=='y':
    rpy[2]=asin(-1*R[0][1])
    rpy[1]=asin(R[0][2]/cos(rpy[2]))
    rpy[0]=asin(R[2][1]/cos(rpy[2]))
  elif axis=='z':
    rpy[0]=asin(-1*R[1][2])
    rpy[1]=asin(R[0][2]/cos(rpy[0]))
    rpy[2]=asin(R[1][0]/cos(rpy[0]))
  else:
    print('To be implemented')
  return rpy

