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
