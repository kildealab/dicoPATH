import pydicom as dcm
import os
import time

start_time = time.time()

PATH = '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'

one_per_dir = True
one_per_unsorted = True
unsorted_checked = False


def identity_removed(file_path,file_name):
    if dcm.read_file(os.path.join(file_path,file_name)).PatientIdentityRemoved != 'YES':
        
        print("ATTENTION: Found DICOMs with identifiers in Patient " + patient + " not de-identified in directory " + file_path)
        return False
    else:
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
            is_deidentified *= identity_removed(patient_path,d)
            unsorted_checked = True 


        if os.path.isdir(os.path.join(patient_path,d)):
            #print(d)
            file_path = os.path.join(patient_path,d) # Assuming only one level of directories
            for f in os.listdir(file_path):
                if os.path.isfile(os.path.join(file_path,f)):
                   # print("**************************************************************************************************************************************************") 
                    #print(dcm.read_file(os.path.join(file_path,f)))
                    try:
                        is_deidentified *= identity_removed(file_path,f)
                        if one_per_dir:
                            break

                    except Exception as e:
                        print("Error with file " + file_path+f,":",e)
                    #print(f)
                    exit
                else:
                    print(file_path,f,"is not a file. Fix directory hierarchy.")
    if is_deidentified:
        print("OK")

        
print("--- %s seconds ---" % (time.time() - start_time))
#if dcm.read_file(PATH).PatientIdentityRemoved != 'YES':
  #  print("ATTENTION: ")
