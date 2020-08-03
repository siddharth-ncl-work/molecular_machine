import pandas as pd

import sys
sys.path.append('../../../..')
from source import init,rotation
from lib import io_chem
import config

df=pd.read_csv('rotation_data_ring_atoms.csv')
columns=[f'insta_atom_no_{atom_no}_absolute_rotation' for atom_no in config.ring_atom_no_list]
df['insta_ring_absolute_rotation']=df[columns].mean(axis=1)
df['insta_ring_relative_rotation']=df['insta_ring_absolute_rotation']-df['insta_track_absolute_rotation']
df['net_ring_relative_rotation']=df['insta_ring_relative_rotation'].cumsum()
print(df['net_ring_relative_rotation'])


test_file_path='/home/vanka/ruchi/molecular_motor/case_1/molecular_rotor_b3lyp_with_solvent.md/scr_hf_1600/coors.xyz'

init.initConfig(test_file_path,ring_atom_no=69,track_atom_no=82)
print(f'--> {config}')
file=open(test_file_path,'r')
_rotation=rotation.getRotation(file,0,1,part1='track',type='absolute',method='rot_part_atomic_r_t_3')
print(_rotation)
