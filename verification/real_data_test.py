import sys
sys.path.extend(['.','..'])

import config
from source import rotation,init

file_path=config.test_file_path
init.initConfig(file_path)
method='rot_part_atomic_r_t_3'
frame1_no=config.start_frame_no
frame2_no=config.end_frame_no
with open(file_path,'r') as file:
  _rotation=rotation.getNetRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=method)
print(_rotation)  

