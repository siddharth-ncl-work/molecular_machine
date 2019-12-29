from math import cos
import pandas as pd
import sys
sys.path.append('..')

import config
from lib.io_chem import io
from lib.basic_operations import vector


def createSystem(cords_list,atom_list,file_path,add_axes=False):
  if add_axes:
    axes_cords_list,axes_atom_list=getAxes()
    cords_list.extend(axes_cords_list)
    atom_list.extend(axes_atom_list)
  _atom_list=map(str.upper,atom_list)
  atom_no_list=range(len(atom_list))
  x_list=[]
  y_list=[]
  z_list=[]
  for cords in cords_list:
    x_list.append(cords[0])
    y_list.append(cords[1])
    z_list.append(cords[2])
  data={'atom':_atom_list,'atom_no':atom_no_list,'x':x_list,'y':y_list,'z':z_list}
  df=pd.DataFrame.from_dict(data)
  io.writeFile(file_path,df)

def getAxes():
  axes_cords_list=[[0,0,0],[1,0,0],[0,1.5,0],[0,0,1.5]]
  axes_atom_list=['o','h','he','li']
  return (axes_cords_list,axes_atom_list)

def getIntersectionPoints(cords_list,axis):
  intersection_points_list=[]
  for cords in cords_list:
    theta=vector.getAngleR(cords,axis)
    r=vector.getMag(cords)
    p=r*cos(theta)
    i=[0,0,0]
    i[0]=p*axis[0]
    i[1]=p*axis[1]
    i[2]=p*axis[2]
    intersection_points_list.append(i)
  intersection_atom_list=['b']*len(cords_list)
  return (intersection_points_list,intersection_atom_list)
  
def addAxes(file_path):
  df=io.readFile(file_path)
  cords_list=list(df[['x','y','z']].values)
  atom_list=list(df['atom'].values)
  createSystem(cords_list,atom_list,file_path,add_axes=True)

def addOrigin(file_path):
  df=io.readFile(file_path)
  cords_list=list(df[['x','y','z']].values)
  atom_list=list(df['atom'].values)
  cords_list.append([0,0,0])
  atom_list.append('o')
  createSystem(cords_list,atom_list,file_path,add_axes=False)  

def getRingDf(df):
  return df[df['atom_no'].isin(range(config.ring_start_atom_no,config.ring_end_atom_no+1))]

def getTrackDf(df):
  return df[df['atom_no'].isin(range(config.track_start_atom_no,config.track_end_atom_no+1))]

