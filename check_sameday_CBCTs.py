import os
import sys
import pydicom as dcm
from config import config

PATH = config['PATH'] # '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'

list_patients = []

file_list = os.listdir(PATH)
# patients_to_avoid = ['600','670','704','730','746','842','944']
ignore_pt_terms = config['ignore_keywords_in_pt_dirname']

if len(ignore_pt_terms) == 0:
    patient_list = sorted([f for f in os.listdir(PATH)])
else:
    patient_list = sorted([f for f in os.listdir(PATH) 
        if all(substring.lower() not in f.lower() for substring in ignore_pt_terms)])
# patient_list = sorted([int(p) for p in file_list if 'b' not in p and 'old' not in p and p not in patients_to_avoid])
#print(patient_list)

with open('output/dirs_with_double_img.txt', 'a') as f:
    for patient in patient_list:
        print(patient)
        patient_path = PATH+str(patient)+'/'
        #print(patient_path)
        prev_img = ''
        for folder in sorted([i for i in os.listdir(patient_path) if '_CBCT_' in i]):
            if prev_img[:-1] == folder[:-1]:
                try:
                    d1 = dcm.read_file(patient_path+folder+'/'+os.listdir(patient_path+folder)[0]).AcquisitionTime
                    d0 = dcm.read_file(patient_path+prev_img+"/"+os.listdir(patient_path+prev_img)[0]).AcquisitionTime
                    print(prev_img,d0,folder,d1)
                
                except:
                    d1 = ''
                    d0 = ''
                f.write('\n'+str(patient)+'\n')
                f.write(prev_img +"("+d0+ ') -> ' + folder + '('+d1+ ')\n')

                if (d0) < (d1):
                    f.write("Older Image: "+ prev_img+'\n\n')
                    # os.system('sudo mv '+patient_path+prev_img+' '+patient_path+'X'+prev_img)
                else:
                    f.write("Older Image: " + folder+'\n\n')
                    # os.system('sudo mv '+patient_path+folder+' '+patient_path+'X'+folder)

            prev_img = folder
'''
for file in [i for i in os.listdir(patient_path) if '_CBCT_' in i]:
    for f in os.listdir(patient_path+file):
        if 'CT' in f:
            d = dcm.read_file(patient_path+file+'/'+f)
            print(d.FrameOfReferenceUID)
            list_patients.append(d.FrameOfReferenceUID)
            break

print(list_patients)
print(list_patients_2)
for patient in list_patients:
    if patient not in list_patients_2:
        print(patient)
'''
