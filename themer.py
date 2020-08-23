import ctypes
import subprocess
from datetime import datetime
from config import get_config
from app_settings import SettingsFile
from widgets import Widget
from registry import Registry

# Loads a setting fild
settings = get_config()

# Choosing theme
time = datetime.now().timetuple()
if time.tm_hour >= settings['time']['dark'] or time.tm_hour < settings['time']['light']:
    theme_mode = 0
else:
    theme_mode = 1
# theme_mode = 1

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
if settings['wallpaper'][0]:
    if theme_mode == 1:
        wallpaper = settings['wallpaper'][1]["light"]
    elif theme_mode == 0:
        wallpaper = settings['wallpaper'][1]["dark"]
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

# SumatraPDF
if settings['sumatrapdf'][0]:
    sumatrapdf_settings = SettingsFile(r"C:\Users\mahdi\AppData\Local\SumatraPDF\SumatraPDF-settings.txt")
    if theme_mode == 1:
        text_replace = "\t"*1 + 'TextColor = ' + settings['sumatrapdf'][1]['light']["text"] + '\n'
        bak_replace = "\t"*1 + 'BackgroundColor = ' + settings['sumatrapdf'][1]['light']["background"] + '\n'
    elif theme_mode == 0:
        text_replace = "\t"*1 + 'TextColor = ' + settings['sumatrapdf'][1]['dark']["text"] + '\n'
        bak_replace = "\t"*1 + 'BackgroundColor = ' + settings['sumatrapdf'][1]['dark']["background"] + '\n'
    sumatrapdf_settings.change("TextColor", text_replace)
    sumatrapdf_settings.change("BackgroundColor", bak_replace)