__version__='1.0.0'

data_dir_path='/home/vanka/ruchi/output_only'
system_name='system3'
file_name='system2_21_11_19_v1.xyz'

test_file_path='verification/test_systems/ring_track_multi_frame_ideal.xyz'#'/home/vanka/ruchi/output_only/system3/ring_track_dl_at_sulfer_end.xyz'

#GENERAL PARAMETERS
ring_start_atom_no=0#0
ring_end_atom_no=19#63

track_start_atom_no=20#64
track_end_atom_no=37#153

axis='x'

simulation_time_step=0.5 #in femto

frame_no_pos=2

tasks='0+1+2+3+4+5+6+7+8+9'

#TASK 0 
#Calculate absolute rotation of ring between two frames
t0_frame1_no=0
t0_frame2_no=1

#TASK 1
#Calculate absolute rotation of track between two frames
t1_frame1_no=0
t1_frame2_no=1

#TASK 2
#Calculate relative rotation of track between two frames
t2_frame1_no=0
t2_frame2_no=1

#TASK 3
#Calculate net absolute rotation of ring  between two frames
t3_frame1_no=0
t3_frame2_no=10

#TASK 4
#Calculate net relative rotation of ring  between two frames
t4_frame1_no=0
t4_frame2_no=1

#TASK 5
#Calculate net relative translation of ring  between two frames
t5_frame1_no=0
t5_frame2_no=1

#TASK 6
#Calculate absolute translation of ring  between two frames
t6_frame1_no=0
t6_frame2_no=1

#TASK 7
#Calculate absolute translation of ring  between two frames
t7_frame1_no=0
t7_frame2_no=1

#TASK 8
#Calculate absolute RKE of ring
t8_frame1_no=0
t8_frame2_no=5

#TASK 9
#Calculate absolute TKE of ring
t9_frame1_no=0
t9_frame2_no=5
