import os
import subprocess
import shutil
import winreg
import ctypes
import fileinput
import json
from pathlib import Path
from datetime import datetime

current_dir = Path(__file__).parent.absolute()

class SettingsFile:
    def __init__(self, path):
        self.file_path = path
    
    def change(self, target_line, new_line):
        with fileinput.FileInput(self.file_path, inplace=True, backup='.bak') as file:
            for line in file:
                if target_line in line:
                    print(line.replace(line, new_line), end='')
                else:
                    print(line, end='')


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

# Loads a setting fild
settings_file = Path(f"{str(current_dir)}\\settings.json")
if settings_file.exists() == False:
    settings = {
        "rainmeter" : True,
        "windows" : True,
        "wallpaper" : True,
        "terminal" : True,
        "vscode" : True,
        "spotify" : True
    }

    settings_file.write_text(json.dumps(settings, indent=4))
else:
    settings = json.loads(settings_file.read_text())

# Choosing theme
time = datetime.now().timetuple()
if time.tm_hour >= 17 or time.tm_hour < 5:
    theme_mode = 0
    wallpaper = f"{current_dir}\\wallpapers\\dark.png"
else:
    theme_mode = 1
    wallpaper = f"{current_dir}\\wallpapers\\light.png"
# theme_mode = 1
# wallpaper = f"{current_dir}\\wallpapers\\light.png"

# Rainmeter
if settings['rainmeter'][0]:
    widgets = settings['rainmeter'][1]
    for widget in widgets:
        working_widget = Widget(widget)
        working_widget.switch(theme_mode)

# Windows Theme
if settings['windows']:
    registry_keys = ["AppsUseLightTheme", "SystemUsesLightTheme"]
    for registry_key in registry_keys:
        working_key = Registry(registry_key)
        working_key.set(theme_mode)

# Wallpaper
if settings['wallpaper']:
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper, 3)

# Windows Terminal
if settings['terminal'][0]:
    terminal_file = SettingsFile(r"C:\Users\mahdi\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json")
    if theme_mode == 1:
        replaced_value = "\t"*3 + '"colorScheme": "' + settings['terminal'][1]['light'] + '",\n'
    elif theme_mode == 0:
        replaced_value = "\t"*3 + '"colorScheme": "' + settings['terminal'][1]['dark'] + '",\n'
    terminal_file.change("colorScheme", replaced_value)

# Vscode
if settings['vscode'][0]:
    vscode_file = SettingsFile(r"C:\Users\mahdi\AppData\Roaming\Code\User\settings.json")
    if theme_mode == 1:
        replaced_value = "\t"*1 + '"workbench.colorTheme": "' + settings['vscode'][1]['light'] + '",\n'
    elif theme_mode == 0:
        replaced_value = "\t"*1 + '"workbench.colorTheme": "' + settings['vscode'][1]['dark'] + '",\n'
    vscode_file.change("workbench.colorTheme", replaced_value)

# Spotify
if settings['spotify'][0]:
    if theme_mode == 0:
        spotify_theme = settings['spotify'][1]['dark']
    elif theme_mode == 1:
        spotify_theme = settings['spotify'][1]['light']

    subprocess.call(f"spicetify -q config current_theme {spotify_theme}", shell=True)
    subprocess.call("spicetify -q update", shell=True)