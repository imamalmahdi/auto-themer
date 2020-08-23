import winreg

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