__version__='1.0.0'

#test_file_path='/home/vanka/ruchi/output_only/system3/system3_a/system3_a_md_29_12_19.xyz'
test_file_path='/home/vanka/ruchi/output_only/system1/system1_a/system1_a_30_1_20.xyz'


input_parent_dir_path='/home/vanka/ruchi/output_only'
input_system_name='system1'
input_subsystem_name='system1_ring'
input_file_name='ring1_md_30_1_20.xyz'
output_parent_dir_path='output'

#GENERAL PARAMETERS
ring_atom_no=0
track_atom_no=144

#ring_start_atom_no=0
#ring_end_atom_no=19#63#19
#track_start_atom_no=20#64#20
#track_end_atom_no=37#153#37

start_frame_no=0
end_frame_no=100000#272849
step_size=10

track_range=2
simulation_time_step=0.5 #in femto
frame_no_pos=2
rotation_method='rot_part_atomic_r_t_3'
translation_method='trans_com'
RKE_method='energy_rot_hybrid_1'
TKE_method='energy_trans_com'
axis='x'

tasks=''

ring_atom_no_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]

track_atom_no_list=None

code_dir_path='/home/vanka/siddharth/molecular_machines_project/molecular_machines'


'''
NOTE COMMIT:
 comment on y,z rotational components: Earlier I thought to include y,z rotational components as well but after thinking for a while, it was realised that its a bit tricky task. So we decided to include y,z rotational components in the next version and focus only on one component(x-axis rotation) in this version. 
  I though y and z components are the just P and Y components respectively but they are not the same. Here as we calcuate RPY angles between projections perpendicular to x-axis,so P and Y components are always zero. In order to get y and z rotational components we need to calculate RPY angles between projections perpendicular to respective axis. But this raises another question, are x,y and z rotational components obtained by calculating RPY angles between respective projections same as actual RPY angles? In other words if apply these components to a point will transfrom to its final position?

FUTURE TASKS:
 1. Think about other RPY components. Maybe a good method will have small P,Y components
 2. real system test: rotation vs step_sizse, rotation vs range
 3. Make code run faster for data generation
 4. cog/com
 5. use networkx to get ring and track
 6. modify assessment and respective test files to include artificial,semi_real,real systems
'''
