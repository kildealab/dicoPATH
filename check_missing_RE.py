import os
import sys
import pydicom as dcm
from config import config


PATH = config['PATH']


list_patients = []

file_list = os.listdir(PATH)

ignore_pt_terms = config['ignore_keywords_in_pt_dirname']

if len(ignore_pt_terms) == 0:
    patient_list = sorted([f for f in os.listdir(PATH)])
else:
    patient_list = sorted([f for f in os.listdir(PATH) 
        if all(substring.lower() not in f.lower() for substring in ignore_pt_terms)])

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
                     first = False
  
                f.write(folder+'\n')

        # The following code was used to empty the directories without dicom RE files so they can be resorted with updated sorting script.
        # No longer needed but keeping in case.
        ''' 
                if '_CT_' not in folder and len(os.listdir(patient_path+folder))!=0:
                    os.system('sudo mv '+patient_path+folder+'/* '+patient_path)
                    is_reg = False
        if not is_reg:
            os.system('sudo mv '+patient_path+'*_CT_*/* ' + patient_path)
        '''
