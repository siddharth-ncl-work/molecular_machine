import sys
sys.path.extend(['.','..'])

import config
from source import rotation,translation,init

file_path=config.test_file_path
init.initConfig(file_path)
rotation_method=config.rotation_method
translation_method=config.translation_method
frame1_no=config.start_frame_no
frame2_no=config.end_frame_no

print(f'frame1 = {frame1_no}\nframe2 = {frame2_no}')
#rotation
'''
with open(file_path,'r') as file:
  _rotation=rotation.getNetRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=rotation_method)
  print(_rotation)
with open(file_path,'r') as file:
  _rotation=rotation.getRotation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=rotation_method)
  print(_rotation)
'''
#translation
with open(file_path,'r') as file:
  _translation=translation.getTranslation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=translation_method) 
  print(f'ring direct absolute translation = {_translation}')
with open(file_path,'r') as file:
  _translation=translation.getTranslation(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=translation_method)
  print(f'track direct absolute translation = {_translation}')
with open(file_path,'r') as file:
  _translation=translation.getTranslation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=translation_method)
  print(f'ring direct relative translation = {_translation}')
with open(file_path,'r') as file:
  _translation=translation.getNetTranslation(file,frame1_no,frame2_no,part1='ring',part2='track',type='absolute',method=translation_method,step_size=config.step_size)
  print(f'ring net absolute translation = {_translation[0]}')
with open(file_path,'r') as file:
  _translation=translation.getNetTranslation(file,frame1_no,frame2_no,part1='track',part2='track',type='absolute',method=translation_method,step_size=config.step_size)
  print(f'track net absolute translation= {_translation[0]}')
with open(file_path,'r') as file:
  _translation=translation.getNetTranslation(file,frame1_no,frame2_no,part1='ring',part2='track',type='relative',method=translation_method,step_size=config.step_size)
  print(f'ring net relative translation = {_translation[0]}')

