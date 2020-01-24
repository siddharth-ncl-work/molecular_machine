__version__='1.0.0'

test_file_path='/home/vanka/ruchi/output_only/system3/system3_a/system3_a_md_29_12_19.xyz'
input_parent_dir_path='/home/vanka/ruchi/output_only'
input_system_name='system3'
input_subsystem_name='system3_a'
input_file_name='system3_a_md_29_12_19.xyz'
output_parent_dir_path='output'

#GENERAL PARAMETERS
ring_start_atom_no=0
ring_end_atom_no=63#63#19
track_start_atom_no=64#64#20
track_end_atom_no=153#153#37

start_frame_no=0
end_frame_no=1000#272849
step_size=10

r=2
simulation_time_step=0.5 #in femto
frame_no_pos=2
rotation_method='rot_part_atomic_r_t_3'
translation_method='trans_com'
RKE_method='energy_rot_hybrid_1'
TKE_method='energy_trans_com'
axis='x'

tasks='0'


#FUTURE TASKS:
# 1. rot_part_atomic_r_t_3: Implement new method for track rotation in which track rotation is calcuated using the atoms near/inside the ring
# 2. Verify on rigid real ring and track
# 3. Identify and verify method which works on real systems
# 4. Triple axis test

