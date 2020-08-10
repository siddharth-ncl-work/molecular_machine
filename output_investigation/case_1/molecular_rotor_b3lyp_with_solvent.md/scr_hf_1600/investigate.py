import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

import sys
sys.path.append('../../../..')
from source import init,rotation,shift_origin
from lib.io_chem import io
from lib.basic_operations import physics,vector
import config

test_file_path='/home/vanka/ruchi/molecular_motor/case_1/molecular_rotor_b3lyp_with_solvent.md/scr_hf_1600/coors.xyz'
init.initConfig(test_file_path,ring_atom_no=69,track_atom_no=82)

####################################################################3
def visualizeShiftOrigin(input_file_path,frame1_no,frame2_no,method='old',part='ring'):
  '''
  Visualize shift_origin Transformations
  Extract two frames 
  '''
  output_file_path=f'test_file_{frame1_no}_{frame2_no}.xyz'

  with open(input_file_path,'r') as file:
    init_frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
    init_frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)

  if method=='old':
    init_axis,init_origin=shift_origin.getAxisAndOriginOld(init_frame1_cords,init_frame2_cords,process='rotation',axis=None,origin=None,debug=True,method='old')
  elif method=='new':
    init_axis,init_origin=shift_origin.getAxisAndOriginNew(init_frame1_cords,init_frame2_cords,process='rotation',axis=None,origin=None,debug=True,method='new')
  print(init_axis,init_origin)

  plot(init_frame1_cords,init_axis,init_origin,part=part,output_file_name=f'init_frame1_cords_{method}.jpg')
  plot(init_frame2_cords,init_axis,init_origin,part=part,output_file_name=f'init_frame2_cords_{method}.jpg')

  transformed_frame1_cords,transformed_frame2_cords=shift_origin.shiftOrigin(init_frame1_cords,init_frame2_cords,process='rotation',debug=True)
  
  transformed_axis=transformed_frame1_cords.iloc[-1][['x','y','z']].values
  transformed_origin=transformed_frame1_cords.iloc[-2][['x','y','z']].values
  transformed_frame1_cords=transformed_frame1_cords.iloc[:-2]
  print(transformed_axis,transformed_origin)
  
  plot(transformed_frame1_cords,transformed_axis,transformed_origin,part=part,output_file_name=f'transformed_frame1_cords_{method}.jpg')
  plot(transformed_frame2_cords,transformed_axis,transformed_origin,part=part,output_file_name=f'transformed_frame2_cords_{method}.jpg')

  with open(output_file_path,'w') as output_file:
    io.writeFileMd(output_file,transformed_frame1_cords,frame1_no,frame_no_pos=config.frame_no_pos)
    io.writeFileMd(output_file,transformed_frame2_cords,frame2_no,frame_no_pos=config.frame_no_pos) 
 
def plot(cords,axis,origin,part='whole',output_file_name='test.jpg'):
  if part=='ring':
    cords=cords[cords['atom_no'].isin(config.ring_atom_no_list)]
  elif part=='track':
    cords=cords[cords['atom_no'].isin(config.track_atom_no_list)]
  elif part=='whole':
    pass

  fig = plt.figure(figsize=(10,10),dpi=72)
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(cords['x'],cords['y'],cords['z'],s=10,color='orange')

  d = -vector.getDotProduct(origin,axis)
  print(f'd = {d}')
  [xx,yy]=np.meshgrid(range(int(origin[0])-5,int(origin[0])+5),range(int(origin[1])-5,int(origin[1])+5))
  z=(-axis[0]*xx - axis[1]*yy - d)/float(axis[2])
  i=np.random.randint(0,10,size=2)
  print(i)
  print(axis[0]*xx[i[0]][i[1]]+axis[1]*yy[i[0]][i[1]]+axis[2]*z[i[0]][i[1]]+d)

  color='#1C4675'
  ax.plot_surface(xx,yy,z,color=color)
  ax.scatter([origin[0]],[origin[1]],[origin[2]],s=100,color=color)
  ax.quiver([origin[0]],[origin[1]],[origin[2]],[axis[0]],[axis[1]],[axis[2]],length=10,normalize=True,color=color)
  ax.quiver([0],[0],[0],[1],[0],[0],length=10,normalize=True,color='g')
  ax.quiver([0],[0],[0],[0],[1],[0],length=10,normalize=True,color='g')
  ax.quiver([0],[0],[0],[0],[0],[1],length=10,normalize=True,color='g')
  ax.scatter([0],[0],[0],s=100,color='g')  

  
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  ax.set_zlim(-10,10)
  ax.view_init(10,10)
  plt.savefig(output_file_name,transparent = True, bbox_inches = 'tight',pad_inches = 0)
  plt.show()
  
##########################################################
def regression(input_file_path,frame1_no):
  with open(input_file_path,'r') as file:
    frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
  cog1=physics.getCog(frame1_cords,atom_list=config.ring_atom_no_list)
  #frame1_cords=shift_origin._shiftOrigin(frame1_cords,cog1)
  frame1_cords=frame1_cords[frame1_cords['atom_no'].isin(config.ring_atom_no_list)]
  X=frame1_cords[['x','y']].values
  Y=frame1_cords['z'].values
  
  reg = LinearRegression().fit(X, Y)
  print(reg.coef_,reg.intercept_)
  
  value_range=range(-5,5)
  [xx,yy]=np.meshgrid(range(int(cog1[0])-5,int(cog1[0])+5),range(int(cog1[1])-5,int(cog1[1])+5))
  z=[]

  for y in yy:
    _X=np.array(list(zip(xx[0],y)))
    _Y=reg.predict(_X)
    z.append(_Y)

  z=np.array(z)
  fig = plt.figure(figsize=(10,10),dpi=72)
  ax = fig.add_subplot(111, projection='3d') 
  ax.scatter(frame1_cords['x'],frame1_cords['y'],frame1_cords['z'],color='orange',s=50)
  color='#1C4675'
  ax.plot_surface(xx,yy,z,color=color)
  ax.scatter([cog1[0]],[cog1[1]],[cog1[2]],s=100,color=color)
  ax.quiver([cog1[0]],[cog1[1]],[cog1[2]],[reg.coef_[0]],[reg.coef_[1]],[-1],length=5,color=color)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  plt.show()


def calculateAxisDifference(input_file_path,start_frame_no,end_frame_no):
  
  file=open(input_file_path,'r')

  data={'frame_no':[],'old_axis':[],'old_origin':[],'new_axis':[],'new_origin':[],'axis_difference (deg)':[]}
  assert end_frame_no>=start_frame_no,'Invalid Frame Numbers'
  prev_frame_no=start_frame_no
  prev_frame_cords=io.readFileMd(file,prev_frame_no,frame_no_pos=config.frame_no_pos)
  pbar=tqdm(range(start_frame_no+config.step_size,end_frame_no+1,config.step_size))
  for curr_frame_no in pbar:
    pbar.set_description(f'Frame No: {curr_frame_no}')
    curr_frame_cords=io.readFileMd(file,curr_frame_no,frame_no_pos=config.frame_no_pos)
    old_axis,old_origin=shift_origin.getAxisAndOriginOld(prev_frame_cords,curr_frame_cords,process='rotation',axis=None,origin=None,debug=False)
    new_axis,new_origin=shift_origin.getAxisAndOriginNew(prev_frame_cords,curr_frame_cords,process='rotation',axis=None,origin=None,debug=False)
    axis_difference=vector.getAngleD(old_axis,new_axis)
    data['frame_no'].append(curr_frame_no)
    data['old_axis'].append(old_axis)
    data['old_origin'].append(old_origin)
    data['new_axis'].append(new_axis)
    data['new_origin'].append(new_origin)
    data['axis_difference (deg)'].append(axis_difference)
    prev_frame_no=curr_frame_no
    prev_frame_cords=curr_frame_cords.copy()

  df=pd.DataFrame.from_dict(data)
  df.to_csv('axis_difference_data.csv',index=False)
  fig,ax=plt.subplots(1,1,figsize=(16,9),dpi=72)
  ax.plot(df['frame_no'],df['axis_difference (deg)'])
  ax.set_xlabel('Frame No.')
  ax.set_ylabel('Axis Difference (Deg)')
  plt.grid()
  plt.savefig('axis_difference_plot.jpg')
  plt.show()

def visualizeDifference(input_file_path,frame1_no,frame2_no,part='whole'):
  with open(input_file_path,'r') as file:
    frame1_cords=io.readFileMd(file,frame1_no,frame_no_pos=config.frame_no_pos)
    frame2_cords=io.readFileMd(file,frame2_no,frame_no_pos=config.frame_no_pos)

  old_axis,old_origin=shift_origin.getAxisAndOriginOld(frame1_cords,frame2_cords,process='rotation',axis=None,origin=None,debug=False)
  new_axis,new_origin=shift_origin.getAxisAndOriginNew(frame1_cords,frame2_cords,process='rotation',axis=None,origin=None,debug=False)
  
  fig = plt.figure(figsize=(10,10),dpi=72)
  ax = fig.add_subplot(111, projection='3d')
  ring_cords=frame1_cords[frame1_cords['atom_no'].isin(config.ring_atom_no_list)]
  ax.scatter(ring_cords['x'],ring_cords['y'],ring_cords['z'],color='orange',s=50)
  axis,origin=old_axis,old_origin
  d = -vector.getDotProduct(origin,axis)
  [xx,yy]=np.meshgrid(range(int(origin[0])-5,int(origin[0])+5),range(int(origin[1])-5,int(origin[1])+5))
  z=(-axis[0]*xx - axis[1]*yy - d)/float(axis[2])
  color='#BA962B'
  ax.plot_surface(xx,yy,z,color=color)
  ax.scatter([origin[0]],[origin[1]],[origin[2]],s=100,color=color)
  ax.quiver([origin[0]],[origin[1]],[origin[2]],[axis[0]],[axis[1]],[axis[2]],length=10,normalize=True,color=color,label='old',arrow_length_ratio=0.1)
  i=np.random.randint(0,10,size=2)
  print(i) 
  print(axis[0]*(xx[i[0]][i[1]])+axis[1]*(yy[i[0]][i[1]])+axis[2]*(z[i[0]][i[1]])+d)
  axis,origin=new_axis,new_origin
  d = -vector.getDotProduct(origin,axis)
  [xx,yy]=np.meshgrid(range(int(origin[0])-5,int(origin[0])+5),range(int(origin[1])-5,int(origin[1])+5))
  z=(-axis[0]*xx - axis[1]*yy - d)/float(axis[2])
  color='#1C4675'
  ax.plot_surface(xx,yy,z,color=color)
  ax.scatter([origin[0]],[origin[1]],[origin[2]],s=100,color=color)
  ax.quiver([origin[0]],[origin[1]],[origin[2]],[axis[0]],[axis[1]],[axis[2]],length=10,normalize=True,color=color,label='new',arrow_length_ratio=0.1)
  i=np.random.randint(0,10,size=2)
  print(i)
  print(axis[0]*xx[i[0]][i[1]]+axis[1]*yy[i[0]][i[1]]+axis[2]*z[i[0]][i[1]]+d)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  plt.legend()
  plt.show()
 
###############################################

frame1_no=18255#np.random.randint(0,55230)
frame2_no=frame1_no+10
print(f'FRAME1 NO = {frame1_no}')
regression(test_file_path,frame1_no)
visualizeShiftOrigin(test_file_path,frame1_no,frame2_no,method='old',part='ring')
#visualizeDifference(test_file_path,frame1_no,frame2_no,part='ring')
################################################
#calculateAxisDifference(test_file_path,0,86054)
##########################################################
'''
df=pd.read_csv('rotation_data_ring_atoms.csv')
df_ref=pd.read_csv('../scr_hf_1600_ref/rotation_data.csv')

#########################################################3
columns=[f'insta_atom_no_{atom_no}_absolute_rotation' for atom_no in config.ring_atom_no_list]
df['insta_ring_absolute_rotation']=df[columns].mean(axis=1)
df['insta_ring_relative_rotation']=df['insta_ring_absolute_rotation']-df['insta_track_absolute_rotation']
df['net_ring_relative_rotation']=df['insta_ring_relative_rotation'].cumsum()
print(df[['frame_no','insta_ring_relative_rotation','net_ring_relative_rotation']])

print(df_ref)
print(np.unique(np.isclose(df_ref['relative_rotation'],df['insta_ring_relative_rotation']),return_counts=True))
print(np.unique(np.isclose(df_ref['net_relative_rotation'],df['net_ring_relative_rotation']),return_counts=True))

##################################################
print(f'--> {config}')
with open(test_file_path,'r') as file:
  _rotation=rotation.getRotation(file,55220,55230,part1='ring',type='absolute',method='rot_part_atomic_r_t_3')
print(_rotation)


###################################################
atom_no=0
frame_no=20#55230
atom_df=df[['frame_no','insta_track_absolute_rotation',f'insta_atom_no_{atom_no}_absolute_rotation']]
print(atom_df.describe())
print(atom_df[atom_df[f'insta_atom_no_{atom_no}_absolute_rotation']>14])
print(atom_df[atom_df['frame_no']==frame_no])
extractFrames(test_file_path,frame_no-10,frame_no)

#########################################################
'''

