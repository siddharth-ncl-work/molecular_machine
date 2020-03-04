__version__='2.1.0'

test_file_path='/home/vanka/ruchi/output_only/system3/system3_a/system3_a_md_29_12_19.xyz'

#GENERAL PARAMETERS
input_parent_dir_path="/home/vanka/ruchi/molecular_motor"
input_system_name="case_3"
input_subsystem_name="ring_track_dl_nutral_nh"
input_scr_dir_name="scr_1700_temp"
output_parent_dir_path='output'

ring_atom_no=4
track_atom_no=104
ref_axis_atom1_no=118
ref_axis_atom2_no=104

start_frame_no=0
end_frame_no=100
step_size=10
frame_no_pos=2

tasks='5'

#INTERNAL PARAMETERS
track_range=20
simulation_time_step=0.5 #in femto

rotation_method='rot_part_atomic_r_t_3'
translation_method='trans_com_2'
RKE_method='energy_rot_hybrid_1'
TKE_method='energy_trans_com'
axis='x'
show_plot=False

ring_atom_no_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

track_atom_no_list=[64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154]

code_dir_path='/home/vanka/siddharth/molecular_machines_project/molecular_machines'

'''
* add coneAssessment method in assessment_of_methods.py 
  coneAssessment: shows out-of-plane contributions to x-axis rotation due to rotation along one of the y- or z-axis.This behaviour was expected before but never seen during verification. when Atom moves on the surface of the cone, it contribute to the x-axis rotation. Track has a lot of this kind of atoms

* add task3,task4 and task5:
  task3: Rotational Directionality: Direct Relative Rotation of the ring between two frames/time steps
  task4: Translational Directionality: Direct Relative Translation of the ring between two frames/time steps
  task5: Robustness Test wrt 'step_size' parameter: Ring Net Relative Rotation Vs step_size
'''
