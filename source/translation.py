from math import cos,sin,acos,asin
import numpy as np
from tqdm import tqdm

from lib.io_chem import io
from lib.basic_operations import vector,physics,constants
from source import shift_origin
import config


def getNetTranslation(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='trans_com',part1_atom_list=[],part2_atom_list=[]):
  net_translation=0
  data={'frame_no':[],'translation':[]}
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=config.frame_no_pos)
  for curr_frame_no in tqdm(range(start_frame_no+step_size,end_frame_no+1,step_size)):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=config.frame_no_pos)
    translation=_getTranslation(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_translation+=translation    
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
    data['frame_no'].append(curr_frame_no)
    data['translation'].append(translation)
  return (net_translation,data)

def getTranslation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='trans_com',part1_atom_list=[],part2_atom_list=[],unit='m'):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  return _getTranslation(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list,unit=unit)

def _getTranslation(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',method='trans_com',part1_atom_list=[],part2_atom_list=[],unit='m'):
  translation=0
  if type=='absolute':
    if method=='trans_atomic_r_t':
      translation=trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)    
    elif method=='trans_com_1':
      translation=trans_com_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='trans_com_2':
      translation=trans_com_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list,unit=unit)
    elif method=='trans_com_3':
      translation=trans_com_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list,unit=unit)
    elif method=='trans_atomic_t_r':
      print('to be implemented')
    else:
      print('Please provide an appropriate method')
  elif type=='relative':
    if method=='trans_atomic_r_t':
      part1_translation=trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_translation=trans_atomic_r_t(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_translation-part2_translation
    elif method=='trans_com_1':
      part1_translation=trans_com_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_translation=trans_com_1(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      translation=part1_translation-part2_translation
    elif method=='trans_com_2':
      part1_translation=trans_com_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list,unit=unit)
      part2_translation=trans_com_2(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list,unit=unit)
      translation=part1_translation-part2_translation
    elif method=='trans_com_3':
      part1_translation=trans_com_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list,unit=unit)
      part2_translation=trans_com_3(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list,unit=unit)
      translation=part1_translation-part2_translation
    elif method=='trans_atomic_t_r':
      print('to be implemented') 
    else:
      print('Please provide an appropriate method')
  return translation

#trans_atomic_r_t is not a suitable method to calculate translation
def trans_atomic_r_t(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  part_translation=0
  avg_part_translation=0
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
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='translation')
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]  
    #getRPYAngles with new prev_frame_cords
    #translate cords of prev_frame
    trans_vec=getAtomicDisplacement(frame1_atom_cords,frame2_atom_cords)
    part_translation+=trans_vec[axis]
  avg_part_translation=part_translation/len(_atom_list)
  return avg_part_translation*constants.angstrom

def trans_com_1(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    _atom_list=config.ring_atom_no_list
  elif part=='track':
    _atom_list=config.track_atom_no_list
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='translation')
  com1=physics.getCom(frame1_cords,atom_list=_atom_list) 
  com2=physics.getCom(frame2_cords,atom_list=_atom_list)
  translation=[0.0,0.0,0.0]
  translation[0]=com2[0]-com1[0]
  translation[1]=com2[1]-com1[1]
  translation[2]=com2[2]-com1[2]
  if config.axis=='x':
    axis=0
  elif config.axis=='y':
    axis=1
  elif config.axis=='z':
    axis=2
  return translation[axis]*constants.angstrom

def trans_com_2(frame1_cords,frame2_cords,part='ring',atom_list=[],unit='m'):
  if part=='ring':
    _atom_list=config.ring_atom_no_list
  elif part=='track':
    _atom_list=config.track_atom_no_list
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
  translation_vector=[0,0,0]
  trans_axis=[0,0,0]
  com1=physics.getCom(frame1_cords,atom_list=_atom_list)
  com2=physics.getCom(frame2_cords,atom_list=_atom_list)
  translation_vector[0]=com2[0]-com1[0]
  translation_vector[1]=com2[1]-com1[1]
  translation_vector[2]=com2[2]-com1[2]
  cog1=physics.getCog(frame1_cords,atom_list=config.ring_atom_no_list)
  cog2=physics.getCog(frame2_cords,atom_list=config.ring_atom_no_list)
  ref_axis_atom1_cords=frame1_cords[frame1_cords['atom_no']==config.ref_axis_atom1_no][['x','y','z']].values[0]
  ref_axis_atom2_cords=frame1_cords[frame1_cords['atom_no']==config.ref_axis_atom2_no][['x','y','z']].values[0]
  trans_axis[0]=ref_axis_atom2_cords[0]-ref_axis_atom1_cords[0]
  trans_axis[1]=ref_axis_atom2_cords[1]-ref_axis_atom1_cords[1]
  trans_axis[2]=ref_axis_atom2_cords[2]-ref_axis_atom1_cords[2]
  if unit=='m':
    return vector.getProjection(translation_vector,trans_axis)*constants.angstrom
  elif unit.upper()=='A':
    return vector.getProjection(translation_vector,trans_axis)

def trans_com_3(frame1_cords,frame2_cords,part='ring',atom_list=[],unit='m'):
  if part=='ring':
    _atom_list=config.ring_atom_no_list
  elif part=='track':
    _atom_list=config.track_atom_no_list
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list

  com_displacement=[0,0,0]
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='translation',ref_axis_alignment=False)
  com1=physics.getCom(frame1_cords,atom_list=_atom_list)
  com2=physics.getCom(frame2_cords,atom_list=_atom_list)
  for i in range(3):
    com_displacement[i]=com2[i]-com1[i]
  print(com1)
  print(com2)
  print(com_displacement)
  if config.axis=='x':
    axis=0
  elif config.axis=='y':
    axis=1
  elif config.axis=='z':
    axis=2
  if unit=='m':
    return com_displacement[axis]*constants.angstrom
  elif unit.upper()=='A':
    return com_displacement[axis]

def translateAlongAxis(cords,axis,distance):
  new_cords=cords.copy()
  _axis=vector.getUnitVec(axis)
  translation_vector=[0,0,0]
  translation_vector[0]=distance*_axis[0]
  translation_vector[1]=distance*_axis[1]
  translation_vector[2]=distance*_axis[2]
  new_cords['x']=new_cords['x']+translation_vector[0]
  new_cords['y']=new_cords['y']+translation_vector[1]
  new_cords['z']=new_cords['z']+translation_vector[2]  
  return new_cords
 
def getAtomicDisplacement(v1,v2):
  mag1=vector.getMag(v1)
  mag2=vector.getMag(v2)
  trans_vec=(mag2-mag1)*vector.getUnitVec(v2) 
  return trans_vec
 
