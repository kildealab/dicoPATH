# Filename: check_missing_RE.py
# Author: Kayla O'Sullivan-Steben
# Date Created: November 28, 2023
# Description: Checks which imaging subdirectories don't contain DICOM registration files. 


# Import statements
import os, sys, time
import pydicom as dcm
from config import config



def generate_dirs_without_reg_txt(PATH, patient_list,print_results = True):
    """
    generate_dirs_without_reg_txt   Loops through each image subdirectory in each patient directory to see if there is a registration
                                    file present, assuming it is in the form of 'RE*.dcm', where * is anything. The results are written
                                    in the following text file: ./output/dirs_without_reg.txt

    :param PATH: General path to patient directories.
    :param patient_list: List of patient directories to go through.
    :param print_results: Prints the results to console as it goes through each patient.
    """
    if not os.path.isdir('output'):
        os.mkdir('output')

    with open('output/dirs_without_reg.txt', 'a') as f:
        for patient in patient_list:
            # is_reg = True
            
            patient_path = PATH+str(patient)+'/'
     
            first = True # used to write the patient id only once in the document

            for folder in [i for i in os.listdir(patient_path) if 'CT_' in i]:
                RE_files = [f for f in os.listdir(patient_path + folder) if 'RE' in f]
                if len(RE_files) == 0:
                    if first:
                         f.write('\n'+str(patient)+'\n')
                         if print_results:
                            print('\n'+patient)
                         first = False
      
                    f.write(folder+'\n')
                    if print_results:
                        print(folder)


            # The following code was used to empty the directories without dicom RE files so they can be resorted with updated sorting script.
            # No longer needed but keeping in case.
            ''' 
                    if '_CT_' not in folder and len(os.listdir(patient_path+folder))!=0:
                        os.system('sudo mv '+patient_path+folder+'/* '+patient_path)
                        is_reg = False
            if not is_reg:
                os.system('sudo mv '+patient_path+'*_CT_*/* ' + patient_path)
            '''


if __name__ == "__main__":
    start = time.time()

    PATH = config['PATH']
    ignore_pt_terms = config['ignore_keywords_in_pt_dirname']
    print_results = config['print_check_results']

    list_patients = []

    if len(sys.argv[1:]) == 0:
        print("WARNING: No files checked for RE.")#to do raise actual warning
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
        generate_dirs_without_reg_txt(PATH, list_patients,print_results)
        print("********************************************")
        print("See results in ./output/dirs_without_reg.txt")
        print("********************************************")

    end = time.time()
    print("***TOTAL TIME***")
    print(end-start,"seconds")
