import os
from datetime import datetime
import csv

PATH = '/mnt/iDriveShare/Kayla/CBCT_images/kayla_extracted/'

#with open('/data/kayla/CT_file_names.csv', 'w', 
list_rows =[]




#with open('/data/kayla/CT_file_names.csv','w',newline='') as file:
   # writer = csv.writer(file)
  #  writer.writerow


list_rows.append(['id','CT1','CT2','CT3'])


for patient in [p for p in os.listdir(PATH) if 'b' not in p and 'not' not in p]:
    patient_path = os.path.join(PATH,patient)
    CT_list = [d for d in os.listdir(patient_path) if d[9:11] == 'CT' and len(d) == 23]

    CT_list.sort(key=lambda x: datetime.strptime(x[12:], "%d_%b_%Y"))
    
    if len(CT_list) > 2:
        print(len(CT_list))
        list_rows.append([patient,CT_list[0],CT_list[1],CT_list[2]])
    elif len(CT_list) == 2:
        list_rows.append([patient,CT_list[0],CT_list[1],''])
    elif len(CT_list) == 1:
        list_rows.append([patient,CT_list[0],'',''])
    else:
        print("Error: no CTs for patient ",patient)
print(list_rows)
with open('/data/kayla/CT_file_names.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(list_rows)


    
    #if len(CT_list) > 2:
     #   print(len(CT_list))

