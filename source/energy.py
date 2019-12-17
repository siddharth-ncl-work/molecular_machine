import sys

sys.path.extend(['..'])

from source import rotation,translation
from lib.io_chem import io
from lib.basic_operations import vector,physics,atomic_mass
import config

def getAvgRKE(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='energy_rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  avg_RKE=0
  net_RKE=0
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=2)
  for curr_frame_no in range(start_frame_no+1,end_frame_no+1,step_size):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=2)
    RKE=_getRKE(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_RKE+=RKE
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
  avg_RKE=net_RKE/len(range(start_frame_no,end_frame_no+1,step_size))
  return avg_RKE

def getRKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='energy_rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=2)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=2)
  return _getRKE(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getRKE(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',method='energy_rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  RKE=0 
  if method=='energy_rot_atomic_angle':
    RKE=energy_rot_atomic_angle(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_rot_atomic_r_t':
    RKE=energy_rot_atomic_r_t(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  else:
    print('Please give an appropriate method')
  return RKE
   
def energy_rot_atomic_angle(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list

  if type=='absolute':    
    for atom_no in _part1_atom_list:
      frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
      frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]
      atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0]
      theta=vector.getAngleR(frame1_atom_cords,frame2_atom_cords)
      omega=theta/(config.simulation_time_step*config.femto)
      atom_RKE=0.5*physics.getMI(frame1_atom_cords,atom_type)*pow(omega,2)
      RKE+=atom_RKE
  elif type=='relative':
    print('This method does not support relative energy')
    pass

  return RKE

def energy_rot_atomic_r_t(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list

  if type=='absolute':
    theta=rotation.rot_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    omega=theta/(config.simulation_time_step*config.femto)
    MI=0
    if config.axis=='x':
      ax=[1,0,0]
    elif config.axis=='y':
      ax=[0,1,0]
    elif config.axis=='z':
      ax=[0,0,1]
    mass_list=[]
    distance_list=[]
    for atom_no in _part1_atom_list:
      atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
      atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
      distance=vector.get_dist_pt_line(atom_cords,ax)
      mass=atomic_mass.atomic_mass_dict[atom_type]
      mass_list.append(mass)
      distance_list.append(distance)
    MI=physics._getMI(mass_list,distance_list)
    RKE=0.5*MI*pow(omega,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list

    part1_theta=rotation.rot_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_theta=rotation.rot_atomic_r_t(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    theta=part1_theta-part2_theta
    omega=theta/(config.simulation_time_step*config.femto)
    MI=0
    if config.axis=='x':
      ax=[1,0,0]
    elif config.axis=='y':
      ax=[0,1,0]
    elif config.axis=='z':
      ax=[0,0,1]
    mass_list=[]
    distance_list=[]
    for atom_no in _part1_atom_list:
      atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
      atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
      distance=vector.get_dist_pt_line(atom_cords,ax)
      mass=atomic_mass.atomic_mass_dict[atom_type]
      mass_list.append(mass)
      distance_list.append(distance)
    MI=physics._getMI(mass_list,distance_list)
    RKE=0.5*MI*pow(omega,2)
  return RKE

#Translational Energy
def getAvgTKE(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='energy_trans_com',part1_atom_list=[],part2_atom_list=[]):
  avg_TKE=0
  net_TKE=0
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=2)
  for curr_frame_no in range(start_frame_no+1,end_frame_no+1,step_size):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=2)
    TKE=_getTKE(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_TKE+=TKE
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
  avg_TKE=net_TKE/len(range(start_frame_no,end_frame_no+1,step_size))
  return avg_TKE

def getTKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='energy_trans_com',part1_atom_list=[],part2_atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=2)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=2)
  return _getTKE(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getTKE(frame1_cords,frame2_cords,part1='ring',part2='track',type='abs',method='energy_trans_com',part1_atom_list=[],part2_atom_list=[]):
  TKE=0
  if method=='energy_trans_atomic_r_t':
    TKE=energy_trans_atomic_r_t(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_trans_com':
    TKE=energy_trans_com(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  else:
    print('Please give an appropriate method')
  return TKE

def energy_trans_atomic_r_t(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):

  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list

  if type=='absolute':
    _translation=translation.trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    v=_translation/(config.simulation_time_step*config.femto)
    m=getTotalMass(frame1_cords,atom_list=_part1_atom_list)
    TKE=0.5*m*pow(v,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_translation=translation.trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_translation=translation.trans_atomic_r_t(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    _translation=part2_translation-part1_translation
    v=_translation/(config.simulation_time_step*config.femto)
    m=getTotalMass(frame1_cords,atom_list=_part1_atom_list)
    TKE=0.5*m*pow(v,2)
  return TKE

def energy_trans_com(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  TKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list

  if type=='absolute':
    _translation=translation.trans_com(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    v=_translation/(config.simulation_time_step*config.femto)
    m=getTotalMass(frame1_cords,atom_list=_part1_atom_list)
    TKE=0.5*m*pow(v,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_translation=translation.trans_com(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_translation=translation.trans_com(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    _translation=part2_translation-part1_translation
    v=_translation/(config.simulation_time_step*config.femto)
    m=getTotalMass(frame1_cords,atom_list=_part1_atom_list)
    TKE=0.5*m*pow(v,2)
  return TKE
 
def getTotalMass(cords,atom_list=None):
  total_mass=0
  if atom_list==None:
    atom_list=list(cords['atom_no'].values)
  for atom_no in atom_list:
    mass=atomic_mass.atomic_mass_dict[cords[cords['atom_no']==atom_no]['atom'].values[0].lower()]
    total_mass+=mass
  return total_mass*config.amu

