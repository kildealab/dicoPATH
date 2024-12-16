import os, sys, time
import pydicom as dcm
from config import config

# dict_class_UID contains image class UIDs and their abbreviations. 
# At the moment, it contains CT, MR, PE and RI UIDs, but more can be added.
# List of image class UIDs: https://dicom.nema.org/dicom/2013/output/chtml/part04/sect_B.5.html
dict_class_UID = {'1.2.840.10008.5.1.4.1.1.2': 'CT', 
				  '1.2.840.10008.5.1.4.1.1.481.1': 'RI', 
				  '1.2.840.10008.5.1.4.1.1.4': 'MR', 
				  '1.2.840.10008.5.1.4.1.1.128':'PE'}


def remove_RI_RT_files(PATH):
	"""
	remove_RI_RT_files Sorts the DICOM RT Image files (and associated registration files) into directory "RI"
					   and DICOM RT Treatment Record files into directory "RT". 
					   Note: This can be changed to delete the files entirely if not needed.

	:param PATH: Path to patient directory.
	"""

	# Counts for the number of each file type moved
	RI_count = 0
	RT_count = 0
	RE_count = 0
	
	file_list = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) if 'RI' in f or 'RT' in f or 'RE' in f]

	# Create RT and RI directories if they don't exist
	RT_path = PATH + "RT"
	if not os.path.exists(RT_path):
		os.system("sudo mkdir " + RT_path)
		print("Created directory "+RT_path)

	RI_path = PATH + "RI"
	if not os.path.exists(RI_path):
		os.system("sudo mkdir " + RI_path)
		print("Created directory "+RI_path)
	
	# Go through each file in list and move into associated directory
	for file in file_list:
		if 'RT' in file:
			os.system("sudo mv " + PATH+file +" " + RT_path+"/"+file)
			RT_count += 1
		
		elif 'RI' in file:
			os.system("sudo mv " + PATH+file +" " + RI_path+"/"+file)
			RI_count += 1
		
		elif 'RE' in file:
			# Check if registration file is referencing an "RI" image file
			RE_class = dcm.read_file(PATH+file).ReferencedSeriesSequence[0].ReferencedInstanceSequence[0].ReferencedSOPClassUID
			if dict_class_UID[RE_class] == 'RI':
				os.system("sudo mv " + PATH+file +" " + RI_path+"/"+file)
				RE_count += 1
	print("--------------------------------------------------------------------------------")
	print("Files moved: ", RT_count, " RT, ", RI_count, " RI, ",RE_count, " RE")
	print("--------------------------------------------------------------------------------")
				
def remove_non_CT_image_files(PATH):
	"""
	remove_non_CT_image_files Sorts the DICOM MRI and PET Image files into directories "MR" and "PE".
							  The scans are not sorted within these folders as they aren't needed for this project.
					   		  Note: This can be changed to delete the files entirely if not needed.
					   		  Note: Can add other image types in the same manner if they arise.

	:param PATH: Path to patient directory.
	"""

	file_list_PE = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) if 'PE' in f]
	file_list_MR = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) if 'MR' in f]
	
	num_PE = len(file_list_PE)
	num_MR = len(file_list_MR)

	# If PET or MRI files exist, create and move into associated directories
	if num_PE > 0:
		PE_path = PATH + "PE"
		if not os.path.exists(PE_path):
			os.system("sudo mkdir " + PE_path)
			print("Created directory "+PE_path)
		for file in file_list_PE:
			os.system("sudo mv "+PATH+file+" "+PE_path+"/"+file)
	
	if num_MR > 0:
		MR_path = PATH + "MR"
		if not os.path.exists(MR_path):
			os.system("sudo mkdir " + MR_path)
			print("Created directory "+MR_path)
		for file in file_list_MR:
			os.system("sudo mv "+PATH+file+" "+MR_path+"/"+file)

	if num_PE + num_MR > 0:
		print("--------------------------------------------------------------------------------")
		print("Files moved: ",num_PE, " PET, ", num_MR, " MR")
		print("--------------------------------------------------------------------------------")

			

def sort_image_files_by_RS(PATH):
	"""
	sort_image_files_by_RS Sorts the CT slice files (and associated registration files), RT Structure Set files
						   and RT Dose files into directories corresponding to each image sequence. Sorting is
						   done based on the RS file, which is associated to RD and RE files using the 
						   FrameOfReferenceUID tag, and to the CT files using the ReferencedSOPInstanceUID tag.
						   Since the CT files are named after this UID tag, this sorting method does not require 
						   opening/reading the CT files.

	:param PATH: Path to patient directory.
	"""
	# Dictionary containing the frame of reference UIDs and the associated file path they belong to
	uid_dict = {}
	
	# List of TODO
	rejected_RS = []

	# List of each file type to be moved
	list_RE = []
	list_RS = []
	list_RD = []
	list_RP = []
	other = [] # Catch-all if a new file type appears

	# Counts of each file type to be moved
	CT_count = 0
	RE_count = 0
	RS_count = 0
	RD_count = 0
	RP_count = 0#['copy', 'adap', 'planad', 'qa', 'test','pa','do not use']
	
	# Get all non-CT files
	file_list = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) if 'CT' not in f]
	
	# Creat sub-list of file types
	for file in file_list:
		if 'RE' in file:
			list_RE.append(file)
		elif 'RS' in file:
			 list_RS.append(file)
		elif 'RD' in file:
			list_RD.append(file)
		elif 'RP' in file:
			list_RP.append(file)
		else:
			other.append(file)
			
	# For each RS file, create directory and move associated CT slices
	for file in list_RS:
		d = dcm.read_file(PATH+file)

		
		new_path = PATH + d.StructureSetDate + "_" +  d.StructureSetLabel.replace(" ", "_") # New directory path: Date_Label (remove spaces from label)

		# Create new directory if not exists
		if not os.path.exists(new_path):
			os.system("sudo mkdir " + new_path)
			print("Created directory "+new_path)
	
		# Move current RS file into new directory
		os.system("sudo mv " + PATH+file +" " + new_path+"/"+file)
		RS_count += 1

		update_uid_dict = False

		# list of words to ignore in if statement below
		ignore_terms = config['ignore_keywords_in_plan'] #['copy', 'adap', 'planad', 'qa', 'test','pa','do not use']

		# Do not gather CT files for "PlanAdapt"/"QA"/"TEST" structure sets, as these are test calculations done on the planning CT
		# Note: this code keeps the PlanAdapt/QA/TEST directories, but it could be deleted as it won't be useful.
		if all(substring.lower() not in d.StructureSetLabel.lower() for substring in ignore_terms) and ((d.StructureSetLabel[-1].isdigit() and 'CBCT' not in d.StructureSetLabel) or 'kV_CBCT' in d.StructureSetLabel):
			# For each image slice referenced in RS file, move the correspondint CT file into the new directory
			# Note: the CT files are automatically named as "CT.ReferencedSOPInstanceUID.dcm"
			for img in d.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence:
				uid = img.ReferencedSOPInstanceUID 
				os_cmd = "sudo mv " + PATH+"CT."+uid+".dcm" +" " + new_path+"/"+"CT."+uid+".dcm"

				# Only increase CT count if command processed
				if os.system(os_cmd) == 0:
					CT_count += 1
			# print(d.StructureSetLabel)
			# print(len(d.StructureSetLabel))

			structset_label = d.StructureSetLabel
			if config['CT_keyword'] in structset_label and len(structset_label) >= config['CT_name_min_length'] and len(structset_label) <= config['CT_name_max_length']:
				update_uid_dict = True

		else:
			rejected_RS.append(d)

		# Save the frame of reference UID into dictionary with associated new directory path
		# Note: the RS, RD and RE files have the same FrameOfReferenceUID, so this dict is used to move RD & RE later
		frame_of_reference_uid = d.ReferencedFrameOfReferenceSequence[0].FrameOfReferenceUID
		if update_uid_dict or frame_of_reference_uid not in uid_dict:
			uid_dict.update({frame_of_reference_uid: new_path}) 


	# Once all proper CT's are sorted, go thorugh the rejected list in case remaining CT files belong to them.
	if len([f for f in os.listdir(PATH) if f[0:3] == 'CT.']) > 0:
		for d in rejected_RS:
			new_path = PATH + d.StructureSetDate + "_" +  d.StructureSetLabel.replace(" ", "_") 
			for img in d.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence:
				uid = img.ReferencedSOPInstanceUID 
				if not os.path.exists(PATH+"CT."+uid+".dcm"):
					break

				os_cmd = "sudo mv " + PATH+"CT."+uid+".dcm" +" " + new_path+"/"+"CT."+uid+".dcm"

				# Only increase CT count if command processed
				if os.system(os_cmd) == 0:
					CT_count += 1



	
	# Organize the registration (RE) files into the appropriate directories based on FrameOfReferenceUID
	for file in list_RE:
		d = dcm.read_file(PATH+file)

		for seq in d.RegistrationSequence:
			if seq.MatrixRegistrationSequence[0].MatrixSequence[0].FrameOfReferenceTransformationMatrix != [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]:
				frame_of_reference_uid = seq.FrameOfReferenceUID
		# try:
		# 	frame_of_reference_uid = d.RegistrationSequence[-1].FrameOfReferenceUID
		# except:
		# 	frame_of_reference_uid = d.FrameOfReferenceUID

		# Catch exception if RE file doesn't belong to any of the images downloaded
		try:
			os.system("sudo mv " + PATH+file +" " + uid_dict[frame_of_reference_uid]+"/"+file)
		except:
			print("could not move file ", file, " with frame of ref uid ",frame_of_reference_uid)
		else:
			RE_count += 1


	# Organize the dose (RD) files into the appropriate directories based on FrameOfReferenceUID
	for file in list_RD:
		d = dcm.read_file(PATH+file)
		frame_of_reference_uid = d.FrameOfReferenceUID

		# Catch exception if RD file doesn't belong to any of the images downloaded
		try:
			os.system("sudo mv " + PATH+file +" " + uid_dict[frame_of_reference_uid]+"/"+file)
		except:
			print("could not move file ", file, " with frame of ref uid ",frame_of_reference_uid)
		else:
			RD_count += 1

	# Organize the dose (RP) files into the appropriate directories based on FrameOfReferenceUID
	for file in list_RP:
		d = dcm.read_file(PATH+file)
		frame_of_reference_uid = d.FrameOfReferenceUID

		# Catch exception if RP file doesn't belong to any of the images downloaded
		try:
			os.system("sudo mv " + PATH+file +" " + uid_dict[frame_of_reference_uid]+"/"+file)
		except:
			print("could not move file ", file, " with frame of ref uid ",frame_of_reference_uid)
		else:
			RP_count += 1


	
	# Display other file types caught
	if len(other) != 0:
		print("Other files not moved:")
		for file in other:
			print(file)
	
	print("--------------------------------------------------------------------------------")
	print("Files moved: ",CT_count, " CT, ", RS_count, " RS, ", RE_count, " RE, ",RD_count, " RD",RP_count, " RP")
	print("--------------------------------------------------------------------------------")



def remove_unneeded_RE_files(PATH):
	"""
	remove_unneeded_RE_files Deletes remaining registration files associated to an image sequence 
							 that was not downloaded.

	:param PATH: Path to patient directory.
	"""
	# TO DO: move into MR and PE files if exist
	file_list = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) and 'RE' in f]
	for file in file_list:
		d = dcm.read_file(PATH+file)
		class_UID = d.RegistrationSequence[-1].ReferencedImageSequence[0].ReferencedSOPClassUID

		ref_image_class = dict_class_UID[class_UID] 

		if ref_image_class != 'CT' and os.path.exists(PATH+ref_image_class):
			print("Moving "+ref_image_class+" registration file.")
			os.system("sudo mv " + PATH+file +" " + PATH+ref_image_class+"/"+file)

		# else:
		# 	print("Removing "+ref_image_class+" registration file.")
		# 	os.system("sudo rm " + PATH+file)




def organize_multiple_patients(list_patients, PATH):
	"""
	organize_multiple_patients calls each of the sorting functions for each patient to be sorted.

	:param list_patients: list of patient directories to be sorted.
	:param PATH: main path to patient directories.
	"""

	for patient in list_patients:
		print("================================================================================")
		print("Patient ", patient)
		print("--------------------------------------------------------------------------------")
		patient_path = PATH + str(patient) + "/"

		# Call each sorting function
		remove_RI_RT_files(patient_path)
		remove_non_CT_image_files(patient_path)
		sort_image_files_by_RS(patient_path)
		remove_unneeded_RE_files(patient_path)

		# Print files that were not sorted
		print("Files Remaining:")
		print([f for f in os.listdir(patient_path) if os.path.isfile(os.path.join(patient_path, f))])
	  


if __name__ == "__main__":
	start = time.time()

	# from config import config
	PATH = config['PATH']
	#PATH = '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'
	# PATH = '/mnt/iDriveShare/Trey/images/'#'/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/' # Path to patient directories
	list_patients_to_sort = [] # Patient directories to sort

	if len(sys.argv[1:]) == 0:
		print("WARNING: No files sorted.")#to do raise actual warning
		print("Please specify patient directory(ies) or write 'all' to sort all patients.")
	for patient in sys.argv[1:]:
		if patient.lower() == "all": # TO DO EMPTY STRING DOESN'T WORK, Prob check sys.argc length above
				# if all(substring.lower() not in d.StructureSetLabel.lower() for substring in ignore_terms)
			ignore_pt_terms = config['ignore_keywords_in_pt_dirname']
			if len(ignore_pt_terms) == 0: # to do: what if patient isnt a number, then sorting by int wont work
				list_patients_to_sort = sorted([f for f in os.listdir(PATH)])#,key=int
			else:
				list_patients_to_sort = sorted([f for f in os.listdir(PATH) 
					if all(substring.lower() not in f.lower() for substring in ignore_pt_terms)])#,key=int
			print(list_patients_to_sort)
			# list_patients_to_sort = sorted([f for f in os.listdir(PATH) if 'b' not in f and 'old' not in f],key=int)
		
		# Check if command line arguments correspond to existing patient directories
		elif os.path.exists(PATH+patient):
			list_patients_to_sort.append(patient)
		else:	
			print("Patient directory "+ PATH+patient + " does not exist.")
	

	organize_multiple_patients(list_patients_to_sort, PATH)    

	# TO DO: fix issue where mutiple CT with diff names

	end = time.time()
	print("***TOTAL TIME***")
	print(end-start,"seconds")
