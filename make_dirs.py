import os
import platform

list_folders = ['dir1','dir2']

from config import config
PATH = config['PATH']


for folder in list_folders:
    folder_path=path+str(folder)
    if not os.path.exists(folder_path):
        if platform.system() == "Windows":
            os.makedirs(folder_path)
        else:
            os.system("sudo mkdir " + folder_path)


