import numpy as np
from math import cos,sin,acos,asin

import sys
sys.path.append(['..'])

from lib.basic_operations import vector
import config

def getRelativeRotation(file,frame1_no,frame2_no,part1='ring',part2='track',method='r+t',part1_atom_list=[],part2_atom_list=[]):
  part1_rotation=getRotation(file,frame1_no,frame2_no,part1=part1,method=method,atom_list=part1_atom_list)
  part2_rotation=getRotation(file,frame1_no,frame2_no,part1=part2,method=method,atom_list=part2_atom_list)
  relative_rotation=part1_rotation-part2_rotation
  return relative_rotation

def getNetRelativeRotation(file,start_frame_no,end_frame_no,step_size,part1='ring',part2='track',method='r+t',part1_atom_list=[],part2_atom_list=[]):
  net_part1_rotation=getNetRotation(file,start_frame_no,end_frame_no,step_size,part=part1,method=method,atom_list=part1_atom_list)
  net_part2_rotation=getNetRotation(file,start_frame_no,end_frame_no,step_size,part=part2,method=method,atom_list=part2_atom_list)
  net_relative_rotation=net_part1_rotation-net_part2_rotation
  return net_relative_rotation

def getNetRotation(file,start_frame_no,end_frame_no,step_size,part='ring',method='r+t',atom_list=[]):
  assert curr_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=2)
  for curr_frame_no in range(start_frame_no+1,end_frame_no+1,step_size):
    curr_frame_cords=io.readFileMd(file,curr_frame_no)
    part_rotation=_getRotation(prev_frame_cords,curr_frame_cords,part=part,method=method,atom_list=[])

    net_part_rotation+=part_rotation    
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
  return net_rotation

def getRotation(file,frame1_no,frame2_no,part='ring',method='r+t',atom_list=[]):
  assert curr_frame_no>=start_frame_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_cords,frame_no_pos=2)
  frame2_cords=io.readFileMd(file,frame2_cords,frame_no_pos=2)
  return _getRotation(frame1_cords,frame2_cords,part=part,method=method,atom_list=atom_list)

def _getRotation(frame1_cords,frame2_cords,part='ring',method='r+t',atom_list=[]):
  avg_rotation=None
  if part=='ring':
    _atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part=='track':
    _atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
       
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values
    if method='r+t':
      atom_rotation=getRPYAngles(frame1_atom_cords,frame2_atom_cords)
    elif method='t+r':
      #translate cords of prev_frame
      #getRPYAngles with new prev_frame_cords
      atom_rotation=-1000
    else:
      print('Please specify valid method')
    net_rotation+=atom_rotation
  avg_rotation=net_rotation/len(_atom_list)
  return avg_rotation

def getRotMat(ax,theta):
  R=np.zeros((3,3))
  s=vector.getUnitVec(ax)
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

def rotateAlongAxis(cords,ax,theta):
  new_cords=cords.copy()
  R=getRotMat(ax,theta)
  _cords=cords[['x','y','z']].values
  new_cords[['x','y','z']]=np.matmul(_cords,R.T)
  return new_cords

def getRPYangles(v1,v2,ax='x'):
  rpy=np.zeros(3)
  s=vector.getCrossProduct(v1,v2) 
  s=vector.getUnitVec(s)
  theta=vector.getAngleR(v1,v2)
  R=getRotMat(s,theta)
  if ax=='x':
    rpy[1]=asin(-1*R[2][0])
    rpy[0]=asin(R[2][1]/cos(rpy[1]))
    rpy[2]=asin(R[1][0]/cos(rpy[1]))
  elif ax=='y':
    rpy[2]=asin(-1*R[0][1])
    rpy[1]=asin(R[0][2]/cos(rpy[2]))
    rpy[0]=asin(R[2][1]/cos(rpy[2]))
  elif ax=='z':
    rpy[0]=asin(-1*R[1][2])
    rpy[1]=asin(R[0][2]/cos(rpy[0]))
    rpy[2]=asin(R[1][0]/cos(rpy[0]))
  else:
    print('To be implemented')
  return rpy

