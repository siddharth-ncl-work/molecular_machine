import numpy as np

from lib.basic_operations import physics,vector
import config


def _shiftOrigin(cords,origin):
  new_cords=cords.copy()
  new_cords['x']=new_cords['x']-origin[0]
  new_cords['y']=new_cords['y']-origin[1]
  new_cords['z']=new_cords['z']-origin[2]
  return new_cords

def getAxisAndOrigin(frame1_cords,frame2_cords,process='rotation',axis=None,origin=None,system_type='molecular_machine'):
  if system_type=='molecular_machine':
    _atom_no_list=config.ring_atom_no_list
  else:
    _atom_no_list=frame1_cords['atom_no'].values

  print(_atom_no_list)
  _axis=[0,0,0]
  if (isinstance(axis,list) or isinstance(axis,np.ndarray)) and len(axis)==3:
    _axis=axis
  elif axis=='cog':
      cog1=physics.getCog(frame1_cords,atom_list=_atom_no_list)
      cog2=physics.getCog(frame2_cords,atom_list=_atom_no_list)
      for i in range(3):
        _axis[i]=cog2[i]-cog1[i]
      if isZero(_axis):
        if system_type=='molecular_machine':
          _atom_no_list=config.track_atom_no_list
          cog1=physics.getCog(frame1_cords,atom_list=_atom_no_list)
          cog2=physics.getCog(frame2_cords,atom_list=_atom_no_list)
          for i in range(3):
            _axis[i]=cog2[i]-cog1[i]
          if isZero(_axis):
            _atom_no_list=config.ring_atom_no_list
            cog1=physics.getCog(frame1_cords,atom_list=config.ring_atom_no_list)
            cog2=physics.getCog(frame2_cords,atom_list=config.track_atom_no_list)
            for i in range(3):
              _axis[i]=cog2[i]-cog1[i]
            if isZero(_axis):
              print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
              print('so returning the same coordinates')
              return None
        else:
          print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
          print('so returning the same coordinates')
          return None
  elif axis=='com':
      com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
      com2=physics.getCom(frame2_cords,atom_list=_atom_no_list)
      for i in range(i):
        _axis[i]=com2[i]-com1[i]
      if isZero(_axis):
        if system_type=='molecular_machine':
          _atom_no_list=config.track_atom_no_list
          com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
          com2=physics.getCom(frame2_cords,atom_list=_atom_no_list)
          for i in range(3):
            _axis[i]=com2[i]-com1[i]
          if isZero(_axis):
            _atom_no_list=config.ring_atom_no_list
            com1=physics.getCom(frame1_cords,atom_list=config.ring_atom_no_list)
            com2=physics.getCom(frame2_cords,atom_list=config.track_atom_no_list)
            for i in range(3):
              _axis[i]=com2[i]-com1[i]
            if isZero(_axis):
              print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
              print('so returning the same coordinates')
              return None
        else:
          print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
          print('so returning the same coordinates')
          return None
  elif type(axis)==type(None):
    print('determining axis...')
    if process=='rotation' or 'translation':
      print('making ring cog as axis')
      cog1=physics.getCog(frame1_cords,atom_list=_atom_no_list)
      cog2=physics.getCog(frame2_cords,atom_list=_atom_no_list)
      for i in range(3):
        _axis[i]=cog2[i]-cog1[i]
      if isZero(_axis):
        print('changing rotation axis to track cog')
        if system_type=='molecular_machine':
          _atom_no_list=config.track_atom_no_list
          cog1=physics.getCog(frame1_cords,atom_list=_atom_no_list)
          cog2=physics.getCog(frame2_cords,atom_list=_atom_no_list)
          for i in range(3):
            _axis[i]=0#cog2[i]-cog1[i]
          if isZero(_axis):
            print('changing rotation axis to ring track cog')
            _atom_no_list=config.ring_atom_no_list
            cog1=physics.getCog(frame1_cords,atom_list=config.ring_atom_no_list)
            cog2=physics.getCog(frame2_cords,atom_list=config.track_atom_no_list)
            for i in range(3):
              _axis[i]=cog2[i]-cog1[i]
            if isZero(_axis):
              print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
              print('so returning the same coordinates')
              return None 
        elif system_type=='ring':
          print('assuming its pure rotation determining axis using cross product')
          atom_no=np.random.choice(_atom_no_list)
          cords1=frame1_cords[frame1_cords['atom_no']==atom_no][['x','y','z']].values[0]
          cords2=frame2_cords[frame2_cords['atom_no']==atom_no][['x','y','z']].values[0]
          _axis=vector.getCrossProduct(cords2,cords1)
          if isZero(_axis):
            print('no rotation or translation, identical\nany axis should give zero value')
            _axis=[1,0,0] 
        else:
          print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
          print('so returning the same coordinates')
          return None
    elif process=='translation':
      com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
      com2=physics.getCom(frame2_cords,atom_list=_atom_no_list)
      for i in range(3):
        _axis[i]=com2[i]-com1[i]
      if isZero(_axis):
        print('Changing to track com axis')
        if system_type=='molecular_machine':
          _atom_no_list=config.track_atom_no_list
          com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
          com2=physics.getCom(frame2_cords,atom_list=_atom_no_list)
          for i in range(3):
            _axis[i]=com2[i]-com1[i]
          if isZero(_axis):
            _atom_no_list=config.ring_atom_no_list
            com1=physics.getCom(frame1_cords,atom_list=config.ring_atom_no_list)
            com2=physics.getCom(frame2_cords,atom_list=config.track_atom_no_list)
            for i in range(3):
              _axis[i]=com2[i]-com1[i]
            if isZero(_axis):
              print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
              print('so returning the same coordinates')
              return None
        else:
          print(f'_axis = {_axis}, Do not know other way to determine axis for {system}')
          print('so returning the same coordinates')
          return None
  else:
    print(f'shiftOrigin: axis_argument = {axis}, cannont determine the axis')  

  
  com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
  com2=physics.getCom(frame2_cords,atom_list=_atom_no_list)
  sign= 1 if com2[0]-com1[0]>=0 else -1
  for i in range(3):
    _axis[i]*=sign
  print(f'shift_origin axis={_axis}')


  if system_type=='molecular_machine':
    _atom_no_list=config.ring_atom_no_list
  else:
    _atom_no_list=frame1_cords['atom_no'].values

  _origin=None
  if (isinstance(origin,list) or isinstance(origin,np.ndarray)) and len(origin)==3:
    _origin=origin
  elif origin=='cog':
      cog1=physics.getCog(frame1_cords,atom_list=_atom_no_list)
      _origin=cog1
  elif axis=='com':
      com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
      _origin=com1
  elif type(origin)==type(None):
    print('determining origin...')
    if process=='rotation' or 'translation':
      cog1=physics.getCog(frame1_cords,atom_list=_atom_no_list)
      _origin=cog1
    elif process=='translation':
      com1=physics.getCom(frame1_cords,atom_list=_atom_no_list)
      _origin=com1
  else:
    print(f'argument origin = {origin}, cannont determine the origin')
  print(f'shift_origin origin={_origin}')

  return _axis,_origin

def isZero(l):
  for i in l:
    if round(i,6)!=0:
      return False
  return True

def shiftOrigin(frame1_cords,frame2_cords,process='rotation',axis=None,origin=None,system_type='molecular_machine',ref_axis_alignment=True): 
  '''
  axis: is required for rotation as well as translation
        if axis is not given then it assumed to be COG/COM axis

  origin: is required only for rotation
          if origin is not given it is assumed to be COG/COM of the first frame
  '''
  _axis,_origin=getAxisAndOrigin(frame1_cords,frame2_cords,process='rotation',axis=None,origin=None,system_type=system_type)
  if type(_axis)==type(None):
    return (frame1_cords,frame2_cords)

  assert not isZero(_axis),'shiftOrigin: _axis is zero even after this, what the ..'

  new_frame1_cords=_shiftOrigin(frame1_cords,_origin)
  new_frame2_cords=_shiftOrigin(frame2_cords,_origin)  
  if config.axis=='x':
    ax=[1,0,0]
  elif config.axis=='y':
    ax=[0,1,0]
  elif config.axis=='z':
    ax=[0,0,1]
  temp_axis=vector.getCrossProduct(_axis,ax)
  theta=vector.getAngleR(_axis,ax)
  new_frame1_cords=physics.rotateAlongAxis(new_frame1_cords,temp_axis,theta)
  new_frame2_cords=physics.rotateAlongAxis(new_frame2_cords,temp_axis,theta)

  #REFERENCE AXIS ALIGNMENT
  if ref_axis_alignment:
    whole_frame_com=physics.getCom(new_frame1_cords) 
    if config.axis=='x':
      ref_axis=[0,1,1]
      whole_frame_com[0]=0
    elif config.axis=='y':
      ref_axis=[1,0,1]
      whole_frame_com[1]=0
    elif config.axis=='z':
      ref_axis=[1,1,0]
      whole_frame_com[2]=0
    temp_axis=vector.getUnitVec(vector.getCrossProduct(whole_frame_com,ref_axis))
    assert not isZero(temp_axis),'ShiftOrigin:Error during reference axis alignment, cannont determine rotation axis'
    theta=vector.getAngleR(whole_frame_com,ref_axis)
    new_frame1_cords=physics.rotateAlongAxis(new_frame1_cords,temp_axis,theta)
    new_frame2_cords=physics.rotateAlongAxis(new_frame2_cords,temp_axis,theta)
  
  return (new_frame1_cords,new_frame2_cords)
