import math
from math import cos,sin,acos,asin
import numpy as np
from scipy import stats
from tqdm import tqdm

from lib.io_chem import io
from lib.basic_operations import vector,physics
from source import shift_origin
import config


def getNetRotation(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t_2',part1_atom_list=[],part2_atom_list=[]):
  net_rotation=0
  data={'frame_no':[],'rotation':[]}
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=config.frame_no_pos)
  for curr_frame_no in tqdm(range(start_frame_no+step_size,end_frame_no+1,step_size)):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=config.frame_no_pos)
    rotation=_getRotation(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_rotation+=rotation    
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
    data['frame_no'].append(curr_frame_no)
    data['rotation'].append(rotation)
  return (net_rotation,data)

def getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t_2',part1_atom_list=[],part2_atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  return _getRotation(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getRotation(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',method='rot_atomic_r_t_2',part1_atom_list=[],part2_atom_list=[]):
  rotation=0
  if type=='absolute':
    if method=='rot_atomic_r_t_1':
      rotation=rot_atomic_r_t_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)    
    elif method=='rot_atomic_r_t_2':
      rotation=rot_atomic_r_t_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_atomic_r_t_3':
      rotation=rot_atomic_r_t_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_mol_plane_1':
      rotation=rot_mol_plane_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_mol_plane_2':
      rotation=rot_mol_plane_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_hybrid_1':
      rotation=rot_hybrid_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_hybrid_2':
      rotation=rot_hybrid_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_hybrid_3':
      rotation=rot_hybrid_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_hybrid_3_1':
      rotation=rot_hybrid_3_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_part_atomic_r_t_3':
      rotation=rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
    elif method=='rot_atomic_t_r':
      print('to be implemented in future')
      return
    else:
      print('Please provide an appropriate method')
      return
  elif type=='relative':
    if method=='rot_atomic_r_t_1':
      part1_rotation=rot_atomic_r_t_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_atomic_r_t_1(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_atomic_r_t_2':
      part1_rotation=rot_atomic_r_t_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_atomic_r_t_2(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_atomic_r_t_3':
      part1_rotation=rot_atomic_r_t_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_atomic_r_t_3(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_mol_plane_1':
      part1_rotation=rot_mol_plane_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_mol_plane_1(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_mol_plane_2':
      part1_rotation=rot_mol_plane_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_mol_plane_2(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_hybrid_1':
      part1_rotation=rot_hybrid_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_hybrid_1(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_hybrid_2':
      part1_rotation=rot_hybrid_2(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_hybrid_2(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_hybrid_3':
      part1_rotation=rot_hybrid_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_hybrid_3(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_hybrid_3_1':
      part1_rotation=rot_hybrid_3_1(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_hybrid_3_1(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotatfion
    elif method=='rot_part_atomic_r_t_3':
      part1_rotation=rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part=part1,atom_list=part1_atom_list)
      part2_rotation=rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part=part2,atom_list=part2_atom_list)
      rotation=part1_rotation-part2_rotation
    elif method=='rot_atomic_t_r':
      print('to be implemented in future')
      return
    else:
      print('Please provide an appropriate method')
      return
  return rotation

#rot_atomic_r_t is not suitable for track
def rot_atomic_r_t_1(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]  
    atom_rotation=getRPYAngles(frame1_atom_cords,frame2_atom_cords,axis=config.axis)
    #getRPYAngles with new prev_frame_cords
    #translate cords of prev_frame
    part_rotation+=atom_rotation[axis]
  avg_part_rotation=part_rotation/len(_atom_list)
  return math.degrees(avg_part_rotation)

def rot_atomic_r_t_2(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
  atom_rotation_list=[]
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  frame1_cords[config.axis]=0
  frame2_cords[config.axis]=0 
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_rotation=vector.getAngleR(frame1_atom_cords,frame2_atom_cords)
    sign=vector.getCrossProduct(frame1_atom_cords,frame2_atom_cords)[axis]
    if sign<0:
      sign=-1
    else:
      sign=1 
    #print(math.degrees(sign*atom_rotation))
    atom_rotation_list.append(sign*atom_rotation)
  #part_rotation=stats.mode(atom_rotation_list)[0]
  part_rotation=np.average(atom_rotation_list)
  return math.degrees(part_rotation)

def rot_atomic_r_t_3(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  part_rotation=0
  if part=='ring':
    _atom_list=config.ring_atom_no_list
  elif part=='track':
    _atom_list=config.track_atom_no_list
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
  if config.axis=='x':
    axis=0
  elif config.axis=='y':
    axis=1
  elif config.axis=='z':
    axis=2
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  frame1_cords[config.axis]=0
  frame2_cords[config.axis]=0
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_rotation=getRPYAngles(frame1_atom_cords,frame2_atom_cords,axis=config.axis)
    part_rotation+=atom_rotation[axis]
  avg_part_rotation=part_rotation/len(_atom_list)
  return math.degrees(avg_part_rotation)

def rot_mol_plane_1(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  frame1_part_df=frame1_cords[frame1_cords['atom_no'].isin(_atom_list)]
  frame2_part_df=frame2_cords[frame2_cords['atom_no'].isin(_atom_list)]
  frame1_plane=findMolecularPlane(frame1_part_df)
  frame2_plane=findMolecularPlane(frame2_part_df)
  part_rotation=getRPYAngles(frame1_plane,frame2_plane,axis=config.axis)[axis]
  return math.degrees(part_rotation)

def rot_mol_plane_2(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  frame1_part_df=frame1_cords[frame1_cords['atom_no'].isin(_atom_list)]
  frame2_part_df=frame2_cords[frame2_cords['atom_no'].isin(_atom_list)]
  frame1_plane=findMolecularPlane(frame1_part_df)
  frame2_plane=findMolecularPlane(frame2_part_df)
  frame1_plane[axis]=0
  frame2_plane[axis]=0
  part_rotation=getRPYAngles(frame1_plane,frame2_plane,axis=config.axis)[axis]
  return math.degrees(part_rotation)

def rot_mol_plane_3(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  frame1_part_cords_df=frame1_cords[frame1_cords['atom_no'].isin(_atom_list)]
  frame2_part_cords_df=frame2_cords[frame2_cords['atom_no'].isin(_atom_list)]
  coplanar_atom_no_list=findCoplanarAtoms(frame1_part_cords_df)
  frame1_coplanar_atom_cords_list=frame1_part_cords_df[frame1_part_cords_df['atom_no'].isin(coplanar_atom_no_list)][['x','y','z']].values[:-1]
  frame2_coplanar_atom_cords_list=frame2_part_cords_df[frame2_part_cords_df['atom_no'].isin(coplanar_atom_no_list)][['x','y','z']].values[:-1]
  frame1_plane=vector.getPlaneNormal(frame1_coplanar_atom_cords_list)
  frame2_plane=vector.getPlaneNormal(frame2_coplanar_atom_cords_list)
  part_rotation=getRPYAngles(frame1_plane,frame2_plane,axis=config.axis)[axis]
  '''
  RPY gives accurate results when vector are perpendicular to the axis of rotation
  RPY gives both positive and negative values
  Following angle calulation will give only positive values 
  frame1_plane[axis]=0
  frame2_plane[axis]=0
  part_rotation=vector.getAngleR(frame1_plane,frame2_plane)
  '''
  return math.degrees(part_rotation)

def rot_mol_plane_3_1(frame1_cords,frame2_cords,part='ring',atom_list=[]):
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
  frame1_cords,frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation')
  frame1_part_cords_df=frame1_cords[frame1_cords['atom_no'].isin(_atom_list)]
  frame2_part_cords_df=frame2_cords[frame2_cords['atom_no'].isin(_atom_list)]
  coplanar_atom_no_list=findCoplanarAtoms(frame1_part_cords_df)
  frame1_coplanar_atom_cords_list=frame1_part_cords_df[frame1_part_cords_df['atom_no'].isin(coplanar_atom_no_list)][['x','y','z']].values[:-1]
  frame2_coplanar_atom_cords_list=frame2_part_cords_df[frame2_part_cords_df['atom_no'].isin(coplanar_atom_no_list)][['x','y','z']].values[:-1]
  frame1_plane=vector.getPlaneNormal(frame1_coplanar_atom_cords_list)
  frame2_plane=vector.getPlaneNormal(frame2_coplanar_atom_cords_list)
  frame1_plane[axis]=0
  frame2_plane[axis]=0
  part_rotation=getRPYAngles(frame1_plane,frame2_plane,axis=config.axis)[axis]
  return math.degrees(part_rotation)

def rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part='ring')
  elif part=='track':
    track_atom_list=config.track_atom_no_list
    ring_atom_list=config.ring_atom_no_list
    trans_axis=[0,0,0]
    cog1=physics.getCog(frame1_cords,atom_list=ring_atom_list)
    cog2=physics.getCog(frame2_cords,atom_list=ring_atom_list)
    trans_axis[0]=cog2[0]-cog1[0]
    trans_axis[1]=cog2[1]-cog1[1]
    trans_axis[2]=cog2[2]-cog1[2] 
    nearest_atom_list=getNearestAtomList(frame1_cords,cog1,trans_axis,config.track_range)
    track_part_atom_list=list(filter(lambda x:x in track_atom_list,nearest_atom_list))
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part='custom',atom_list=track_part_atom_list)
  else:
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part=part,atom_list=atom_list)

def rot_hybrid_1(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    return rot_atomic_r_t_1(frame1_cords,frame2_cords,part='ring')
  elif part=='track':
    return rot_mol_plane_1(frame1_cords,frame2_cords,part='track')
  else:
    return rot_atomic_r_t_1(frame1_cords,frame2_cords,part=part,atom_list=atom_list)

def rot_hybrid_2(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    return rot_atomic_r_t_2(frame1_cords,frame2_cords,part='ring')
  elif part=='track':
    return rot_mol_plane_2(frame1_cords,frame2_cords,part='track')
  else:
    return rot_atomic_r_t_2(frame1_cords,frame2_cords,part=part,atom_list=atom_list)

def rot_hybrid_3(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part='ring')
  elif part=='track':
    return rot_mol_plane_3(frame1_cords,frame2_cords,part='track')
  else:
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part=part,atom_list=atom_list)

def rot_hybrid_3_1(frame1_cords,frame2_cords,part='ring',atom_list=[]):
  if part=='ring':
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part='ring')
  elif part=='track':
    return rot_mol_plane_3_1(frame1_cords,frame2_cords,part='track')
  else:
    return rot_atomic_r_t_3(frame1_cords,frame2_cords,part=part,atom_list=atom_list)

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

def getRPYAngles(v1,v2,axis='x',unit='radians'):
  rpy=np.zeros(3)
  s=vector.getCrossProduct(v1,v2) 
  s=vector.getUnitVec(s)
  theta=vector.getAngleR(v1,v2)
  R=getRotMat(s,theta)
  if axis=='x':
    rpy[1]=asin(fixArcDomain(-1*R[2][0]))
    rpy[0]=asin(fixArcDomain(R[2][1]/cos(rpy[1])))
    rpy[2]=asin(fixArcDomain(R[1][0]/cos(rpy[1])))
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
  if unit=='radians':
    return rpy
  elif unit=='degrees':
    return list(map(math.degrees,rpy))

def findMolecularPlane(df):
  n=5
  first_atom_no=df.iloc[1]['atom_no']
  last_atom_no=df.iloc[-1]['atom_no']
  p1=df[df['atom_no']==first_atom_no][['x','y','z']].values[0]
  p2=df[df['atom_no']==first_atom_no+n][['x','y','z']].values[0]
  p3=df[df['atom_no']==last_atom_no-n][['x','y','z']].values[0]
  p4=df[df['atom_no']==last_atom_no][['x','y','z']].values[0]
  v1=p4-p1
  v2=p3-p2
  return vector.getCrossProduct(v1,v2)
 
def findCoplanarAtoms(df):
  error=0.0174533
  out_atom_no_list=[]
  atom_no_list=df['atom_no'].values
  for atom1_no in atom_no_list:
    for atom2_no in atom_no_list:
      if atom2_no==atom1_no:
        continue
      for atom3_no in atom_no_list:
        if atom3_no==atom1_no or atom3_no==atom2_no:
          continue
        for atom4_no in atom_no_list:
          if atom4_no==atom1_no or atom4_no==atom2_no or atom4_no==atom3_no:
            continue
          p=df[df['atom_no'].isin([atom1_no,atom2_no,atom3_no,atom4_no])][['x','y','z']].values   
          dihedral_angle=vector.getDihedralAngle(p,unit='radians')
          if np.abs(dihedral_angle-math.pi)<error or np.abs(dihedral_angle)<error:
            out_atom_no_list=[atom1_no,atom2_no,atom3_no,atom4_no]
            return out_atom_no_list

def getNearestAtomList(df,point,direction,distance):
  atom_list=[]
  direction=vector.getUnitVec(direction)
  for index,row in df.iterrows():
    p=[0,0,0]
    atom_cords=row[['x','y','z']].values
    p[0]=atom_cords[0]-point[0]
    p[1]=atom_cords[1]-point[1]
    p[2]=atom_cords[2]-point[2]
    projection=vector.getDotProduct(direction,p)
    if isZero(p):
      continue
    if np.abs(round(projection,6))<=distance:
      atom_list.append(row['atom_no'])
  return atom_list

def isZero(l):
  for i in l:
    if round(i,6)!=0:
      return False
  return True

def fixArcDomain(v):
  if v<-1:  
    return -1
  elif v>1:
    return 1
  else:
    return v
