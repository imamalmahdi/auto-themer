from pathlib import Path
import json

CURRENT_DIR = Path(__file__).parent.absolute()

def get_config():
    settings_file = Path(f"{str(CURRENT_DIR)}\\settings.json")
    if settings_file.exists() == False:
        settings = {
            "time" : {
                "light": 5,
                "dark": 17
            },
            "rainmeter": [
                False, 
                [
                    ""
                ]
            ],
            "windows": False,
            "wallpaper": [
                False, {
                    "light": "",
                    "dark": ""
                }
            ],
            "terminal": [
                False, {
                    "light": "",
                    "dark": ""
                }
            ],
            "vscode": [
                False, {
                    "light": "",
                    "dark": ""
                }
            ],
            "spotify": [
                False, {
                    "light": "",
                    "dark": ""
                }
            ],
            "sumatrapdf": [
                False, {
                    "light": {
                        "text": "",
                        "background": ""
                    },
                    "dark": {
                        "text": "",
                        "background": ""
                    }
                }
            ]
        }

        settings_file.write_text(json.dumps(settings, indent=4))
    
    return json.loads(settings_file.read_text())