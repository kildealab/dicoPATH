import os
import sys
import pydicom as dcm

#PATH = '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'
PATH='/mnt/iDriveShare/Trey/images/'
# files = os.listdir('/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/')
# for file in files:
#     imgs= os.listdir('/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'+file+'/')
#     for img in imgs:
#         if '1c' in img:
#             print(file)

list_patients = []
list_patients_2 = []
patient = '968'
patient_path = PATH + patient + '/'
CBCT_path = patient_path+'20230420_kV_CBCT_13g/'

if len(sys.argv) > 1:
    print(sys.argv)
    for arg in sys.argv[1:]:
        patient_path = PATH+arg+'/'
        print(patient_path)
        for folder in [i for i in os.listdir(patient_path) if 'kV_CBCT_' in i and 'X' not in i]:
            RE_files = [f for f in os.listdir(patient_path + folder) if 'RE' in f]
            if len(RE_files) == 0:
                print(folder)

    quit()


'''
for file in os.listdir(CBCT_path):
    if 'RE' in file:
        d = dcm.read_file(CBCT_path+file)
        for reg in d.RegistrationSequence:
            print(reg.FrameOfReferenceUID)
            print(reg.MatrixRegistrationSequence[0])
    if 'CT' in file:
        d = dcm.read_file(CBCT_path+file)
        print(d.FrameOfReferenceUID)
        break
    
print("CT FOLDER")
CT_path = patient_path+'20230331_CT_20_MAR_2023/'
for file in os.listdir(CT_path):
    if 'RE' in file:
        print("-------------------------------")
        d = dcm.read_file(CT_path+file)
        for reg in d.RegistrationSequence:
            print(reg.FrameOfReferenceUID)
            print(reg.MatrixRegistrationSequence[0].MatrixSequence[0])
            if (reg.MatrixRegistrationSequence[0].MatrixSequence[0].FrameOfReferenceTransformationMatrix!=[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]):
                list_patients_2.append(reg.FrameOfReferenceUID)

    if 'CT' in file:
        d = dcm.read_file(CT_path+file)
        # print(d)
        #break
'''
file_list = os.listdir(PATH)
patients_to_avoid = ['600','670','704','730','746','842','944']
patient_list = sorted([int(p) for p in file_list if 'b' not in p and 'old' not in p and p not in patients_to_avoid])
#print(patient_list)

with open('dirs_without_reg.txt', 'a') as f:
    for patient in patient_list:
        is_reg = True
        print(patient)
        patient_path = PATH+str(patient)+'/'
        #print(patient_path)
        first = True
        for folder in [i for i in os.listdir(patient_path) if 'CT_' in i]:
            #print(folder)
            # print(os.listdir(patient_path))
            RE_files = [f for f in os.listdir(patient_path + folder) if 'RE' in f]
            if len(RE_files) == 0:
                if first:
                     f.write('\n'+str(patient)+'\n')
                     first = False
                #print(folder)
                f.write(folder+'\n')
                if '_CT_' not in folder and len(os.listdir(patient_path+folder))!=0:
                   # os.system('sudo mv '+patient_path+folder+'/* '+patient_path)
                    is_reg = False
       # if not is_reg:
            #os.system('sudo mv '+patient_path+'*_CT_*/* ' + patient_path)

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
