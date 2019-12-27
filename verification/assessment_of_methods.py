import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from source import rotation
import make_test_systems


def assessRotationMethodSingleAxis(method='rot_atomic_r_t',step_size=10):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in ['ring','track']:
    for axis in range(3):
      rpy=[0,0,0]
      x=[]
      y=[]
      for theta in range(-360,360,step_size):
        rpy[axis]=theta
        if part=='ring':
          make_test_systems.ringTrackTwoFramesNonIdeal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          make_test_systems.ringTrackTwoFramesNonIdeal(ring_rpy=zero_rpy,track_rpy=rpy)
        file_path='test_systems/ring_track_two_frames_non_ideal.xyz'
        file=open(file_path,'r')
        _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        file.close()
        x.append(theta)
        y.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method}')
      plot1(x,y,method=method,part=part,axis=axis,assessment_type='single_axis')

def assessRotationMethodDoubleAxis(method='rot_atomic_r_t',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=10):
  assert rotation_axis!=constant_axis,'Rotation axis should not be same constant axis'
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in ['ring','track']:
      rpy=[0,0,0]
      rpy[constant_axis]=constant_theta
      x=[]
      y=[]
      for theta in range(-360,360,step_size):
        rpy[rotation_axis]=theta
        if part=='ring':
          make_test_systems.ringTrackTwoFramesNonIdeal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          make_test_systems.ringTrackTwoFramesNonIdeal(ring_rpy=zero_rpy,track_rpy=rpy)
        file_path='test_systems/ring_track_two_frames_non_ideal.xyz'
        file=open(file_path,'r')
        _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        file.close()
        x.append(theta)
        y.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method}')
      plot2(x,y,method=method,part=part,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_theta=constant_theta,assessment_type='double_axis')

def plot1(x,y,method='test',part='ring',axis=0,assessment_type=''):
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y)
  plt.plot(x,x)
  title=method.upper()+'('+part+','+axis+','+assessment_type+')'
  plt.title(title)
  plt.xlabel('Expected Angle(D)')
  plt.ylabel('Predicted Angle(D)')
  plt.savefig('output/assessment_'+method+'/'+title+'.png')
  #plt.show()
 
def plot2(x,y,method='test',part='ring',rotation_axis=0,constant_axis=1,constant_theta=10,assessment_type=''):
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
  plt.plot(x,x)
  title=method.upper()+'('+part+','+rotation_axis+','+constant_axis+'='+str(constant_theta)+','+assessment_type+')'
  plt.title(title)
  plt.xlabel('Expected Angle(D)')
  plt.ylabel('Predicted Angle(D)')
  plt.savefig('output/assessment_'+method+'/'+title+'.png')
  #plt.show()


assessRotationMethodSingleAxis(method='rot_atomic_r_t')
assessRotationMethodSingleAxis(method='rot_atomic_r_t_2')

assessRotationMethodDoubleAxis(method='rot_atomic_r_t',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=25)
assessRotationMethodDoubleAxis(method='rot_atomic_r_t',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=70)
assessRotationMethodDoubleAxis(method='rot_atomic_r_t',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=-45)

assessRotationMethodDoubleAxis(method='rot_atomic_r_t_2',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=25)
assessRotationMethodDoubleAxis(method='rot_atomic_r_t_2',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=70)
assessRotationMethodDoubleAxis(method='rot_atomic_r_t_2',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=-45)


