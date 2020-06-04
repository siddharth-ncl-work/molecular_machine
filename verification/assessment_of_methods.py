import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pickle
import sys
sys.path.extend(['.','..'])
import subprocess

from source import rotation,init,translation,shift_origin,energy
from lib.io_chem import io
from lib.basic_operations import physics,constants
import make_test_systems
import config

def _init(method,system):
  if 'rot' in method:
    subprocess.run(['mkdir',f'assessment_{method}'],cwd='output')
    subprocess.run(['mkdir','artificial_test_system','semi_real_test_system'],cwd=f'output/assessment_{method}')
    subprocess.run(['mkdir','ring','track'],cwd=f'output/assessment_{method}/artificial_test_system')
    subprocess.run(['mkdir','ring/single_axis_test','ring/double_axis_test','ring/triple_axis_test','ring/cone_test'],cwd=f'output/assessment_{method}/artificial_test_system')
    subprocess.run(['mkdir','track/single_axis_test','track/double_axis_test','track/triple_axis_test','track/cone_test'],cwd=f'output/assessment_{method}/artificial_test_system')
    subprocess.run(['mkdir','ring','track'],cwd=f'output/assessment_{method}/semi_real_test_system')
    subprocess.run(['mkdir','ring/single_axis_test','ring/double_axis_test','ring/triple_axis_test','ring/cone_test'],cwd=f'output/assessment_{method}/semi_real_test_system')
    subprocess.run(['mkdir','track/single_axis_test','track/double_axis_test','track/triple_axis_test','track/cone_test'],cwd=f'output/assessment_{method}/semi_real_test_system')
    subprocess.run(['mkdir','-p','output/assessment_rot_part_atomic_r_t_3/only_ring_artificial_test_system/ring/single_axis_test'])
  elif 'trans' in method:
    subprocess.run(['mkdir',f'assessment_{method}'],cwd='output')
    subprocess.run(['mkdir','artificial_test_system','semi_real_test_system'],cwd=f'output/assessment_{method}')
    subprocess.run(['mkdir','ring','track'],cwd=f'output/assessment_{method}/artificial_test_system')
    subprocess.run(['mkdir','ring/translation_without_rotation_test','ring/translation_with_single_axis_rotation_1d_test','ring/translation_with_single_axis_rotation_3d_test','ring/translation_with_random_triple_axis_rotation_test'],cwd=f'output/assessment_{method}/artificial_test_system')
    subprocess.run(['mkdir','track/translation_without_rotation_test','track/translation_with_single_axis_rotation_1d_test','track/translation_with_single_axis_rotation_3d_test','track/translation_with_random_triple_axis_rotation_test'],cwd=f'output/assessment_{method}/artificial_test_system')
    subprocess.run(['mkdir','ring','track'],cwd=f'output/assessment_{method}/semi_real_test_system')
    subprocess.run(['mkdir','ring/translation_without_rotation_test','ring/translation_with_single_axis_rotation_1d_test','ring/translation_with_single_axis_rotation_3d_test','ring/translation_with_random_triple_axis_rotation_test'],cwd=f'output/assessment_{method}/semi_real_test_system')
    subprocess.run(['mkdir','track/translation_without_rotation_test','track/translation_with_single_axis_rotation_1d_test','track/translation_with_single_axis_rotation_3d_test','track/translation_with_random_triple_axis_rotation_test'],cwd=f'output/assessment_{method}/semi_real_test_system')
  else:
    print(f'{method} does not exist, not creating directories')
  if system=='artificial':
    init.initConfig('test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz',ring_atom_no=0,track_atom_no=30,ref_axis_atom1_no=20,ref_axis_atom2_no=37,frame_no_pos=2)
    make_test_systems.ringTrackAtOriginNonIdealArtificial()
  elif system=='semi_real':
    init.initConfig(config.test_file_path,ring_atom_no=0,track_atom_no=153,ref_axis_atom1_no=75,ref_axis_atom2_no=98,frame_no_pos=2)
    make_test_systems.ringTrackAtOriginSemiReal()
    #init.initConfig(config.test_file_path,ring_atom_no=0,track_atom_no=153,ref_axis_atom1_no=75,ref_axis_atom2_no=98,frame_no_pos=2)
  else:
    print(f'system={system} does not exist')

def assessRotationMethodSingleAxis(method='rot_hybrid_3',step_size=10,parts=['ring','track'],system='',translation_list=[],show_plot=True):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  ring_translation_list=translation_list
  if 'only_ring' in system:
    track_translation_list=[0]
  else:
    track_translation_list=translation_list
  print(f'track_translation_list = {track_translation_list}')
  for ring_translation in ring_translation_list:
    for track_translation in track_translation_list:
      for part in parts:
        for axis in range(3):
          rpy=[0,0,0]
          x=[]
          y=[]
          for theta in range(-90,91,step_size):
            print('*'*50)
            rpy[axis]=theta
            if part=='ring':
              if system=='artificial':
                make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy,ring_translation=ring_translation,track_translation=track_translation)
              elif system=='semi_real':
                make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=rpy,track_rpy=zero_rpy,ring_translation=ring_translation,track_translation=track_translation)
              elif system=='only_ring_artificial':
                make_test_systems.ringTwoFramesArtificial(ring_rpy=rpy,track_rpy=zero_rpy,ring_translation=ring_translation,track_translation=track_translation)
            elif part=='track':
              if system=='artificial':
                make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy,ring_translation=ring_translation,track_translation=track_translation)
              elif system=='semi_real':
                make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=zero_rpy,track_rpy=rpy,ring_translation=ring_translation,track_translation=track_translation)
            if system=='artificial':
              file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
            elif system=='semi_real':
              file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
            elif system=='only_ring_artificial':
              file_path='test_systems/ring_two_frames_non_ideal_artificial_system.xyz'
            with open(file_path,'r') as file:
              if system=='artificial' or system=='semi_real':
                _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
              elif system=='only_ring_artificial':
                _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method,system_type='ring')
            x.append(theta)
            y.append(_rotation)
            print(f'{rpy},{part} Absolute Rotation = {_rotation},{method},single_axis,{system}')
          plot1(x,y,method=method,part=part,axis=axis,assessment_type='single_axis',system=system,translation=[ring_translation,track_translation],show_plot=show_plot)

def assessRotationMethodDoubleAxis2d(method='rot_atomic_r_t',step_size=10,rotation_axis=0,constant_axis=1,constant_theta=10,parts=['ring','track'],system='',show_plot=True):
  assert rotation_axis!=constant_axis,'Rotation axis should not be same constant axis'
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    rpy=[0,0,0]
    rpy[constant_axis]=constant_theta
    x=[]
    y=[]
    for theta in range(-50,51,step_size):
      rpy[rotation_axis]=theta
      if part=='ring':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
      elif part=='track':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
      if system=='artificial':
        file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
      elif system=='semi_real':
        file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
      with open(file_path,'r') as file:
        _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
      x.append(theta)
      y.append(_rotation)
      print(f'{rpy},{part} Absolute Rotation = {_rotation},{method},double_axis,2d,{system}')
    plot2(x,y,method=method,part=part,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_theta=constant_theta,assessment_type='double_axis',system=system,show_plot=show_plot)

def assessRotationMethodDoubleAxis3d(method='rot_atomic_r_t',rotation_axis=1,constant_axis=2,step_size=120,parts=['ring','track'],system='',show_plot=True):
  theta_range=range(-50,51,step_size)
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    X=[]
    Y=[]
    Z_expected=[]
    Z_predicted=[]
    for axis_theta in theta_range:
      rpy=[0,0,0]
      rpy[rotation_axis]=axis_theta
      x=[]
      theta_axis_list=[]
      z_expected=[]
      z_predicted=[]
      for theta_x in theta_range:
        rpy[0]=theta_x
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
        with open(file_path,'r') as file:
          _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        x.append(theta_x)
        theta_axis_list.append(axis_theta)
        z_expected.append(theta_x)
        z_predicted.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method},double_axis,3d,{system}')
      X.append(x)
      Y.append(theta_axis_list)
      Z_expected.append(z_expected)
      Z_predicted.append(z_predicted)
    plot3(X,Y,np.array(Z_expected),np.array(Z_predicted),method=method,part=part,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_axis_theta=0,assessment_type='double_axis',system=system,show_plot=show_plot)

def _tripleAxis(method='rot_atomic_r_t',rotation_axis=1,constant_axis=1,constant_axis_theta=0,step_size=120,parts=['ring','track'],system='',show_plot=True):
  theta_range=range(-50,51,step_size)
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    X=[]
    Y=[]
    Z_expected=[]
    Z_predicted=[]
    for rotation_axis_theta in theta_range:
      rpy=[0,0,0]
      rpy[rotation_axis]=rotation_axis_theta
      rpy[constant_axis]=constant_axis_theta
      x=[]
      rotation_axis_theta_list=[]
      z_expected=[]
      z_predicted=[]
      for theta_x in theta_range:
        rpy[0]=theta_x
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
        with open(file_path,'r') as file:
          _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        x.append(theta_x)
        rotation_axis_theta_list.append(rotation_axis_theta)
        z_expected.append(theta_x)
        z_predicted.append(_rotation)
        print(f'{rpy},{part} Absolute Rotation = {_rotation},{method},triple_axis,{system}')
      X.append(x)
      Y.append(rotation_axis_theta_list)
      Z_expected.append(z_expected)
      Z_predicted.append(z_predicted)
    plot3(X,Y,np.array(Z_expected),np.array(Z_predicted),method=method,part=part,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_axis_theta=constant_axis_theta,assessment_type='triple_axis',system=system,show_plot=show_plot)

def assessRotationMethodTripleAxis3d(method='rot_atomic_r_t',rotation_axis=1,constant_axis=1,constant_axis_theta_range=[],step_size=120,parts=['ring','track'],system='',show_plot=True):
  for constant_axis_theta in constant_axis_theta_range:
    _tripleAxis(method=method,rotation_axis=rotation_axis,constant_axis=constant_axis,constant_axis_theta=constant_axis_theta,step_size=step_size,parts=parts,system=system,show_plot=show_plot)

def plot1(x,y,method='test',part='ring',axis=0,assessment_type='',system='',translation=-50,show_plot=True):
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y,'r',label='predicted')
  if axis=='x':
    plt.plot(x,x,'b',label='expected')
  else:
    zero=np.zeros(len(x))
    plt.plot(x,zero,'b',label='expected')
  title=method.upper()+'('+part+','+axis+','+assessment_type+','+system+f'{translation}'+')'
  plt.title(title)
  plt.xlabel(f'{axis} Rotation(D)')
  plt.ylabel('Predicted/Expected x Rotation (D)')
  plt.ylim(-100, 100)
  plt.legend()
  plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  data={'x':x,'predicted_rotation':y,'expected_rotation':x}
  pd.DataFrame.from_dict(data).to_csv('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.csv')
  if show_plot:
    plt.show()
 
def plot2(x,y,method='test',part='ring',rotation_axis=0,constant_axis=1,constant_theta=10,assessment_type='',system='',show_plot=True):
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
  plt.plot(x,y,'r',label='predicted')
  if rotation_axis=='x':
    plt.plot(x,x,'b',label='expected')
  else:
    zero=np.zeros(len(x))
    plt.plot(x,zero,'b',label='expected')
  title=method.upper()+'('+part+','+rotation_axis+','+constant_axis+'='+str(constant_theta)+','+assessment_type+','+system+',2d'+')'
  plt.title(title)
  plt.xlabel(f'{rotation_axis} Rotation(D)')
  plt.ylabel('Predicted/Expected x Rotation(D)')
  plt.ylim(-100, 100)
  plt.legend()
  plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()

def plot3(X,Y,Z_expected,Z_predicted,method='rot_atomic_r_t',part='',rotation_axis=0,constant_axis=0,constant_axis_theta=0,assessment_type='',system='',show_plot=True):
  axis={0:'x',1:'y',2:'z'}
  title=method.upper()+'('+part+',x,'+axis[rotation_axis]+','+axis[constant_axis]+'='+str(constant_axis_theta)+','+assessment_type+','+system+',3d'+')'
  data={'X':X,'Y':Y,'Z_expected':Z_expected,'Z_predicted':Z_predicted}
  pickle.dump(data,open('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.dat.pkl', 'wb'))
   
  for ele in [-10,10,45]:
    for azm in range(0,181,45):
      title=method.upper()+'('+part+',x,'+axis[rotation_axis]+','+axis[constant_axis]+'='+str(constant_axis_theta)+','+assessment_type+','+system+',3d,'+f'[{ele},{azm}]'+')'
      fig=plt.figure(figsize=(16,8))
      plt.rcParams.update({'font.size': 15})
      ax=plt.axes(projection="3d")
      surf1=ax.plot_surface(X,Y,Z_expected,cmap='Reds',edgecolor='none')
      surf2=ax.plot_surface(X,Y,Z_predicted,cmap='winter',edgecolor='none')
      ax.set_title(title)
      ax.set_xlabel('x Rotation')
      ax.set_ylabel(f'{axis[rotation_axis]} Rotation')
      ax.set_zlabel('Expcted/Predicted x Rotation')
      ax.view_init(ele,azm)
      fig.colorbar(surf1,label='expected',fraction=.05)
      fig.colorbar(surf2,label='predicted',fraction=.05)
      plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()

#TRANSLATION
def assessTranslationMethodWithoutRotation(method='',step_size=10,parts=['ring','track'],system='',show_plot=True):
  distance_range=np.arange(-10,11,step_size)
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    x=[]
    y=[]
    for distance in distance_range:
      if part=='ring':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=distance,track_translation=0,ring_rpy=zero_rpy,track_rpy=zero_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=distance,track_translation=0,ring_rpy=zero_rpy,track_rpy=zero_rpy)
      elif part=='track':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=0,track_translation=distance,ring_rpy=zero_rpy,track_rpy=zero_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=0,track_translation=distance,ring_rpy=zero_rpy,track_rpy=zero_rpy)
      if system=='artificial':
        file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
      elif system=='semi_real':
        file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
      with open(file_path,'r') as file:
        _translation=translation.getTranslation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method,unit='A')
      x.append(distance)
      y.append(_translation)
      print(f'{distance},{part} Absolute Translation = {_translation},{method},translation_without_rotation,{system}')
    plot4(x,y,method=method,part=part,assessment_type='translation_without_rotation',system=system,show_plot=show_plot)

def assessTranslationMethodWithSingleAxisRotation1d(method='',rotation_axis=1,theta=60,step_size=120,parts=['ring','track'],system='',show_plot=True):
  distance_range=np.arange(-10,11,step_size)
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  rpy=[0,0,0]
  rpy[rotation_axis]=theta
  for part in parts:
    x=[]
    y=[]
    for distance in distance_range:
      if part=='ring':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=distance,track_translation=0,ring_rpy=rpy,track_rpy=zero_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=distance,track_translation=0,ring_rpy=rpy,track_rpy=zero_rpy)
      elif part=='track':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=0,track_translation=distance,ring_rpy=zero_rpy,track_rpy=rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=0,track_translation=distance,ring_rpy=zero_rpy,track_rpy=rpy)
      if system=='artificial':
        file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
      elif system=='semi_real':
        file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
      with open(file_path,'r') as file:
        _translation=translation.getTranslation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method,unit='A')
      x.append(distance)
      y.append(_translation)
      print(f'{distance},{part} Absolute Translation = {_translation},{method},translation_with_single_axis_rotation_1d,{system}')
    plot4(x,y,method=method,part=part,assessment_type='translation_with_single_axis_rotation_1d',system=system,show_plot=show_plot)

def assessTranslationMethodWithSingleAxisRotation3d(method='',rotation_axis=1,step_size=120,parts=['ring','track'],system='',show_plot=True):
  distance_range=np.arange(-10,11,step_size)
  theta_range=range(-90,91,10)
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  for part in parts:
    X=[]
    Y=[]
    Z_expected=[]
    Z_predicted=[]
    for distance in distance_range:
      x=[]
      axis_theta_list=[]
      z_expected=[]
      z_predicted=[]
      for theta in theta_range:
        rpy=[0,0,0]
        rpy[rotation_axis]=theta
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=distance,track_translation=0,ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=distance,track_translation=0,ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=0,track_translation=distance,ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=0,track_translation=distance,ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
        with open(file_path,'r') as file:
          _translation=translation.getTranslation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method,unit='A')
        x.append(distance)
        axis_theta_list.append(theta)
        z_expected.append(distance)
        z_predicted.append(_translation)
        print(f'{distance},{rpy},{part} Absolute Translation = {_translation},{method},translation_with_single_axis_rotation_3d,{rotation_axis},{system}')
      X.append(x)
      Y.append(axis_theta_list)
      Z_expected.append(z_expected)
      Z_predicted.append(z_predicted)
    plot5(X,Y,np.array(Z_expected),np.array(Z_predicted),method=method,part=part,rotation_axis=rotation_axis,assessment_type='translation_with_single_axis_rotation_3d',system=system,show_plot=show_plot)

def assessTranslationMethodWithRandomTripleAxisRotation1d(method='',step_size=10,parts=['ring','track'],system='',show_plot=True):
  distance_range=np.arange(-10,11,step_size)
  frame1_no=0
  frame2_no=1
  for part in parts:
    x=[]
    y=[]
    for distance in distance_range:
      ring_rpy=np.random.uniform(low=-10,high=10,size=(3,))
      track_rpy=np.random.uniform(low=-10,high=10,size=(3,))
      if part=='ring':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=distance,track_translation=0,ring_rpy=ring_rpy,track_rpy=track_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=distance,track_translation=0,ring_rpy=ring_rpy,track_rpy=track_rpy)
      elif part=='track':
        if system=='artificial':
          make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_translation=0,track_translation=distance,ring_rpy=ring_rpy,track_rpy=track_rpy)
        elif system=='semi_real':
          make_test_systems.ringTrackTwoFramesSemiReal(ring_translation=0,track_translation=distance,ring_rpy=ring_rpy,track_rpy=track_rpy)
      if system=='artificial':
        file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
      elif system=='semi_real':
        file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
      with open(file_path,'r') as file:
        _translation=translation.getTranslation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method,unit='A')
      x.append(distance)
      y.append(_translation)
      print(f'{distance},{part} Absolute Translation = {_translation},{method},translation_with_random_triple_axis_rotation,{system}')
    plot4(x,y,method=method,part=part,assessment_type='translation_with_random_triple_axis_rotation',system=system,show_plot=show_plot)

def plot4(x,y,method='test',part='ring',assessment_type='',system='',show_plot=True):
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y,'r',label='predicted')
  plt.plot(x,x,'b',label='expected')
  title=method.upper()+'('+part+','+assessment_type+','+system+')'
  plt.title(title)
  plt.xlabel('Translation (A)')
  plt.ylabel('Predicted/Expected Translation (A)')
  plt.ylim(-15, 15)
  plt.legend()
  plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()

def plot5(X,Y,Z_expected,Z_predicted,method='rot_atomic_r_t',part='',rotation_axis=0,assessment_type='',system='',show_plot=True):
  axis={0:'x',1:'y',2:'z'}
  title=method.upper()+'('+part+','+axis[rotation_axis]+','+assessment_type+','+system+',3d'+')'
  data={'X':X,'Y':Y,'Z_expected':Z_expected,'Z_predicted':Z_predicted}
  pickle.dump(data,open('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.dat.pkl', 'wb'))

  for ele in [-10,10,45]:
    for azm in range(0,181,45):
      title=method.upper()+'('+part+','+axis[rotation_axis]+','+assessment_type+','+system+',3d,'+f'[{ele},{azm}]'+')'
      fig=plt.figure(figsize=(16,8))
      plt.rcParams.update({'font.size': 15})
      ax=plt.axes(projection="3d")
      surf1=ax.plot_surface(X,Y,Z_expected,cmap='Reds')
      surf2=ax.plot_surface(X,Y,Z_predicted,cmap='winter')
      ax.set_title(title)
      ax.set_xlabel('Translation (A)')
      ax.set_ylabel('Rotation (D)')
      ax.set_zlabel('Expcted/Predicted Translation')
      fig.colorbar(surf1,label='expected',fraction=.05)
      fig.colorbar(surf2,label='predicted',fraction=.05)
      ax.view_init(ele,azm)
      plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()

def assessRotationMethodSingleAxisPoster(method='rot_hybrid_3',step_size=10,parts=['ring','track'],system='',show_plot=True):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  theta_range=range(-90,91,step_size)
  x=theta_range
  systems=['artificial','semi_real']
  print(method)
  for part in parts:
    for axis in range(3):
      Y={}
      for system in systems:
        _init('custom_single_axis',system)
        y=[]
        rpy=[0,0,0]
        for theta in theta_range:
          rpy[axis]=theta
          if part=='ring':
            if system=='artificial':
              make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
            elif system=='semi_real':
              make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
          elif part=='track':
            if system=='artificial':
              make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
            elif system=='semi_real':
              make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
          if system=='artificial':
            file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
          elif system=='semi_real':
            file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
          with open(file_path,'r') as file:
            _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
          y.append(_rotation)
          print(f'{rpy},{part} Absolute Rotation = {_rotation},{method},single_axis,{system}')
        Y[system]=y
      plot1Poster(x,Y,method=method,part=part,axis=axis,assessment_type='single_axis',system=system,show_plot=show_plot)

def plot1Poster(x,Y,method='test',part='ring',axis=0,assessment_type='',system='',show_plot=True):
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,Y['artificial'],'r',label='Artificial',lw=5)
  plt.plot(x,Y['semi_real'],'g',label='Semi-Real',lw=5)
  if axis=='x':
    plt.plot(x,x,'b',label='Expected',lw=5)
  else:
    zero=np.zeros(len(x))
    plt.plot(x,zero,'b',label='Expected',lw=5)
  title=method.upper()+'('+part+','+axis+','+assessment_type+')'
  plt.title(title)
  plt.xlabel(f'{axis} Rotation(D)')
  plt.ylabel('Predicted/Expected x Rotation (D)')
  plt.ylim(-100, 100)
  plt.legend()
  #plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()

def coneAssessment(method='',system='',parts='',step_size=0):
  if system=='artificial':
    file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
  elif system=='semi_real':
    file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
  with open(file_path,'r') as file:
    frame1_cords=io.readFileMd(file,0,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,1,frame_no_pos=config.frame_no_pos)
  track_atom_list=config.track_atom_no_list
  ring_atom_list=config.ring_atom_no_list
  step_size=5
  theta_range=range(-90,91,step_size)
  x=theta_range
  #initial_cords_list=[[1.0, -0.5,  0],[2.0,  0.5, 0]]#[[1.0,  0.353553,  0.353553],[2.0, -0.353553, -0.353553]]
  print(system)
  for part in parts:
    if part=='ring':
      atom_no_list=ring_atom_list
    elif part=='track':
      trans_axis=[0,0,0]
      cog1=physics.getCog(frame1_cords,atom_list=ring_atom_list)
      cog2=physics.getCog(frame2_cords,atom_list=ring_atom_list)
      print(f'{cog1},{cog2}')
      trans_axis[0]=cog2[0]-cog1[0]
      trans_axis[1]=cog2[1]-cog1[1]
      trans_axis[2]=cog2[2]-cog1[2]
      nearest_atom_list=rotation.getNearestAtomList(frame1_cords,cog1,trans_axis,config.track_range)
      atom_no_list=list(filter(lambda x:x in track_atom_list,nearest_atom_list))
    
    new_frame1_cords,new_frame2_cords=shift_origin.shiftOrigin(frame1_cords,frame2_cords,process='rotation',ref_axis_alignment=False)

    initial_cords_list=new_frame1_cords[new_frame1_cords['atom_no'].isin(atom_no_list)][['x','y','z']].values
    print(part)
    print(atom_no_list)
    print(initial_cords_list)
    for axis in range(1,3):
      Y=[]
      _axis=[0,0,0]
      _axis[axis]=1
      for initial_cords in initial_cords_list:
        atom_data={'atom':['c'],'atom_no':[0],'x':initial_cords[0],'y':initial_cords[1],'z':initial_cords[2]}
        initial_df=pd.DataFrame.from_dict(atom_data)
        y=[]
        for theta in theta_range:
          final_df=rotation.rotateAlongAxis(initial_df,_axis,math.radians(theta))
          final_cords=final_df[['x','y','z']].values[0]
          initial_cords[0]=0
          final_cords[0]=0
          _rotation=rotation.getRPYAngles(initial_cords,final_cords,unit='degrees')    
          #print(f'theta = {theta}, x-axis rotation = {_rotation}')
          y.append(_rotation[0])
        Y.append(y)
      y=np.mean(np.array(Y),axis=0)
      print(y)
      plotConeAssessment(x,y,method=method,part=part,axis=axis,system=system,assessment_type='cone')

def plotConeAssessment(x,y,method='',part='ring',axis=0,assessment_type='',system='',show_plot=True):
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y,'r',label='Error')
  if axis=='x':
    plt.plot(x,x,'b',label='Expected')
  else:
    zero=np.zeros(len(x))
    plt.plot(x,zero,'b',label='Expected')
  title=method.upper()+f'({system},'+part+','+axis+','+assessment_type
  plt.title(title)
  plt.xlabel(f'{axis} Rotation(D)')
  plt.ylabel('Predicted/Expected x Rotation (D)')
  plt.ylim(-100, 100)
  plt.legend()
  plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()

#ENERGY
def assessRKEMethodSingleAxis(method='rot_hybrid_3',step_size=10,parts=['ring','track'],system='',show_plot=True):
  frame1_no=0
  frame2_no=1
  zero_rpy=[0,0,0]
  theta_range=range(-90,91,step_size)
  x=theta_range
  for part in parts:
    for axis in range(3):
      rpy=[0,0,0]
      y_predicted=[]
      y_expected=[]
      for theta in theta_range:
        rpy[axis]=theta
        if part=='ring':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=rpy,track_rpy=zero_rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=rpy,track_rpy=zero_rpy)
        elif part=='track':
          if system=='artificial':
            make_test_systems.ringTrackTwoFramesNonIdealArtificial(ring_rpy=zero_rpy,track_rpy=rpy)
          elif system=='semi_real':
            make_test_systems.ringTrackTwoFramesSemiReal(ring_rpy=zero_rpy,track_rpy=rpy)
        if system=='artificial':
          file_path='test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
        elif system=='semi_real':
          file_path='test_systems/ring_track_two_frames_semi_real_system.xyz'
        with open(file_path,'r') as file:
          predicted_rke,_=energy.getRKE(file,frame1_no,frame2_no,part1=part,part2='track',type='absolute',method=method)
        y_predicted.append(predicted_rke)
        expected_rke=getExpectedRKE(system=system,part=part,axis=axis,_rotation=theta)
        y_expected.append(expected_rke)
        print(f'{rpy},{part} Absolute RKE = {predicted_rke},{method},single_axis,{system}')
      plotRKE(x,y_predicted,y_expected,method=method,part=part,axis=axis,assessment_type='RKE_single_axis',system=system,show_plot=show_plot)

def getExpectedRKE(system='',part='',axis='',_rotation=0):
  MI_artificial={'ring':[1.66465125e-43,8.32325625e-44,8.323256249999998e-44],'track':[1.597027387500013e-45,8.831999703266061e-43,8.835985561608938e-43]}
  MI_semi_real={}
  MI=0
  if system=='artificial':
    MI=MI_artificial[part][axis]
  elif system=='semi_real':
    MI=MI_semi_real[part][axis]
  omega=math.radians(_rotation)/(config.simulation_time_step*constants.femto)
  expected_rke=0.5*MI*omega**2
  return expected_rke

def plotRKE(x,y_predicted,y_expected,method='',part='',axis='',assessment_type='',system='',show_plot=True):
  print(len(x))
  print(len(y_predicted))
  print(len(y_expected))
  if axis==0:
    axis='x'
  elif axis==1:
    axis='y'
  elif axis==2:
    axis='z'
  plt.figure(figsize=(16,8))
  plt.rcParams.update({'font.size': 15})
  plt.plot(x,y_expected,'b',label='expected',lw=5)
  plt.plot(x,y_predicted,'r',label='predicted')
  title=method.upper()+'('+part+','+axis+','+assessment_type+','+system+')'
  plt.title(title)
  plt.xlabel(f'{axis} Rotation(deg)')
  plt.ylabel('Predicted/Expected RKE (D)')
  #plt.ylim(-100, 100)
  plt.legend()
  #plt.savefig('output/assessment_'+method+'/'+f'{system}_test_system'+'/'+part+'/'+f'{assessment_type}_test'+'/'+title+'.png')
  if show_plot:
    plt.show()



#ROTATION
system_list=['only_ring_artificial']#'artificial']
method_list=['rot_part_atomic_r_t_3']
step_size=5
parts=['ring']
translation_list=[0,3.14,-3.14]
show_plot=True
for system in system_list:
  for method in method_list:
    _init(method,system)
    #coneAssessment(method=method,system=system,parts=parts,step_size=step_size)
    assessRotationMethodSingleAxis(method=method,step_size=step_size,parts=parts,system=system,translation_list=translation_list,show_plot=show_plot)
    #coneAssessment(system=system,parts=parts,step_size=step_size)
    #assessRotationMethodDoubleAxis2d(method=method,step_size=step_size,rotation_axis=0,constant_axis=1,constant_theta=45,system=system,show_plot=show_plot)
    #assessRotationMethodDoubleAxis2d(method=method,step_size=step_size,rotation_axis=0,constant_axis=1,constant_theta=-45,system=system,show_plot=show_plot)
    #assessRotationMethodDoubleAxis2d(method=method,step_size=step_size,rotation_axis=0,constant_axis=2,constant_theta=45,system=system,show_plot=show_plot)
    #assessRotationMethodDoubleAxis2d(method=method,step_size=step_size,rotation_axis=0,constant_axis=2,constant_theta=-45,system=system,show_plot=show_plot)
    #assessRotationMethodDoubleAxis3d(method=method,rotation_axis=1,constant_axis=2,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    #assessRotationMethodDoubleAxis3d(method=method,rotation_axis=2,constant_axis=1,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    #assessRotationMethodTripleAxis3d(method=method,rotation_axis=1,constant_axis=2,constant_axis_theta_range=[-10,10],step_size=step_size,parts=parts,system=system,show_plot=show_plot)



#TRANSLATION
system_list=['artificial']
method_list=['trans_com_3']
step_size=0.5
parts=['ring','track']
show_plot=True
for system in system_list:
  for method in method_list:
    _init(method,system)
    #assessTranslationMethodWithoutRotation(method=method,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    assessTranslationMethodWithSingleAxisRotation1d(method=method,rotation_axis=0,theta=90,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    #assessTranslationMethodSingleAxisWithRotation3d(method=method,rotation_axis=0,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    #assessTranslationMethodSingleAxisWithRotation3d(method=method,rotation_axis=1,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    #assessTranslationMethodSingleAxisWithRotation3d(method=method,rotation_axis=2,step_size=step_size,parts=parts,system=system,show_plot=show_plot)
    #assessTranslationMethodWithRandomTripleAxisRotation1d(method=method,step_size=step_size,parts=parts,system=system,show_plot=show_plot)


#assessRKEMethodSingleAxis(method='energy_rot_part_atomic_r_t_3',system='artificial',parts=['ring','track'],step_size=5,show_plot=True)

#coneAssessment()
#_init('rot_part_atomic_r_t_3','artificial')
#assessRotationMethodSingleAxis(method='rot_part_atomic_r_t_3',step_size=5,system='artificial',parts=['track'],show_plot=True)
#assessRotationMethodSingleAxisPoster(method='rot_part_atomic_r_t_3',step_size=5,show_plot=True)
