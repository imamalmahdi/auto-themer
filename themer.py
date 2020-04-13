import os
import subprocess


class Widget:
    def __init__(self, name):
        docs = r"C:\Users\mahdi\OneDrive\Documents\Rainmeter\Skins"
        self.name = name
        self.main = docs + '\\' + name.split("\\")[0] + r"\@Resources\Variables.inc"
        self.mid = self.main + ".a"
        self.bak = self.main + ".bak"
    
    def switch(self):
        os.rename(self.main, self.mid)
        os.rename(self.bak, self.main)
        os.rename(self.mid, self.bak)

        path = r'"C:\Program Files\Rainmeter\Rainmeter.exe" !Refresh '
        command = path + f'"{self.name}"'
        subprocess.call(command)


lyrics_widget = Widget("Simple Lyrics Display")
lyrics_widget.switch()

info_widget = Widget("Lumiero\\Song Info")
info_widget.switch()


