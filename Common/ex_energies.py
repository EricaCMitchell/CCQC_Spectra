#!/bin/python
import numpy as np
import re
import os

def grab_psi4(out):
	'''
	Parses a Psi4 output file and 
	grabs the final optimized geometry
	returning it as a string
	'''
	full = open(out).readlines()

	i = 0
	num = 0
	natom = 0
	for line in reversed(full):
		if re.search('Final optimized geometry and variables:',line) != None:
			num = len(full) - i + 5
			natom = i - 13
			break	
		i += 1
	
	geom_list = full[num:num+natom]
	geom = ""	
	for i in geom_list:
		geom += i	
	
	return geom

def create_inputs(rots,directory,temp):
	'''
	Creates the directories where all
	the QChem input files with the appropriate optimized geometry
	will be located, $DIR_NAME/ROTS_#
	'''
	for i in range(len(rots)):
		path = os.path.join(directory + '/ROTS_' + str(i) + '/') 
		os.makedirs(path)
		with open('{:s}input.dat'.format(path),'w') as f:
			f.write(temp.format(rots[i]))

def check_geoms(rots):
	'''
	Creates a molden formatted file 
	so all optimized geometries can be viewed
	and visually compared
	'''
	natom = len(rots[0].split('\n')) - 1 
	f = open('opt_geoms.xyz','w')
	for i in range(len(rots)):
		f.write(str(natom) + '\n\n')
		f.write(rots[i])

if __name__ == "__main__":
	# Template uses the absolute path to the energy.dat file
	opt_geoms = []
	template = open('/scratch/ecm23353/3_Rotavera/bin/energy.dat').read()

	n = int(input("Enter number of ROTS_#: "))
	for i in range(n):
		opt_geoms.append(grab_psi4('ROTS_' + str(i) + '/output.dat'))

	check_geoms(opt_geoms)
	
	create_inputs(opt_geoms,'ENERGY',template)
		
