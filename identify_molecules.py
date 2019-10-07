from source.frame_class import frame_class
import networkx as nx
import networkx.algorithms.isomorphism as iso
from param.gen_params import coll_steps,non_coll_steps
from source.shared_methods import found,addUnique

def findInFrame(molecule,frame):
  insts=[]
  G=frame.frame_graph
  H=molecule.mol_graph
  nm=iso.categorical_node_match('element','C')
  for sg in list(nx.connected_component_subgraphs(G)):
    GM=iso.GraphMatcher(H,sg,node_match=nm)
    if GM.is_isomorphic():
      insts.append(sg)
  
  return found(frame.frame_no,insts)

def identifyMolecules(molecule,file_name,start_frame_no=0,end_frame_no=100000,inc=1):
  found_molecules_list=[]
  curr_list=[]
  file=open(file_name,'r')
  for frame_no in range(start_frame_no,end_frame_no+1,inc):
    frame=frame_class(file,frame_no)
    if frame.frame_no==-1:
      continue
    #print "At frame "+str(frame_no)
    found_molecules=findInFrame(molecule,frame)
    is_added=addUnique(found_molecules_list,found_molecules)
    if is_added:
      print found_molecules    
  return found_molecules_list

def getUniqueFoundObj(found_objs):

  """
  first occurence of non-zero unique found objects
  """
  filtered_found_objs=[]
    
  for f in found_objs:
    if f._no_of_insts!=0:   
     filtered_found_objs.append(f)
     break

  for f in found_objs:
    if f._no_of_insts!=0:
     present=False
     for ff in filtered_found_objs:
       if ff.isEqual(f):
         present=True
         break
     if not present:
       filtered_found_objs.append(f)
 
  return filtered_found_objs

def getUniqueMolecules(found_objs):
  unique_mols=[]

  for f in found_objs:
    if f._no_of_insts!=0:
     for G in f._insts:
       unique_mols.append((f._frame_no,G))
     break

  for f in found_objs:
    for G in f._insts:
      present=False
      for H in unique_mols:
        if set(G.nodes())==set(H[1].nodes()):
          present=True
          break
      if not present:
        unique_mols.append((f._frame_no,G))

  return unique_mols

"""
#new_new
def addUniqueIdentify(final_list,found):
  if len(final_list)==0:
    final_list.append(found)
    return True

  if not final_list[-1].isEqual(found):
    final_list.append(found)
    return True
  else:
   return False

#new
def addUniqueIdentify1(curr_list,final_list,found):
  if len(final_list)==0:
    for G in found[2]:
      final_list.append((found[0],G))
    return

  for H in found[2]:
    present=False
    for G in final_list:
      if set(G[1].nodes())==set(H.nodes()):
          present=True
          break
    if not present:
      final_list.append((found[0],H))

#old
def addUniqueIdentify0(curr_list,final_list,found):
  if len(found)!=0:
    print 'tracking '+str(found[0])

  if len(found)!=0 and len(curr_list)==0:
    for G in found[2]:
      curr_list.append((found[0],G))
    return

  if len(found)!=0 and len(found[2])!=0:
    for index,G1 in enumerate(curr_list):
      present=False
      for G2 in found[2]:
        print 'nodes'
        print set(G1[1].nodes())
        print set(G2.nodes())
        if set(G1[1].nodes())==set(G2.nodes()):
          print 'yes'
          present=True
          break
      print not present
      if not present:
        print 'yes2'
        final_list.append(G1)
        curr_list.pop(index)

    for G2 in found[2]:
      present=False
      for G1 in curr_list:
        if set(G1[1].nodes())==set(G2.nodes()):
          present=True
          break
      if not present:
        curr_list.append((found[0],G2))

  if len(found)!=0 and found[0]>=end_frame:
    final_list.extend(curr_list)
"""
