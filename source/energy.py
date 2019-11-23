import sys

sys.path.extend(['..'])

from lib.io_chem import io
from lib.basic_operations import vector,physics
from bin import config

def getNetRKE(file,start_frame_no,end_frame_no,part='ring',step_size=1,method='atom_axis',atom_list=[]):
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=2)
  for curr_frame_no in range(start_frame_no+1,end_frame_no+1,step_size):
    curr_frame_cords=io.readFileMd(file,curr_frame_no)
    part_RKE=_getRKE(prev_frame_cords,curr_frame_cords,part=part,method=method,atom_list=[])

    net_part_RKE+=part_RKE
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()
  return net_part_RKE

def getRKE(file,frame1_no,frame2_no,part='ring',method='atom_axis',atom_list=[]):
  assert frame2_no>=frame1_no,'Invalid Frame Numbers'
  frame1_cords=io.readFileMd(file,frame1_cords,frame_no_pos=2)
  frame2_cords=io.readFileMd(file,frame2_cords,frame_no_pos=2)
  return _getRKE(frame1_cords,frame2_cords,part=part,method=method,atom_list=atom_list)

def _getRKE(frame1_cords,frame2_cords,part='ring',method='atom_axis',atom_list=[]):
  part_RKE=0
  if part=='ring':
    _atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1)
  elif part=='track':
    _atom_list=range(config.track_start_atom_no,config.track_end_atom_no+1)
  elif part=='whole':
    _atom_list=io.readFileMd(file,0,'atoms')
  else:
    assert len(atom_list)!=0,'atoms_list should not be empty'
    _atom_list=atom_list
       
  for atom_no in _atom_list:
    frame1_atom_cords=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values
    frame2_atom_cords=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values
    atom_type=frame1_cords[frame1_cords['atom_no']==atom_noc]['atom'].values[0]
    if method=='atom_axis':
      atom_RKE=getAtomRKE(frame1_atom_cords,frame2_atom_cords,atom_type)
    elif method=='com_axis':
      pass
    elif method=='r+t':
      pass
    elif method=='t+r':
      pass
    else:
      print('Please specify valid method')
    part_RKE+=atom_RKE
  return part_RKE

def getAtomRKE(atom_cords1,atom_cords2,atom_type):
  theta=vector.getAngleR(atom_cords1,atom_cords2)
  omega=theta/(config.simulation_time_step*config.femto)
  RKE=0.5*physics.getMI(atom_cords,atom_type)*pow(omega,2)
  return RKE


