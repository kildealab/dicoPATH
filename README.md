# dicoPATH
A python script for sorting DICOM images and related registration and DICOM-RT data exported from the Varian Eclipse Treatment Planning System (v15 and v18).

## Table of Contents
- [Motivation](#Motivation)
- [Features](#Features)
- [Dependencies](#Dependencies)
- [Installation](#Installation)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [Contact](#Contact)

## Motivation
TODO

## Features
TODO

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
   
## Usage
### Downloading data from the Treatment Planning System
Instructions for downloading DICOM data from the Varian Eclipse TPS (tested on versions 15 and 18) can be found here: [TPS Download Instructions](https://docs.google.com/document/d/1NtpMWKvi45IYjV2Tp65CwWPKFmXAfJu6idoXx9AcafA/edit?usp=sharing).
Files should be exported all at once per patient, each in their own patient directory. 

The code expects that each patient has their own directory with a dump of unorganized DICOM files for all images, like so (note the patient directories can have any names):

```
/path/to/patient/directories/ 
├── patient1
│   ├── CT....dcm 
│   ├── CT....dcm 
│   ├── ... 
│   └── RS....dcm 
├── patient2
|   ├── CT....dcm
|   ├── CT....dcm
|   ├── ...
|   └── RS....dcm
...
├── patientN
|    └── ...

```
### Configuring the sorting script
TODO: explain config file
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
  python DICOM_sorter.py all
  ```
To sort only a subset of patient directories in PATH:
  ```
  python DICOM_sorter.py patient1 patient2
  ```
TO DO: Add part about changing the CBCT directory names from v18 --> v15

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
