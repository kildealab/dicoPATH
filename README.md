# dicoPATH
A python script for sorting DICOM images (mainly planning CTs and CBCTs), DICOM-RT data, and DICOM registration files exported from the Varian Eclipse Treatment Planning System (TPS). This code has been tested on data exported from Eclipse versions 15 and 18.

This repo also contains instructions for downloading DICOM data from the TPS, as well as some additional scripts, including: reformatting CBCT directory names, checking if DICOMs are deidentified, checking for missing registration files, and checking for multiple CBCTs from the same treatment fraction.

## Table of Contents
- [Motivation](#Motivation)
- [Features](#Features)
- [Dependencies](#Dependencies)
- [Installation](#Installation)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [Contact](#Contact)
- [Disclaimer](#Disclaimer)

## Motivation
The research in our lab requires a large dataset of CBCT scans to model imaging changes over the course of radiotherapy. The previous method for obtaining these CBCTs was to export them one by one from the TPS in order to keep them organized. However, this process is very slow, and exporting all of the files at once per patient resulted in a large dump of unorganized DICOM files. Therefore, I created this sorting script to sort CBCT, planning CT, and related DICOM-RT and registration files into organized directories with the same names as they are stored in the TPS. 

#### Overview of how the sorting works
Rather than opening each individual CT slice file, which would be very slow, the code uses the DICOM-RT Structure Set files to sort the images. The Structure Set file contains the label (name given in the TPS) which is used to create each image directory, and also contains a list of the CT slice UIDs it refers to, which are used to copy over the corresponding CT files. A visual representation of how the code works is shown below: 

<p align="center">
	<img src="https://github.com/user-attachments/assets/c0ebc43d-d971-4711-b4c2-c70a7f439871" width="800">
</p>

## Dependencies
* Python >= 3.8
* Pydicom >= 2.4.4

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/kildealab/dicoPATH.git
   ```
2. Install dependenices:
   ```
   cd dicoPATH
   pip install -r requirements.txt
   ```
   Note: the requirements include the line ```-e .```, which installs the current package with editing permissions. This will allow you to call the scripts below, and the ```-e``` flag allows you to edit code in the package without reinstalling.
   
## Usage
### Downloading data from the Treatment Planning System
Instructions for downloading DICOM data from the Varian Eclipse TPS (tested on versions 15 and 18) can be found here: [TPS Download Instructions](https://docs.google.com/document/d/1NtpMWKvi45IYjV2Tp65CwWPKFmXAfJu6idoXx9AcafA/edit?usp=sharing).
Files should be exported all at once per patient, each in their own patient directory. Unfortunately, this export process must be done manually once per patient, but the script itself will run on all patients at once.

The code expects that each patient has their own directory with a dump of unorganized DICOM files for all images, like so (note the patient directories can have any names):
```
/path/to/patient/directories/ 
├── 📁patient1
│   ├── 📄CT....dcm 
│   ├── 📄CT....dcm 
│   ├── ... 
│   └── 📄RS....dcm 
├── 📁patient2
|   ├── 📄CT....dcm
|   ├── 📄CT....dcm
|   ├── ...
|   └── 📄RS....dcm
...
├── 📁patientN
|    └── ...
```
### Configuring the sorting script
Open `config.py` and replace the 'PATH' variable with the path containing your patient directories. Please see comments in `config.py` for an explanation of the other optional variables.
```
config = {
	'PATH':'/path/to/patient/directories/', # path to patient directories
	'CT_keyword':'',
	'CT_name_min_length':0,
	'CT_name_max_length':16, # maximum string length allowed in Structure Set Label tag = 16
	'ignore_keywords_in_plan':['copy', 'adap', 'planad', 'qa', 'test','pa','do not use'],
	'ignore_keywords_in_pt_dirname':[] 
}
```
### Running the sorting script
You can then either run the code for all patients in PATH, or on select patient directory(ies).

To sort all patient directories in PATH:
  ```
  python DICOM_sorter all
  ```
To sort only a subset of patient directories in PATH:
  ```
  python DICOM_sorter patient1 patient2
  ```
The resulting directory structure will look like this:
```
/path/to/patient/directories/ 
├── 📁patient1
│   ├── 📁DATE_Planning_CT_name 
│   ├── 📁DATE_kV_CBCT_1a
|   ├── 📁DATE_kV_CBCT_3a
│   ├── ... 
│   ├── 📁RI  # RT Image + registrations 
│   └── 📁RT  # RT Treatment Records
...
```
### Running the other scripts
I've created a few other scripts that may or may not be useful. A brief description of each are written below. They are all run the same as the sorting script, using the command line argument 'all' to run it over all patients in PATH, or using individual patients as the arguments to only do a subset.
#### Formatting the CBCT directory names from v18 to v15 for consistency
The CBCT names generated by the TPS in v18 are formatted differently than those in previous versions. This script will rename all of those with the v18 format (eg: kVCBCT_01c01) to the older version (eg: kV_CBCT_01c). This makes post-processing simpler when you have a mix of old and new data.
To reformat all patient directories in PATH:
  ```
  python format_CBCT_dirnames all
  ```
#### Check which patients are not deidentified
If exporting data for research, DICOM files should always be deidentified on export of the TPS. This code checks for patients that have DICOMs that have NOT been deidentified by the TPS.
To check all patient directories in PATH:
  ```
  python check_anon all
  ```
#### Check which image directories are missing Registration files
CBCTs will likely have been registered to the planning CT, and the DICOM registration file containing the registration matrix should have been downloaded and sorted into the appropriate directories. This code checks which image directories are missing registration files.
To check all patient directories in PATH:
  ```
  python check_missing_RE all
  ```
#### Check for multiple CBCTs taken at the same treatment fraction
Sometimes, multiple CBCTs will be captured during the same treatment session, either due to poor quality or improper positioning. This code will checks for CBCTs taken during the same treatment fraction and determines which one is older and likely discardable.
To check all patient directories in PATH:
  ```
  python check_sameday_CBCTs all
  ```

## Contributing
We welcome contributions! If you are interested in contributing, please fork the repository and create a pull request with your changes.
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them.
4. Push your branch: `git push origin feature-name`
5. Create a pull request.
## Lincense
This project is provided under the GNU GLPv3 license to preserve open-source access to any derivative works. See the LICENSE file for more information.
## Contact
For support or questions, please email Kayla O'Sullivan-Steben at kayla.osullivan-steben@mail.mcgill.ca.
## Disclaimer
This is not the most beautifully packaged or polished code, but I hope it still proves useful. I have also only tested this code on our in-house data and on our Linux system. That being said, I happily welcome suggestions, improvements, and contributions!

