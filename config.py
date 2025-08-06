''' 
Configuration variables for runing the code. See below for more information. 
PATH is the only variable you NEED to change, but it is recommended to change the CT keyword and ignore terms too.
'''

config = {
	'PATH':'/mnt/iDriveShare/Kayla/sort_examples/',#rtog-hea-and-neck-cetuximab/', # list to patient directories
	'CT_keyword':'CT_', # A keyword present in all CT names from the TPS, helps to differentiate between CBCT names
	'CT_name_min_length':0, # minimum string length of CT name
	'CT_name_max_length':16, # maximum string length allowed in Structure Set Label tag = 16
	'ignore_keywords_in_CT':['copy', 'adap', 'planad', 'qa', 'test','pa','do not use'], # Words to ignore in CT names (ie not real planning CTs)
	'ignore_keywords_in_pt_dirname':[], # Keywords in patient directories to skip, eg if you want to skip all dirs with 'old' in them
	'print_check_results': True # Prints results to console for additional scripts 
}

'''
PATH: This is a mandatory variable indicating the path where the patient directories each with unsorted DICOMs are stored.

Since there are often duplicate structure sets for a given CT created for testing and calculations, you can avoid
some sorting errors if there is a (somewhat) standardized naming convention for the main planning CTs. You can optionally
customize the following variables to work with your naming convention.
 - CT_keyword: a keyword present in all CT names form the TPS
 - CT_name_min_length: the minimum length of the CT name
 - CT_name_max_length: the maximum length of the CT name
 - ignore_keywords_in_CT: keywords frequently found in CT copies created in the TPS that are not useful. Often contain words
 						  like 'copy', 'QA', 'test', etc.
For example, our CTs are always named in the format "CT_16_JUN_2024", so I might set CT_keyword = 'CT_' and the min and
max lengths to 14. Doing so would ignore names like "CT_1", which in our case is simply an unwanted copy.

ignore_keywords_in_pt_dirname: list of keywords in patient directories you want to skip. 
For example, if you want to ignore all patient directories with 'old' or 'skip' in their names.

'''