from lib.basic_operations import physics,vector
import rotation
import config

def shiftOrigin(frame1_cords,frame2_cords):
  atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1) 
  com1=physics.getCom(frame1_cords,atom_list=atom_list) 
  com2=physics.getCom(frame2_cords,atom_list=atom_list)
  origin=com1
  trans_axis=[0.0,0.0,0.0]
  trans_axis[0]=com2[0]-com1[0]
  trans_axis[1]=com2[1]-com1[1]
  trans_axis[2]=com2[2]-com1[2]

  new_frame1_cords=_shiftOrigin(frame1_cords,origin)
  new_frame2_cords=_shitfOrigin(frame2_cords,origin)

  if config.axis='x':
    ax=[1,0,0]
  elif config.axis='y':
    ax=[0,1,0]
  elif config.axis='z':
    ax=[0,0,1]
  axis=vector.getCrossProduct(trans_axis,ax)
  theta=vector.getAngleR(trans_axis,ax)
  
  new_frame1_cords=rotation.rotateAlongAxis(new_frame1_cords,axis,theta)
  new_frame2_cords=rotation.rotateAlongAxis(new_frame2_cords,axis,theta)
  
  if config.axis='x':
    ax=[0,1,1]
  elif config.axis='y':
    ax=[1,0,1]
  elif config.axis='z':
    ax=[1,1,0]
  com=physics.getCom(new_frame1_cords)
  axis=vector.getCrossProduct(com,ax)
  theta=vector.getAngleR(axis,ax)

  new_frame1_cords=rotation.rotateAlongAxis(new_frame1_cords,axis,theta)
  new_frame2_cords=rotation.rotateAlongAxis(new_frame2_cords,axis,theta)

  return (new_frame1_cords,new_frame2_cords)  

def _shiftOrigin(cords,origin):
  new_cords=cords.copy()
  new_cords['x']=new_cords['x']-origin[0]
  new_cords['y']=new_cords['y']-origin[1]
  new_cords['z']=new_cords['z']-origin[2]
  
  return new_cords


