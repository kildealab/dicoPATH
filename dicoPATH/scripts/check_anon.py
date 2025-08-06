# Filename: check_anon.py
# Author: Kayla O'Sullivan-Steben
# Date Created: October 10, 2024
# Description: Checks whether DICOM files have been deidentified on export from TPS.

import pydicom as dcm
import os, sys, time
from config import config

patients_not_deidentified = []
patients_with_errors = []

def identity_removed(file_path,file_name,patient):
    """
    identity_removed    Checks whether a DICOM file has been deidentified (patient identifiers removed). 
                        First checks if the tag PatientIdentityRemoved = 'YES', which is set on export from the TPS
                        when anonymization is selected. If error, checks if DOB, sex are blank and if '^' or ' ' 
                        are in the name (typically used to separate first and last names).

    :param file_path: Path to the DICOM file.
    :param file_name: DICOM file name.
    :param patient: Current patient id (used to track which patient is being checked).

    :return: bool True or False indicating if a DICOM file has been deidentified.
    """
    try:

        if dcm.read_file(os.path.join(file_path,file_name)).PatientIdentityRemoved != 'YES':
            
            print("ATTENTION: Found DICOMs with identifiers in Patient "+patient+" directory : " + file_path)
            if patient not in patients_not_deidentified:
                patients_not_deidentified.append(patient)
            return False
        else:
            return True

    except Exception as e:
        d_file = dcm.read_file(os.path.join(file_path,file_name))
        print(file_path,file_name)
        if d_file.PatientSex != ''  or d_file.PatientBirthDate != '' or '^' in d_file.PatientName or ' ' in d_file.PatientName or ',' in d_file.patientName:
            print("ATTENTION: Found DICOMs with identifiers in Patient "+patient+" directory :"+file_path)
            if patient not in patients_not_deidentified:
                patients_not_deidentified.append(patient)
            return False

            
        else:
           # if e =="'FileDataset' object has no attribute 'PatientIdentityRemoved'":

            print("Error with file " + file_path+f,":",e)
            if patient not in patients_with_errors:
                patients_with_errors.append(patient)
            return True

    #print( dcm.read_file(os.path.join(PATH,patient,file_path,file_name)).PatientIdentityRemoved )


def check_deidentification(PATH,patient_list,print_results=True):
    """
    check_deidentification  loops through patients in list and checks whether each image directory is deidentified.

    :param PATH: General path to patient directories.
    :param patient_list: List of patient directories to go through.
    :param print_results: Prints the results to console as it goes through each patient. 
    """

    one_per_dir = True # only checking one file per directory, since should all be exported at once should be same for each
    one_per_unsorted = True # checking one file not sorted into subdirectory per patient 
    
  
    for patient in patient_list:
        print("=====================================================================")
        print(patient)
        #print("=====================================================================")
        is_deidentified = True
        unsorted_checked = False
        patient_path = os.path.join(PATH,patient)
        for d in os.listdir(patient_path):
            if d.endswith(".dcm") and not (one_per_unsorted and unsorted_checked):
                
                is_deidentified *= identity_removed(patient_path,d,patient)
                unsorted_checked = True 


            if os.path.isdir(os.path.join(patient_path,d)):
                file_path = os.path.join(patient_path,d) # Assuming only one level of directories
                for f in sorted(os.listdir(file_path)): # will choose CT before RS, sometimes tags missing in RS
                    if os.path.isfile(os.path.join(file_path,f)):

                        is_deidentified *= identity_removed(file_path,f,patient)
                        
                        if one_per_dir:
                            break


                    else:
                        print(file_path,f,"is not a file. Fix directory hierarchy.")
        if is_deidentified:
            print("OK")
        else:
            print("CAUTION - "+patient+"  NOT DEIDENTIFIED")





#if dcm.read_file(PATH).PatientIdentityRemoved != 'YES':
  #  print("ATTENTION: ")

def main():


    start = time.time()

    PATH = config['PATH']
    print_results = config['print_check_results']
    ignore_pt_terms = config['ignore_keywords_in_pt_dirname']

    list_patients = []

    if len(sys.argv[1:]) == 0:
        print("WARNING: No files checked for deidentification.")#to do raise actual warning
        print("Please specify patient directory(ies) or write 'all' to check all patients.")
    
    for patient in sys.argv[1:]:
        if patient.lower() == "all":
            
            if len(ignore_pt_terms) == 0: 
                list_patients = sorted([f for f in os.listdir(PATH)])
            else:
                list_patients = sorted([f for f in os.listdir(PATH) 
                    if all(substring.lower() not in f.lower() for substring in ignore_pt_terms)])#,key=int
            

        # Check if command line arguments correspond to existing patient directories
        elif os.path.exists(PATH+patient):
            list_patients.append(patient)
        else:   
            print("Patient directory "+ PATH+patient + " does not exist.")
    

    if len(list_patients) > 0:
        check_deidentification(PATH, list_patients,print_results)
        print("**************************************************")
        print("Number of patients checked:",len(list_patients))
        print("Patients checked:",list_patients)
        print(len(patients_not_deidentified),"patients not deidentified:",patients_not_deidentified)
        print(len(patients_with_errors),"patients with errors:",patients_with_errors)
        # print("--- %s seconds ---" % (time.time() - start_time))
        print("**************************************************")


    end = time.time()
    print("***TOTAL TIME***")
    print(end-start,"seconds")


if __name__ == "__main__":
    main()