#!/home/vulcan/ecm23353/.conda/envs/py38/bin/python3

import sys
import re
import numpy as np
import pandas as pd
from scipy import integrate
sys.path.append('/home/vulcan/ecm23353/bin/')
from spectrum import spectrum
np.set_printoptions(precision=7,threshold=sys.maxsize)

def get_info():
	'''
	Retrieves the excitation energy in Hartree
	and calculates the magnitude of the
	electric dipole transition moment
	'''
	ee = []
	tm = []
	mult = []
	#os = []
	ref_e = 0.0
	with open('output.dat') as f:
		for line in f:
			if re.search("CCSD total energy",line) != None:
				ref_e += float(line.split()[-1])
			if re.search("Total energy =",line) != None:
				ee.append(float(line.split()[3]) - ref_e)
			if re.search("A->B",line) != None and re.search("X",line) != None:
				vals = line.split()
				tm.append(float(vals[1]))
			#if re.search("Oscillator strength",line) != None:
			#       os.append(float(line.split()[3]))

	k = 0
	for i,j in enumerate(mult):
		if j == "Triplet":
			ee.pop(i - k)
			tm.pop(i - k)
			k += 1

	return np.array(ee), np.array(tm)

def similarity(x, y, min_eV, max_eV):
	df = pd.read_excel('/home/vulcan/ecm23353/Research/3_AB/bin/cross-secs-Sept2021.xlsx', sheet_name="water")
	exp_x = df['E (eV)']
	exp_y = df['s (Mb)']	

	sim_x = []
	sim_y = []
	sim_exp_x = []
	sim_exp_y = []
	for i in range(len(exp_x)):
		for j in range(len(x)):
			lower = exp_x[i] - 0.0005
			upper = exp_x[i] + 0.0005
			if lower <= x[j] <= upper and exp_x[i] not in sim_exp_x:
				sim_x.append(x[j])
				sim_y.append(y[j])
				sim_exp_x.append(exp_x[i])
				sim_exp_y.append(exp_y[i])
			if lower <= x[j] <= upper and exp_x[i] in sim_exp_x:
				sim_x[-1] = (sim_x[-1] + x[j]) / 2
				sim_y[-1] = (sim_y[-1] + y[j]) / 2

	for i in range(len(sim_exp_x)):
		if sim_exp_x[i] > max_eV:
			max_index = i
		if sim_exp_x[i] < min_eV:
			min_index = i
			break
	x_vals = sim_x[max_index:min_index]
	y_vals = sim_y[max_index:min_index]
	exp_x_vals = sim_exp_x[max_index:min_index]
	exp_y_vals = sim_exp_y[max_index:min_index]

	zip_1 = zip(x_vals, y_vals)	
	zip_2 = zip(exp_x_vals, exp_y_vals)	
	sorted_1 = sorted(zip_1)
	sorted_2 = sorted(zip_2)
	tuples_1 = zip(*sorted_1)
	tuples_2 = zip(*sorted_2)
	x_vals, y_vals = [ np.array(tuple) for tuple in tuples_1 ]
	exp_x_vals, exp_y_vals = [ np.array(tuple) for tuple in tuples_2 ]

	num = integrate.simpson(y_vals * exp_y_vals, exp_x_vals) 
	denom_1   = integrate.simpson(y_vals * y_vals, exp_x_vals)
	denom_2   = integrate.simpson(exp_y_vals * exp_y_vals, exp_x_vals)
	cos_sim = (num / np.sqrt(denom_1 * denom_2))

	numerator = integrate.simpson(abs(y_vals - exp_y_vals), exp_x_vals)
	denom = integrate.simpson(exp_y_vals, exp_x_vals)
	ric = numerator / denom

	return cos_sim, ric

if __name__ == "__main__":
	# Change eV to fit FWHM
	#val = float(input("Enter Gamma: "))
	val = 0.30
	eV2Eh = val / 27.21138602

	poles, opa_residues = get_info()
	opa_spectrum = spectrum(poles=poles, residues=opa_residues, gamma=eV2Eh, out_units="eV")

	x_vals = opa_spectrum["convolution"]["x"]
	y_vals = opa_spectrum["convolution"]["y"]

	s, ric = similarity(x_vals, y_vals, 8.75, 9.25)
	x = os.getcwd()
	print(" {:10}  {: .14f}  {: .14f}".format(os.path.split(os.path.split(x)[0])[1], s, ric))
