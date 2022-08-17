#!/home/vulcan/akb95494/.conda/envs/py38/bin/python3

import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
sys.path.append('/home/vulcan/akb95494/bin/excited_states')
from spectrum import spectrum
np.set_printoptions(precision=7,threshold=sys.maxsize)

def get_info(d):
	'''
	Retrieves the excitation energy in Hartree
	and calculates the magnitude of the
	electric dipole transition moment
	'''
	ee = []
	tm = []
	os = []
	ref_e = 0.0
	with open(d+'/output.dat') as f:
		for line in f:
			if re.search("Total energy in the final",line) != None:
				ref_e = float(line.split()[-1])
			if re.search("Total energy for state",line) != None:
				ee.append(float(line.split()[-2]) - ref_e)
			if re.search("Trans. Mom.",line) != None:
				vals = line.split()
				x = float(vals[2])
				y = float(vals[4])
				z = float(vals[6])
				tm.append(np.linalg.norm([x,y,z]))
				#tm.append(np.linalg.norm([x,y,z]))
			#if re.search("Strength   :",line) != None:
				#os.append(float(line.split()[-1]))
	return np.array(ee), np.array(tm)

def reg_plot(x,y,p,r):
	'''
	Creates a plot with both the theoretical spectra and
	experimental spectra overlaid on top of the computed poles
	'''
	# df uses the absolute path to the 3-butenal experimental results (butanal.csv)
	df = pd.read_excel('/home/vulcan/ecm23353/Research/3_AB/bin/cross-secs-Sept2021.xlsx', sheet_name="")
	exp_x = df['E (eV)']
	exp_y = df['s (Mb)']	

	plt.rcParams.update({
	    "figure.titlesize": 24,
	    "axes.titlesize": 20,
	    "axes.labelsize": 16,
	    "xtick.labelsize": 14,
	    "ytick.labelsize": 14
	    })

	plt.figure(figsize=(10,8))
	plt.title(r'TD-functional/d-aug-cc-pVTZ for 1-Propanol'+' \n')
	plt.plot(x,y,label="TD-functional/d-aug-cc-pVTZ")
	plt.bar(p,r,0.007,color='tab:red')
	plt.plot(exp_x,exp_y,label='Experimental',color='k')

	plt.xlim([5.2,7.1])
	plt.xlabel("Energy (eV)")
	plt.ylabel("Absorption Cross Section (Mb)")
	plt.savefig("functional.png")
	plt.close()

def th_expt_plot(x,y,p,r):
	'''
	Creates a series of plots
	A plot with just the computed poles,
	A plot with only theoretical spectra and the poles,
	And a plot comparing theoretical and experimental spectra overlaying the computed poles
	'''
	# df uses the absolute path to the 3-butenal experimental results (butanal.csv)
	df = pd.read_excel('/home/vulcan/ecm23353/Research/3_AB/bin/cross-secs-Sept2021.xlsx', sheet_name="")
	exp_x = df['E (eV)']
	exp_y = df['s (Mb)']	

	plt.rcParams.update({
	    "figure.titlesize": 24,
	    "axes.titlesize": 20,
	    "axes.labelsize": 16,
	    "xtick.labelsize": 14,
	    "ytick.labelsize": 14
	    })
	
	fig, axs = plt.subplots(1,3,figsize=(20,7),sharey=True)
	fig.subplots_adjust(top=0.85,wspace=0.5)
	axs[0].bar(p_vals,r_vals,0.007,color='tab:red')
	axs[1].bar(p_vals,r_vals,0.007,color='tab:red')
	axs[1].plot(x_vals,y_vals)
	axs[2].bar(p_vals,r_vals,0.007,color='tab:red')
	axs[2].plot(x_vals,y_vals,label="TD-functional/d-aug-cc-pVTZ")
	axs[2].plot(exp_x,exp_y,label='Experimental',color='k')
	fig.suptitle(r'TD-functional/d-aug-cc-pVTZ and Experimental Data Comparison'+' \n')
	axs[0].set_title('Computed Poles')
	axs[0].set_ylabel("Absorption Cross Section (Mb)\n")
	axs[0].set_xlabel("Energy (eV)")
	axs[0].set_xlim([5.2,7.1])
	axs[1].set_title('Theoretical Spectra')
	axs[1].set_xlabel("Energy (eV)")
	axs[1].set_xlim([5.2,7.1])
	axs[2].set_title('Theoretical and Experimental Spectra')
	axs[2].set_xlabel("Energy (eV)")
	axs[2].set_xlim([5.2,7.1])
	
	plt.tight_layout()
	plt.savefig("Theory_Expt_functional.png")
	plt.close()


if __name__ == "__main__":
	# Change eV to fit FWHM
	val = float(input("Enter Gamma: "))
	eV2Eh = val / 27.21138602

	poles, opa_residues = get_info(d)
	opa_spectrum = spectrum(poles=poles, residues=opa_residues, gamma=eV2Eh, out_units="eV")
	x_vals = opa_spectrum["convolution"]["x"]
	y_vals = opa_spectrum["convolution"]["y"]
	p_vals = opa_spectrum["sticks"]["poles"]
	r_vals = opa_spectrum["sticks"]["residues"])

	reg_plot(x_vals,y_vals,p_vals,r_vals)

