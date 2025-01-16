from setuptools import setup, find_packages

setup(
    name='dicoPATH',
    version='0.1.0',
    description='TODO',
    author="Kayla O'Sullivan-Steben",
    author_email='kayla.osullivan-steben@mail.mcgill.ca',
    packages=find_packages(),
    install_requires=[
        'pydicom'
    ],
    entry_points={
        'console_scripts': [
            'check_anon=scripts.check_anon:main',
            'check_missing_RE=scripts.check_missing_RE:main',
            'check_sameday_CBCTs=scripts.check_sameday_CBCTs:main',
            'DICOM_sorter=scripts.DICOM_sorter:main',
            'format_CBCT_dirnames=scripts.format_CBCT_dirnames:main',
        ],
    },
)
