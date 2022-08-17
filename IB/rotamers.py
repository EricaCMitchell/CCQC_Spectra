#!/bin/python
import numpy as np
import os
import sys

def partition_xyz(crot):
	'''
	Parses a Molden formatted geometries file 
	to separate each geometry returning a
	list of lists
	'''
	with open(crot) as f:
		full = [line.split() for line in f]
	
	natom = int(full[0][0])
	lines = len(full)
	molecs = int(lines / (natom+2))
	
	rotamers = [] 
	start = 2
	for i in range(molecs):
		rotamers.append(np.array(full[start:start+natom][:]))
		start += natom + 2

	return rotamers

def xyz_string(geom):
	'''
	Takes a geometry from a list of lists 
	an converts it into a formatted string
	'''	
	string = ""
	for i in range(len(geom)):
		string += "\n {:^2} {:^20.10f} {:^20.10f} {:^20.10f}".format(geom[i][0],\
		float(geom[i][1]),float(geom[i][2]),float(geom[i][3]))
	return string 

def create_inputs(rots,directory,temp):
	'''
	Creates the directories where all
	the Psi4 input files with the appropriate geometry
	will be located, $DIR_NAME/ROTS_#
	'''
	for i in range(len(rots)):
		path = os.path.join(directory + '/ROTS_' + str(i) + '/') 
		os.makedirs(path)
		with open('{:s}input.dat'.format(path),'w') as f:
			f.write(temp.format(xyz_string(rots[i])))

if __name__ == "__main__":
	# Template relies on the absolute path to the correct input file for a geometry optimization
	#template = open('/home/vulcan/ecm23353/Research/4_Rotavera/init/bin/molpro_geom.dat').read()
	template = open('/home/vulcan/ecm23353/Research/4_Rotavera/init/bin/psi4_geom.dat').read()
	directory = 'ROTAMERS'
	rotamers = partition_xyz('crest_rotamers.xyz')
	create_inputs(rotamers,directory,template)

