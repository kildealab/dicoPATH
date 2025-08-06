from setuptools import setup, find_packages

setup(
    name='dicoPATH',
    version='0.1.0',
    description='TODO',
    author="Kayla O'Sullivan-Steben",
    author_email='kayla.osullivan-steben@mail.mcgill.ca',
    packages=find_packages(where='.', include=['dicoPATH', 'dicoPATH.*']),
    py_modules=['config'],
    install_requires=[
        'pydicom'
    ],
    entry_points={
        'console_scripts': [
            'check_anon=dicoPATH.scripts.check_anon:main',
            'check_missing_RE=dicoPATH.scripts.check_missing_RE:main',
            'check_sameday_CBCTs=dicoPATH.scripts.check_sameday_CBCTs:main',
            'DICOM_sorter=dicoPATH.scripts.DICOM_sorter:main',
            'format_CBCT_dirnames=dicoPATH.scripts.format_CBCT_dirnames:main',
        ],
    },
)
