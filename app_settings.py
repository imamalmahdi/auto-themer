import in_place

class SettingsFile:
    def __init__(self, path):
        self.file_path = path
    
    def change(self, target_line, new_line):
        with in_place.InPlace(self.file_path, backup_ext=".bak", encoding="utf-8") as config_file:
            for line in config_file:
                if target_line in line:
                    config_file.write(line.replace(line, new_line))
                else:
                    config_file.write(line)
