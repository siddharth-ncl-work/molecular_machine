import networkx as nx
import subprocess
import matplotlib.pyplot as plt
import sys
sys.path.extend(['.','..'])

from lib.io_chem import io
import config


def isMd(file_path):
  with open(file_path,'r') as file:
    for i in range(10):
      line=file.readline()
      if 'frame' in line:
        return True
  return False

def extractMolecule(file_path,atom_no=0):
  if isMd(file_path):
    with open(file_path,'r') as file:
      df_cords=io.readFileMd(file,config.start_frame_no,frame_no_pos=config.frame_no_pos)
  else:
    df_cords=io.readFile(file_path)
  io.writeFile('ring_track_frame.tmp.xyz',df_cords) 
  subprocess.run(['babel','ring_track_frame.tmp.xyz','ring_track_frame.tmp.mol']) 
  G=io.readFile('ring_track_frame.tmp.mol',info='graph')
  subprocess.run(['rm','ring_track_frame.tmp.xyz','ring_track_frame.tmp.mol'])
  cc_list=list(nx.connected_component_subgraphs(G))
  print(f'number of molecules found is {len(cc_list)}')
  for cc in cc_list:
    if atom_no in list(cc.nodes):
      return sorted(list(cc.nodes))
      
    #print(list(cc.nodes))
    #pos=nx.spring_layout(cc)
    #nx.draw_networkx(cc,pos,labels=nx.get_node_attributes(cc,'element'))
    #plt.show()


if __name__=='__main__':
  file_path='verification/test_systems/ring_track_two_frames_non_ideal_artificial_system.xyz'
  #file_path=config.test_file_path
  print(f'ring: {extractMolecule(file_path,atom_no=config.ring_atom_no)}')
  print(f'track: {extractMolecule(file_path,atom_no=config.track_atom_no)}')
