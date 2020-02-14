__version__='1.1.0'

test_file_path='/home/vanka/ruchi/output_only/system3/system3_a/system3_a_md_29_12_19.xyz'

#GENERAL PARAMETERS
input_parent_dir_path="/home/vanka/ruchi/output_only"
input_system_name="system2"
input_subsystem_name="system2_a"
output_parent_dir_path='output'

ring_atom_no=0
track_atom_no=236
ref_axis_atom1_no=95
ref_axis_atom2_no=178

start_frame_no=20
end_frame_no=99
step_size=10
frame_no_pos=1

tasks='0+2'

#INTERNAL PARAMETERS
track_range=2
simulation_time_step=0.5 #in femto

rotation_method='rot_part_atomic_r_t_3'
translation_method='trans_com_2'
RKE_method='energy_rot_hybrid_1'
TKE_method='energy_trans_com'
axis='x'
show_plot=False

ring_atom_no_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]

track_atom_no_list=[68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238]

code_dir_path='/home/vanka/siddharth/molecular_machines_project/molecular_machines'

'''
* make code ready for data generation according to new data location
* add task to get rotation and traslation data simultaneously
* add feature to get absolute data during relative data calculation
* update 1.1.0 tag
* update data-1.1.0 with new traslation data
'''
