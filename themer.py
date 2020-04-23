import os
import subprocess
import shutil
import winreg
import ctypes
from pathlib import Path
from datetime import datetime

current_dir = Path(__file__).parent.absolute()

class Widget:
    def __init__(self, name):
        docs = r"C:\Users\mahdi\OneDrive\Documents\Rainmeter\Skins"
        self.name = name
        self.absolute = name.split("\\")[0]
        self.main = docs + '\\' + self.absolute + r"\@Resources\Variables.inc"
    
    def switch(self, mode):
        if mode == 0:
            file = f"{current_dir}\\{self.absolute}\\dark.inc"
        elif mode == 1:
            file = f"{current_dir}\\{self.absolute}\\light.inc"

        os.remove(self.main)
        shutil.copy(file, self.main)
        path = r'"C:\Program Files\Rainmeter\Rainmeter.exe" !Refresh '
        command = path + f'"{self.name}"'
        subprocess.call(command)

class Registry:
    def __init__(self, name):
        self.root = winreg.HKEY_CURRENT_USER
        self.path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        self.key_name = name

    def query(self):
        opened_key = winreg.OpenKeyEx(self.root, self.path, access=winreg.KEY_READ)
        values = winreg.QueryValueEx(opened_key, self.key_name)
        winreg.CloseKey(opened_key)
        return values
    
    def set(self, value):
        opened_key = winreg.OpenKeyEx(self.root, self.path, access=winreg.KEY_WRITE)
        winreg.SetValueEx(opened_key, self.key_name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(opened_key)

# Choosing theme
time = datetime.now().timetuple()
if time.tm_hour >= 17 or time.tm_hour < 5:
    theme_mode = 0
    wallpaper = f"{current_dir}\\wallpapers\\dark.png"
else:
    theme_mode = 1
    wallpaper = f"{current_dir}\\wallpapers\\light.png"

# Rainmeter
widgets = ["Simple Lyrics Display", "Lumiero\\Song Info"]
for widget in widgets:
    working_widget = Widget(widget)
    working_widget.switch(theme_mode)

# Windows Theme
registry_keys = ["AppsUseLightTheme", "SystemUsesLightTheme"]
for registry_key in registry_keys:
    working_key = Registry(registry_key)
    working_key.set(theme_mode)

# Wallpaper
ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper, 3)

# Windows Terminal
terminal_file = r"C:\Users\mahdi\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\profiles.json"
if theme_mode == 0:
    new_file = f"{current_dir}\\Terminal\\dark.json"
elif theme_mode == 1:
    new_file = f"{current_dir}\\Terminal\\light.json"
os.remove(terminal_file)
shutil.copy(new_file, terminal_file)

# Spotify
if theme_mode == 0:
    subprocess.call("spicetify restore", stdout=subprocess.DEVNULL)
elif theme_mode == 1:
    subprocess.call("spicetify apply", stdout=subprocess.DEVNULL)