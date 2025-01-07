import os, sys, time
import pydicom as dcm
from config import config



def generate_dirs_with_double_img(PATH,patient_list,print_results=True):

    with open('output/dirs_with_double_img.txt', 'a') as f:
        for patient in patient_list:

            patient_path = PATH+str(patient)+'/'
            #print(patient_path)
            prev_img = ''
            for folder in sorted([i for i in os.listdir(patient_path) if '_CBCT_' in i]):
                if prev_img[:-1] == folder[:-1]:
                    try:
                        d1 = dcm.read_file(patient_path+folder+'/'+os.listdir(patient_path+folder)[0]).AcquisitionTime
                        d0 = dcm.read_file(patient_path+prev_img+"/"+os.listdir(patient_path+prev_img)[0]).AcquisitionTime

                    
                    except:
                        d1 = ''
                        d0 = ''
                    f.write('\n'+str(patient)+'\n')
                    f.write(prev_img +"("+d0+ ') -> ' + folder + '('+d1+ ')')

                    if print_results:
                        print('\n'+str(patient))
                        print(prev_img +"("+d0+ ') -> ' + folder + '('+d1+ ')')

                    if (d0) < (d1):
                        f.write("Older Image: "+ prev_img+'\n\n')
                        if print_results:
                            print("Older Image: "+ prev_img)
                        # os.system('sudo mv '+patient_path+prev_img+' '+patient_path+'X'+prev_img)
                    else:
                        f.write("Older Image: " + folder+'\n\n')
                        if print_results:
                            print("Older Image: "+ folder)
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

if __name__ == "__main__":
    start = time.time()

    PATH = config['PATH']
    print_results = config['print_check_results']

    list_patients = []

    if len(sys.argv[1:]) == 0:
        print("WARNING: No files checked for image duplicates.")#to do raise actual warning
        print("Please specify patient directory(ies) or write 'all' to check all patients.")
    
    for patient in sys.argv[1:]:
        if patient.lower() == "all":
            ignore_pt_terms = config['ignore_keywords_in_pt_dirname']
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
        generate_dirs_with_double_img(PATH, list_patients,print_results)
        print("************************************************")
        print("See results in ./output/dirs_with_double_img.txt")
        print("************************************************")

    end = time.time()
    print("***TOTAL TIME***")
    print(end-start,"seconds")
