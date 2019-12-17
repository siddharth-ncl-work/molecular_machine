from source import rotation,translation,energy
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
  _rotation=rotation.getRotation(file,config.t2_frame1_no,config.t2_frame2_no,type='relative')
  print(_rotation)

def task3():
  file=open(config.test_file_path)
  _rotation=rotation.getNetRotation(file,config.t3_frame1_no,config.t3_frame2_no,part1='ring',type='absolute')
  print(_rotation)

def task4():
  file=open(config.test_file_path)
  _rotation=rotation.getNetRotation(file,config.t4_frame1_no,config.t4_frame2_no,type='relative')
  print(_rotation)

def task5():
  file=open(config.test_file_path)
  _translation=translation.getNetTranslation(file,config.t5_frame1_no,config.t5_frame2_no,type='relative')
  print(_translation)

def task6():
  file=open(config.test_file_path)
  _translation=translation.getTranslation(file,config.t6_frame1_no,config.t6_frame2_no,type='absolute',part1='ring')
  print(_translation)

def task7():
  file=open(config.test_file_path)
  _translation=translation.getTranslation(file,config.t7_frame1_no,config.t7_frame2_no,type='absolute',part1='track')
  print(_translation)

def task8():
  file=open(config.test_file_path)
  _energy=energy.getTKE(file,config.t8_frame1_no,config.t8_frame2_no,type='absolute',method='energy_trans_com')
  print(_energy)




tasks={'0':task0,'1':task1,'2':task2,'3':task3,'4':task4,'5':task5,'6':task6,'7':task7,'8':task8}

for task_no in config.tasks.split('+'):
  tasks[task_no]()
  

