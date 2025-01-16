# Filename: format_CBCT_dirnames.py
# Author: Kayla O'Sullivan-Steben
# Created: June 29, 2023
# Description: 	Changes CBCT directory name formatting from the newer version of Varian Eclipse (v18) to older versions for consistency.
#				These names are automatically generated by the TPS. Below are the formats, where 01 can be any 1 or 2 digits and c can be any letter.
# 				-----> Eclipse v18: kVCBCT_01c01
# 				-----> Older version(s): kv_CBCT_1c   (though this code would convert it to kV_CBCT_01c, with the extra 0)

# Import statements
import os,sys, platform
from config import config

system = platform.system()


def find_bad_CBCT_files(patient_path):
	"""
	find_bad_CBCT_files finds incorrectly formatted dircetories. Here, incorrectly formatted names contain 
						'kVCBCT' and are 21 chars long.

	:param patient_path: Path to patient directory.
	:return: list of directories.
	"""

	dir_list = [f for f in os.listdir(patient_path) if 'kVCBCT' in f and len(f)==21]
	return dir_list

def reformat_file_name(patient_path,old_name):
	"""
	reformat_file_name Renames file or directory to new format, which here is date_kV_CBCT_fx

	:param patient_path: Path to patient directory.
	:param old_name: Current directory or file name to be changed.
	"""
	date = old_name[0:8]
	fx = old_name[16:-2]
	new_name = date+"_kV_CBCT_"+fx
	print(old_name +" ------> " +new_name)

	if system == "Windows":
		os.system("move "+patient_path+old_name+" " + patient_path+new_name)
	else:
		os.system("sudo mv " + patient_path+old_name+" " + patient_path+new_name)


def reformat_directory(patient_path):
	"""
	reformat_directory Loops through each image directory in patient directory and rename.

	:param patient_path: Path to patient directory.
	"""

	dirs = find_bad_CBCT_files(patient_path)
	if dirs == []: # If no bad dirs found
		print("OK")
	for d in dirs:
		reformat_file_name(patient_path,d)

def reformat_multiple_patients(list_patients,PATH):
	"""
	reformat_multiple_patients Loops through each patient and calls reformatting function.

	:param list_patients: List of patient dirctories to go through. 
	:param PATH: General path to patient directories.
	"""
	
	for patient in list_patients:
		print("================================================================================")
		print("Patient ", patient)
		print("--------------------------------------------------------------------------------")
		patient_path = PATH + str(patient) + "/"

		reformat_directory(patient_path,system)

	

def main():

	
	PATH = PATH = config['PATH'] # Path to patient directories
	list_patients_to_reformat = [] # Patient directories to reformat

	if len(sys.argv[1:]) == 0:
		print("WARNING: No files checked for formatting.")#to do raise actual warning
		print("Please specify patient directory(ies) or write 'all' to check all patients.")
	
	for patient in sys.argv[1:]:
		if patient.lower() == "all":
			ignore_pt_terms = config['ignore_keywords_in_pt_dirname']
			if len(ignore_pt_terms) == 0: 
				list_patients_to_reformat = sorted([f for f in os.listdir(PATH)])
			else:
				list_patients_to_reformat = sorted([f for f in os.listdir(PATH) 
					if all(substring.lower() not in f.lower() for substring in ignore_pt_terms)])#,key=int
			
			# list_patients_to_reformat = sorted([f for f in os.listdir(PATH) if 'b' not in f and 'old' not in f],key=int)

		# Check if command line arguments correspond to existing patient directories
		elif os.path.exists(PATH+patient):
			list_patients_to_reformat.append(patient)
		else:	
			print("Patient directory "+ PATH+patient + " does not exist.")
	

	reformat_multiple_patients(list_patients_to_reformat, PATH)    

if __name__ == "__main__":
    main()