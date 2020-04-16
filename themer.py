import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

current_dir = Path(__file__).parent.absolute()

class Widget:
    def __init__(self, name):
        docs = r"C:\Users\mahdi\OneDrive\Documents\Rainmeter\Skins"
        self.name = name
        self.absolute = name.split("\\")[0]
        self.main = docs + '\\' + self.absolute + r"\@Resources\Variables.inc"
    
    def switch(self):
        time = datetime.now().timetuple()
        if time.tm_hour >= 17 or time.tm_hour < 5:
            file = f"{current_dir}\\{self.absolute}\\dark.inc"
        else:
            file = f"{current_dir}\\{self.absolute}\\light.inc"

        os.remove(self.main)
        shutil.copy(file, self.main)
        path = r'"C:\Program Files\Rainmeter\Rainmeter.exe" !Refresh '
        command = path + f'"{self.name}"'
        subprocess.call(command)


lyrics_widget = Widget("Simple Lyrics Display")
lyrics_widget.switch()

info_widget = Widget("Lumiero\\Song Info")
info_widget.switch()