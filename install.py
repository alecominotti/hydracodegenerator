import subprocess
import sys
import platform

# Dependencies Installer for Hydra Code Generator
# Additionaly for Linux, xclip is installed 

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__=='__main__':
    if(platform.system()=='Linux'):
        subprocess.call(['sudo', 'apt-get', 'install', 'xclip'])
    with open('requirements.txt') as file:
        lines = file.readlines()
        for package in lines:
            install(package)
    