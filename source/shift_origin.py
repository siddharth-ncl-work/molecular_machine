from lib.basic_operations import physics,vector
import config


def _shiftOrigin(cords,origin):
  new_cords=cords.copy()
  new_cords['x']=new_cords['x']-origin[0]
  new_cords['y']=new_cords['y']-origin[1]
  new_cords['z']=new_cords['z']-origin[2]

  return new_cords

def shiftOrigin(frame1_cords,frame2_cords,process='rotation'):
  atom_list=range(config.ring_start_atom_no,config.ring_end_atom_no+1) 
  trans_axis=[0.0,0.0,0.0] 
  if process=='rotation':
    cog1=physics.getCog(frame1_cords,atom_list=atom_list)
    cog2=physics.getCog(frame2_cords,atom_list=atom_list)
    trans_axis[0]=cog2[0]-cog1[0]
    trans_axis[1]=cog2[1]-cog1[1]
    trans_axis[2]=cog2[2]-cog1[2]
    new_frame1_cords=_shiftOrigin(frame1_cords,cog1)
    new_frame2_cords=_shiftOrigin(frame2_cords,cog2)
  elif process=='translation':
    com1=physics.getCom(frame1_cords,atom_list=atom_list)
    com2=physics.getCom(frame2_cords,atom_list=atom_list)
    trans_axis[0]=com2[0]-com1[0]
    trans_axis[1]=com2[1]-com1[1]
    trans_axis[2]=com2[2]-com1[2]
    new_frame1_cords=_shiftOrigin(frame1_cords,com1)
    new_frame2_cords=_shiftOrigin(frame2_cords,com1)
  if config.axis=='x':
    ax=[1,0,0]
  elif config.axis=='y':
    ax=[0,1,0]
  elif config.axis=='z':
    ax=[0,0,1]
  axis=vector.getCrossProduct(trans_axis,ax)
  theta=vector.getAngleR(trans_axis,ax)
  
  new_frame1_cords=physics.rotateAlongAxis(new_frame1_cords,axis,theta)
  new_frame2_cords=physics.rotateAlongAxis(new_frame2_cords,axis,theta)
  
  cog=physics.getCog(new_frame1_cords) 
  if config.axis=='x':
    ref_axis=[0,1,1]
    cog[0]=0
  elif config.axis=='y':
    ref_axis=[1,0,1]
    cog[1]=0
  elif config.axis=='z':
    ref_axis=[1,1,0]
    cog[2]=0
  #axis=vector.getCrossProduct(com,ref_axis)
  theta=vector.getAngleR(axis,ax)

  new_frame1_cords=physics.rotateAlongAxis(new_frame1_cords,ax,theta)
  new_frame2_cords=physics.rotateAlongAxis(new_frame2_cords,ax,theta)

  return (new_frame1_cords,new_frame2_cords)
