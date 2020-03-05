import math
from tqdm import tqdm

from lib.io_chem import io
from lib.basic_operations import vector,physics,constants,atomic_mass
from source import rotation,translation
import config


#Rotational Energy
def getAvgRKE(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='energy_rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  avg_RKE=0
  net_RKE=0
  data={'frame_no':[],'RKE':[],f'ring_{type}_rotation':[]}
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=config.frame_no_pos)
  for curr_frame_no in tqdm(range(start_frame_no+step_size,end_frame_no+1,step_size)):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=config.frame_no_pos)
    RKE,rotation=_getRKE(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_RKE+=RKE
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
    data['frame_no'].append(curr_frame_no)
    data['RKE'].append(RKE)
    data[f'ring_{type}_rotation'].append(rotation)
  avg_RKE=net_RKE/len(range(start_frame_no,end_frame_no+1,step_size))
  return (avg_RKE,data)

def getRKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='energy_rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  return _getRKE(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getRKE(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',method='energy_rot_atomic_r_t',part1_atom_list=[],part2_atom_list=[]):
  RKE=0 
  if method=='energy_rot_atomic_r_t':
    RKE=energy_rot_atomic_r_t(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_rot_atomic_angle':
    RKE=energy_rot_atomic_angle(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_rot_hybrid_1':
    RKE=energy_rot_hybrid_1(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_rot_part_atomic_r_t_3':
    RKE,rotation=energy_rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_rot_atomic_t_r':
    print('to be implemented')
  else:
    print('Please provide an appropriate method')
  return (RKE,rotation)
   
def energy_rot_atomic_r_t(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  mass_list=[]
  cords_list=[]
  for atom_no in _part1_atom_list:
    atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
    mass=atomic_mass.atomic_mass_dict[atom_type]
    mass_list.append(mass)
    cords_list.append(atom_cords)
  MI=physics._getMI(cords_list,mass_list,axis)
  if type=='absolute':
    theta=rotation.rot_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
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
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*config.femto)
    RKE=0.5*MI*pow(omega,2)
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
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  if type=='absolute':    
    for atom_no in _part1_atom_list:
      frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
      frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]
      atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0]
      theta=vector.getAngleR(frame1_atom_cords,frame2_atom_cords)
      theta=math.radians(theta)
      omega=theta/(config.simulation_time_step*config.femto)
      MI=physics.getMI(frame1_atom_cords,atom_type,axis)
      atom_RKE=0.5*MI*pow(omega,2)
      RKE+=atom_RKE
  elif type=='relative':
    print('This method does not support relative energy')
    pass
  return RKE

def energy_rot_hybrid_1(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  mass_list=[]
  cords_list=[]
  for atom_no in _part1_atom_list:
    atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
    mass=atomic_mass.atomic_mass_dict[atom_type]
    mass_list.append(mass)
    cords_list.append(atom_cords)
  MI=physics._getMI(cords_list,mass_list,axis)
  if type=='absolute':
    theta=rotation.rot_hybrid_1(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_theta=rotation.rot_hybrid_1(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_theta=rotation.rot_hybrid_1(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    theta=part1_theta-part2_theta
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  return RKE

def energy_rot_hybrid_2(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  mass_list=[]
  cords_list=[]
  for atom_no in _part1_atom_list:
    atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
    mass=atomic_mass.atomic_mass_dict[atom_type]
    mass_list.append(mass)
    cords_list.append(atom_cords)
  MI=physics._getMI(cords_list,mass_list,axis)
  if type=='absolute':
    theta=rotation.rot_hybrid_2(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_theta=rotation.rot_hybrid_2(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_theta=rotation.rot_hybrid_2(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    theta=part1_theta-part2_theta
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  return RKE

def energy_rot_hybrid_3(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  mass_list=[]
  cords_list=[]
  for atom_no in _part1_atom_list:
    atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
    mass=atomic_mass.atomic_mass_dict[atom_type]
    mass_list.append(mass)
    cords_list.append(atom_cords)
  MI=physics._getMI(cords_list,mass_list,axis)
  if type=='absolute':
    theta=rotation.rot_hybrid_3(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_theta=rotation.rot_hybrid_3(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_theta=rotation.rot_hybrid_3(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    theta=part1_theta-part2_theta
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  return RKE

def energy_rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  RKE=0
  if part1=='ring':
    _part1_atom_list=config.ring_atom_no_list
  elif part1=='track':
    _part1_atom_list=config.track_atom_no_list
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  if config.axis=='x':
    axis=[1,0,0]
  elif config.axis=='y':
    axis=[0,1,0]
  elif config.axis=='z':
    axis=[0,0,1]
  mass_list=[]
  cords_list=[]
  for atom_no in _part1_atom_list:
    atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
    atom_type=frame1_cords[frame1_cords['atom_no']==atom_no]['atom'].values[0].lower()
    mass=atomic_mass.atomic_mass_dict[atom_type]
    mass_list.append(mass)
    cords_list.append(atom_cords)
  MI=physics._getMI(cords_list,mass_list,axis)
  if type=='absolute':
    theta=rotation.rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    theta=math.radians(theta)
    omega=theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=config.ring_atom_no_list
    elif part2=='track':
      _part2_atom_list=config.track_atom_no_list
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_theta=rotation.rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_theta=rotation.rot_part_atomic_r_t_3(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    theta=part1_theta-part2_theta
    _theta=math.radians(theta)
    omega=_theta/(config.simulation_time_step*constants.femto)
    RKE=0.5*MI*pow(omega,2)
  return (RKE,theta)

#Translational Energy
def getAvgTKE(file,start_frame_no,end_frame_no,step_size=1,part1='ring',part2='track',type='absolute',method='energy_trans_com',part1_atom_list=[],part2_atom_list=[]):
  avg_TKE=0
  net_TKE=0
  data={'frame_no':[],'TKE':[],f'ring_{type}_translation':[]}
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=config.frame_no_pos)
  for curr_frame_no in tqdm(range(start_frame_no+step_size,end_frame_no+1,step_size)):
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=config.frame_no_pos)
    TKE,_translation=_getTKE(prev_frame_cords,curr_frame_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
    net_TKE+=TKE
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
    data['frame_no'].append(curr_frame_no)
    data['TKE'].append(TKE)
    data[f'ring_{type}_translation'].append(_translation)
  avg_TKE=net_TKE/len(range(start_frame_no,end_frame_no+1,step_size))
  return (avg_TKE,data)

def getTKE(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method='energy_trans_com',part1_atom_list=[],part2_atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)
  return _getTKE(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,method=method,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)

def _getTKE(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',method='energy_trans_com',part1_atom_list=[],part2_atom_list=[]):
  TKE=0
  if method=='energy_trans_atomic_r_t':
    TKE=energy_trans_atomic_r_t(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_trans_com':
    TKE=energy_trans_com(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_trans_com_2':
    TKE,_translation=energy_trans_com_2(frame1_cords,frame2_cords,part1=part1,part2=part2,type=type,part1_atom_list=part1_atom_list,part2_atom_list=part2_atom_list)
  elif method=='energy_trans_atomic_t_r':
    print('to be implemented')
  else:
    print('Please give an appropriate method')
  return (TKE,_translation)

def energy_trans_atomic_r_t(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  TKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  if type=='absolute':
    _translation=translation.trans_atomic_r_t(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    v=_translation/(config.simulation_time_step*constants.femto)
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
    m=physics.getTotalMass(frame1_cords,atom_list=_part1_atom_list)
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
  m=physics.getTotalMass(frame1_cords,atom_list=_part1_atom_list)
  if type=='absolute':
    _translation=translation.trans_com(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    v=_translation/(config.simulation_time_step*constants.femto)
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
    _translation=part1_translation-part2_translation
    v=_translation/(config.simulation_time_step*constants.femto)
    TKE=0.5*m*pow(v,2)
  return TKE

def energy_trans_com_2(frame1_cords,frame2_cords,part1='ring',part2='track',type='absolute',part1_atom_list=[],part2_atom_list=[]):
  TKE=0
  if part1=='ring':
    _part1_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part1=='track':
    _part1_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  else:
    assert len(part1_atom_list)!=0,'atoms_list should not be empty'
    _part1_atom_list=part1_atom_list
  m=physics.getTotalMass(frame1_cords,atom_list=_part1_atom_list)
  if type=='absolute':
    _translation=translation.trans_com_2(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    v=_translation/(config.simulation_time_step*constants.femto)
    TKE=0.5*m*pow(v,2)
  elif type=='relative':
    if part2=='ring':
      _part2_atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
    elif part2=='track':
      _part2_atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
    else:
      assert len(part2_atom_list)!=0,'atoms_list should not be empty'
      _part2_atom_list=part2_atom_list
    part1_translation=translation.trans_com_2(frame1_cords,frame2_cords,part=part1,atom_list=_part1_atom_list)
    part2_translation=translation.trans_com_2(frame1_cords,frame2_cords,part=part2,atom_list=_part2_atom_list)
    _translation=part1_translation-part2_translation
    v=_translation/(config.simulation_time_step*constants.femto)
    TKE=0.5*m*pow(v,2)
  return TKE,_translation
