import numpy as np
from math import cos,sin,acos,asin

import sys
sys.path.append(['..'])

from lib.basic_operations import vector
import config


def getNetTranslation(file,start_frame_no,end_frame_no,step_size,part1='ring',part2='track',type='abs',method='atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  assert curr_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=2)
  for curr_frame_no in range(start_frame_no+1,end_frame_no+1,step_size):
    curr_frame_cords=io.readFileMd(file,curr_frame_no)
    rotation=_getTranslation(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_translation+=translation    
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
  return net_translation

def getTranslation(file,frame1_no,frame2_no,part1='ring',part2='track',type='abs',method='trans_com',part1_atom_list=[],part2_atom_list=[]):
  assert curr_frame_no>=start_frame_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_cords,frame_no_pos=2)
  frame2_cords=io.readFileMd(file,frame2_cords,frame_no_pos=2)
  return _getTranslation(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getTranslation(frame1_cords,frame2_cords,part1='ring',part2='track',type='abs',method='r+t',part1_atom_list=[],part2_atom_list=[]):
  rotation=None
  if part=='ring':
    _atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part=='track':
    _atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
       
  if type=='abs':
    if method=='trans_atomic_r_t':
      translation=trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)    
    elif method=='trans_com':
      translation=trans_com(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    else:
      print('Please give an appropriate method')
  elif type=='rel':
    if method=='trans_atomic_r_t':
      part1_translation=trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_translation=trans_atomic_r_t(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_translation-part2_translation
    elif method=='trans_com':
      part1_translation=trans_com(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_translation=trans_com(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      translation=part1_translation-part2_translation

    else:
      print('Please give an appropriate method')
  return translation

def trans_atomic_r_t(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
    atom_rotation=getRPYAngles(frame1_atom_cords,frame2_atom_cords)
    #getRPYAngles with new prev_frame_cords
    #translate cords of prev_frame
    mag1=vector.getMag(frame1_atom_cords)
    mag2=vector.getMag(frame2_atom_cords)
    trans_vec=(mag2-mag1)*vector.getUnitVec(frame2_atom_cords)
    net_translation+=trans_vec[ax]
  avg_translation=net_translation/len(atom_list)
  return avg_translation

def trans_com(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    _atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part=='track':
    _atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list

  com1=physics.getCom(frame1_cords,atom_list=_atom_list) 
  com2=physics.getCom(frame2_cords,atom_list=_atom_list)

  translation=[0.0,0.0,0.0]
  translation[0]=com2[0]-com1[0]
  translation[1]=com2[1]-com1[1]
  translation[2]=com2[2]-com1[2]
  
  return translation[config.axis]

