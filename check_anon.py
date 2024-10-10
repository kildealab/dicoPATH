import pydicom as dcm
import os
import time

start_time = time.time()

PATH = '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'

one_per_dir = True
one_per_unsorted = True
unsorted_checked = False
patients_not_deidentified = []
patients_with_errors = []

def identity_removed(file_path,file_name,patient):
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

#upper_level_done = False

for patient in sorted(os.listdir(PATH)):
    print("=====================================================================")
    print(patient)
    #print("=====================================================================")
    is_deidentified = True
    patient_path = os.path.join(PATH,patient)
    for d in os.listdir(patient_path):
        if d.endswith(".dcm") and not (one_per_unsorted and unsorted_checked):
            
            is_deidentified *= identity_removed(patient_path,d,patient)
            unsorted_checked = True 


        if os.path.isdir(os.path.join(patient_path,d)):
            #print(d)
            file_path = os.path.join(patient_path,d) # Assuming only one level of directories
            for f in sorted(os.listdir(file_path)): # will choose CT before RS, sometimes tags missing in RS
                if os.path.isfile(os.path.join(file_path,f)):
                    #print("**************************************************************************************************************************************************") 
                    #print(dcm.read_file(os.path.join(file_path,f)))
                    #if f[0:2] == "RS":
                     #   print("doing RS")
                    is_deidentified *= identity_removed(file_path,f,patient)
                    
                    if one_per_dir:
                        break

                    #print(f)
                    #
                else:
                    print(file_path,f,"is not a file. Fix directory hierarchy.")
    if is_deidentified:
        print("OK")
    else:
        print("CAUTION - "+patient+"  NOT DEIDENTIFIED")

print("**************************************************")
print(len(patients_not_deidentified),"patients not deidentified:",patients_not_deidentified)
print(len(patients_with_errors),"patients with errors:",patients_with_errors)
print("--- %s seconds ---" % (time.time() - start_time))
print("**************************************************")

#if dcm.read_file(PATH).PatientIdentityRemoved != 'YES':
  #  print("ATTENTION: ")
