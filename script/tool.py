import subprocess
from urllib import request
import zipfile
import os, shutil
import ctypes
import py7zr
import pyunpack # it needs patool

path_prompt_x32 = r'C:\"Program Files (x86)\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat"'
path_prompt_x64 = r'C:\"Program Files (x86)\Microsoft Visual Studio 10.0\VC\bin\amd64\vcvars64.bat"'

def get_working_path():
    return os.path.dirname(os.path.abspath(__file__))

def is_admin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def create_folder(dir):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError:
            print(f'[*] Error: Could not create the directory {dir}')
            exit(1)

def generate_temp_file_name():
    return 'temp.bin'

def generate_temp_bat_name():
    return 'temp.bat'

def extract_to(url, path, is_7z = False):
    temp_path = generate_temp_file_name()
    request.urlretrieve(url, temp_path)

    if is_7z:
        #pyunpack.Archive(temp_path).extractall(path)
        f = py7zr.SevenZipFile(temp_path)
        f.extractall(path)
        f.close()
    else:
        f = zipfile.ZipFile(temp_path)
        f.extractall(path)
        f.close()
    
    os.remove(temp_path)

def execute_batch_x32_inst(inst):
    temp_bat_path = generate_temp_bat_name()
    with open(temp_bat_path, 'wt') as f:
        f.write(f'call {path_prompt_x32}\n')
        f.write(f'{inst}\n')      
    subprocess.call([temp_bat_path])
    os.remove(temp_bat_path)

def execute_batch_x32(path):
    execute_batch_x32_inst(f'call {path}')
    
def execute_batch_x64_inst(inst):
    temp_bat_path = generate_temp_bat_name()
    with open(temp_bat_path, 'wt') as f:
        f.write(f'call {path_prompt_x64}\n')
        f.write(f'{inst}\n')      
    subprocess.call([temp_bat_path])
    os.remove(temp_bat_path)

def execute_batch_x64(path):
    execute_batch_x64_inst(f'call {path}')

path_curr_dir   = get_working_path()
path_main_dir   = os.path.abspath(f'{path_curr_dir}/../bin')
path_vbox_dir   = os.path.abspath(f'{path_main_dir}/VirtualBox')