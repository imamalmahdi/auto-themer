import os
import subprocess
import shutil
from config import CURRENT_DIR

class Widget:
    def __init__(self, name):
        docs = r"C:\Users\mahdi\OneDrive\Documents\Rainmeter\Skins"
        self.name = name
        self.absolute = name.split("\\")[0]
        self.main = docs + '\\' + self.absolute + r"\@Resources\Variables.inc"
    
    def switch(self, mode):
        if mode == 0:
            config_file = f"{CURRENT_DIR}\\{self.absolute}\\dark.inc"
        elif mode == 1:
            config_file = f"{CURRENT_DIR}\\{self.absolute}\\light.inc"

        os.remove(self.main)
        shutil.copy(config_file, self.main)
        path = r'"C:\Program Files\Rainmeter\Rainmeter.exe" !Refresh '
        command = path + f'"{self.name}"'
        subprocess.call(command)
