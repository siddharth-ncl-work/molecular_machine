from source import rotation
import config

def task0():
  file=open(config.test_file_path)
  _rotation=rotation.getRotation(file,config.t0_frame1_no,config.t0_frame2_no,part1='ring')
  print(_rotation)
 
def task1():
  file=open(config.test_file_path)  
  _rotation=rotation.getRotation(file,config.t1_frame1_no,config.t1_frame2_no,part1='track')
  print(_rotation)

def task2():
  file=open(config.test_file_path)
  _rotation=rotation.getNetRotation(file,config.t2_frame1_no,config.t2_frame2_no,part1='ring',type='absolute')
  print(_rotation)

def task3():
  file=open(config.test_file_path)
  _rotation=rotation.getNetRotation(file,config.t3_frame1_no,config.t3_frame2_no,type='relative')
  print(_rotation)

tasks={'0':task0,'1':task1,'2':task2,'3':task3}

for task_no in config.tasks.split('+'):
  tasks[task_no]()
  

