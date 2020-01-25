import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pickle
import sys
sys.path.extend(['.','..'])
import subprocess

from source import rotation
import make_test_systems


def init(method):
  subprocess.run(['mkdir',f'assessment_{method}'],cwd='output')
  subprocess.run(['mkdir','artificial_test_system','semi_real_test_system'],cwd=f'output/assessment_{method}')
  subprocess.run(['mkdir','ring','track'],cwd=f'output/assessment_{method}/artificial_test_system')
  subprocess.run(['mkdir','ring/single_axis_test','ring/double_axis_test'],cwd=f'output/assessment_{method}/artificial_test_system')
  subprocess.run(['mkdir','track/single_axis_test','track/double_axis_test'],cwd=f'output/assessment_{method}/artificial_test_system')
  subprocess.run(['mkdir','ring','track'],cwd=f'output/assessment_{method}/semi_real_test_systems')
  subprocess.run(['mkdir','ring/single_axis_test','ring/double_axis_test'],cwd=f'output/assessment_{method}/semi_real_test_system')
  subprocess.run(['mkdir','track/single_axis_test','track/double_axis_test'],cwd=f'output/assessment_{method}/semi_real_test_system')

def assessRotationMethodSingleAxis(method='rot_hybrid_3',step_size=10,syste='',parts=['ring','track']):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    for axis in range(3):
      rpy=[0,0,0]
      x=[]
      y=[]
      for theta in range(-360,361,step_size):
        rpy[axis]=theta
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_non_ideal_semi_real_system.xyz'
        with open(file_path,'r') as file:
          _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        x.append(theta)
        y.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method}')
      plot1(x,y,method=method,part=part,axis=axis,assessment_type='single_axis')

def assessRotationMethodDoubleAxis2d(method='rot_atomic_r_t',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=10,parts=['ring','track']):
  assert rotation_axis!=constant_axis,'Rotation axis should not be same constant axis'
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    rpy=[0,0,0]
    rpy[constant_axis]=constant_theta
    x=[]
    y=[]
    for theta in range(-360,361,step_size):
      rpy[rotation_axis]=theta
      if part=='ring':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
      elif part=='track':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
      if system=='artificial':
        file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
      elif system=='semi_real':
        file_path='test_systems/ring_track_two_frames_non_ideal_semi_real_system'
      with open(file_path,'r') as file:
        _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
      x.append(theta)
      y.append(_rotation)
      print(f'{rpy},{part} Absolute Rotation = {_rotation},{method}')
    plot2(x,y,method=method,part=part,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_theta=constant_theta,assessment_type='double_axis')

def assessRotationMethodDoubleAxis3d(method='rot_atomic_r_t',axis=1,step_size=120,parts=['ring','track']):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    X=[]
    Y=[]
    Z_expected=[]
    Z_predicted=[]
    for theta_axis in range(-100,101,step_size):
      rpy=[0,0,0]
      rpy[axis]=theta_axis
      x=[]
      theta_axis_list=[]
      z_expected=[]
      z_predicted=[]
      for theta_x in range(-100,101,step_size):
        rpy[0]=theta_x
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_non_ideal_semi_real_system'
        with open(file_path,'r') as file:
          _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        x.append(theta_x)
        theta_axis_list.append(theta_axis)
        z_expected.append(theta_x)
        z_predicted.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method}')
      X.append(x)
      Y.append(theta_axis_list)
      Z_expected.append(z_expected)
      Z_predicted.append(z_predicted)
    plot3(X,Y,np.array(Z_expected),np.array(Z_predicted),method=method,part=part,axis=axis,assessment_type='double_axis')

def _tripleAxis(method='rot_atomic_r_t',rotation_axis=1,constant_axis=1,constant_axis_theta=0,step_size=120,parts=['ring','track']):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    X=[]
    Y=[]
    Z_expected=[]
    Z_predicted=[]
    for rotation_axis_theta in range(-100,101,step_size):
      rpy=[0,0,0]
      rpy[rotation_axis]=rotation_axis_theta
      rpy[constant_axis]=constant_axis_theta
      x=[]
      rotation_axis_theta_list=[]
      z_expected=[]
      z_predicted=[]
      for theta_x in range(-100,101,step_size):
        rpy[0]=theta_x
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesNonIdealSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_non_ideal_semi_real_system'
        with open(file_path,'r') as file:
          _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        x.append(theta_x)
        rotation_axis_theta_list.append(rotation_axis_theta)
        z_expected.append(theta_x)
        z_predicted.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method}')
      X.append(x)
      Y.append(theta_axis_list)
      Z_expected.append(z_expected)
      Z_predicted.append(z_predicted)
    plot3(X,Y,np.array(Z_expected),np.array(Z_predicted),method=method,part=part,axis=axis,assessment_type='double_axis')

def assessRotationMethodTripleAxis3d(method='rot_atomic_r_t',rotation_axis=1,constant_axis=1,constant_axis_theta_range=[],step_size=120,parts=['ring','track']):
  for constant_axis_theta in constant_axis_theta_range:
    _tripleAxis(method=method,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_axis_theta=constant_axis_theta,step_size=step_size,parts=parts):

def plot1(x,y,method='test',part='ring',axis=0,assessment_type='',system=''):
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y)
  if axis=='x':
    plt.plot(x,x)
  else:
    zero=np.zeros(len(x))
    plt.plot(x,zero)
  title=method.upper()+'('+part+','+axis+','+assessment_type+','+system')'
  plt.title(title)
  plt.xlabel(f'{axis} Rotation(D)')
  plt.ylabel('Predicted X Rotation (D)')
  plt.ylim(-360, 360)
  plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  plt.show()
 
def plot2(x,y,method='test',part='ring',rotation_axis=0,constant_axis=1,constant_theta=10,assessment_type='',system=''):
  if rotation_axis==0:
    rotation_axis='x'
  elif rotation_axis==1:
    rotation_axis='y'
  elif rotation_axis==2:
    rotation_axis='z'
  if constant_axis==0:
    constant_axis='x'
  elif constant_axis==1:
    constant_axis='y'
  elif constant_axis==2:
    constant_axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y)
  if rotation_axis=='x':
    plt.plot(x,x)
  else:
    zero=np.zeros(len(x))
    plt.plot(x,zero)
  title=method.upper()+'('+part+','+rotation_axis+','+constant_axis+'='+str(constant_theta)+','+assessment_type+','+system+')'
  plt.title(title)
  plt.xlabel(f'{rotation_axis} Rotation(D)')
  plt.ylabel('Predicted X Rotation(D)')
  plt.ylim(-360, 360)
  plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  plt.show()

def plot3(X,Y,Z_expected,Z_predicted,method='rot_atomic_r_t',part='',axis=0,assessment_type='',system=''):
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  data={'X':X,'Y':Y,'Z_expected':Z,'Z_predicted':Z_predicted}
  pickle.dump(data,open('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.dat.pkl', 'wb')
   
  title=method.upper()+'('+part+',x,'+axis+','+assessment_type+','+system')'
  for ele in [-60,60]:
    for azm in range(361,45):
      fig=plt.figure()
      ax=plt.axes(projection="3d")
      ax.plot_surface(X,Y,Z_expected,cmap='Reds',edgecolor='none')
      ax.plot_surface(X,Y,Z_predicted,cmap='winter',edgecolor='none')
      ax.set_title(title)
      ax.set_xlabel('X Rotation')
      ax.set_ylabel(f'{axis} Rotation')
      ax.set_zlabel('Expcted/Predicted X Rotation')
      ax.view_init(ele,azm)
      plt.save('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  plt.show()



if __name__='__main__':
  system_list=['artificial','semi_real']
  method_list=['rot_part_atomic_r_t_3']
  system_list=['artificial','semi_real']
  step_size=5
  parts=['ring','track']
  for system in system_list:
    for method in method_list:
      init('test_method')
      assessRotationMethodSingleAxis(method=method,step_size=step_size,system=system)
      assessRotationMethodDoubleAxis2d(method=method,step_size=step_size,rotation_axis=0,constant_axis=1,constant_theta=45,system=system)
      assessRotationMethodDoubleAxis2d(method=method,step_size=5,rotation_axis=0,constant_axis=1,constant_theta=-45,system=system)
      assessRotationMethodDoubleAxis3d(method=method,axis=1,step_size=step_size,parts=parts)
      assessRotationMethodDoubleAxis3d(method=method,axis=2,step_size=step_size,parts=parts)
      assessRotationMethodTripleAxis3d(method=method,rotation_axis=1,constant_axis=2,constant_axis_theta_range=[-10,10],step_size=step_size,parts=parts):
