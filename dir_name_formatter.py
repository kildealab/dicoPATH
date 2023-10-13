
import os,sys
# TO DO: This only works for my specific case. Will make general to change any format.

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

def refomat_multiple_patients(list_patients,PATH):
	"""
	refomat_multiple_patients Loops through each patient and calls reformatting function.

	:param list_patients: List of patient dirctories to go through. 
	:param PATH: General path to patient directories.
	"""
	
	for patient in list_patients:
		print("================================================================================")
		print("Patient ", patient)
		print("--------------------------------------------------------------------------------")
		patient_path = PATH + str(patient) + "/"

		reformat_directory(patient_path)

	


if __name__ == "__main__":
	
	PATH = '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/' # Path to patient directories
	list_patients_to_reformat = [] # Patient directories to reformat

	
	for patient in sys.argv[1:]:
		if patient == "all":
			list_patients_to_reformat = sorted([f for f in os.listdir(PATH)],key=int)

		# Check if command line arguments correspond to existing patient directories
		elif os.path.exists(PATH+patient):
			list_patients_to_reformat.append(patient)
		else:	
			print("Patient directory "+ PATH+patient + " does not exist.")
	

	refomat_multiple_patients(list_patients_to_reformat, PATH)    

	
