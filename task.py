from source import rotation
import config

def task0():
  file=open(config.test_file_path)
  _rotation=rotation.getRotation(file,config.t0_frame1_no,config.t0_frame2_no,part1='ring')
  print(_rotation)


tasks={'0':task0}

for task_no in config.tasks.split('+'):
  tasks[task_no]()
  

