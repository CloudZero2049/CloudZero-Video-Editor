from editor_engine import *
from editor_GUI import *
from PySide6.QtWidgets import QApplication
import requests
import json
# 00:01:00.00
# 01:00
# 00:04
# last changes and notes:
# checking if window.windowTitle() works

# To do list:
# [] draging in timeline causes errors. Need to setup timeline logic and dragging
# [] Video player previews
# [x] Fix video and audio Split logic
# [x] User Settings and estimated export times (JSON)
# [x] Check for updates
# [x] check for time difference in resolution re-scaling and adjust
# [] Splitting causing video size mismatch??

# [] Create logging system
# [] Copy and Paste clips
# [] Change time estimates from point minutes to minutes:seconds
# [] insert_text_frame    
# [] insert_black_fade   
# [] insert_sound_fade    
# [] edit_volume
      

VERSION = "0.1.5"
VERSION_URL = "https://raw.githubusercontent.com/CloudZero2049/CloudZero-Video-Editor/main/VERSION.json"
UPDATE_URL = "https://github.com/CloudZero2049/CloudZero-Video-Editor/releases/latest/download/CloudZero_Video_Editor.exe"
SETTINGS_FILE = "CZVE_Settings.json"


class CloudZeroVideoEditor():
    def __init__(self):
        self.editor = EditorEngine()
        self.app = QApplication()
        self.main_window = None
        self.editor.main_window = None
    
        self.username = "person"
        self.low_timings = []
        self.low_timings_max = []
        self.mid_timings = []
        self.mid_timings_max = []
        self.high_timings = []
        self.high_timings_max = []
        self.max_timings = 10


    def check_for_update(self, mainWindow):
        try:
            response = requests.get(VERSION_URL, timeout=10)
            
            if response.status_code == 200:
                version_data = response.json()
                latest = version_data.get("version", VERSION)
                if latest != VERSION:
                    mainWindow.new_version_popup(VERSION, latest)
                    
            else:
                print("Failed to fetch version info.")
        except Exception as e:
            print(f"Error checking version: {e}")

    def check_resources(self):
        output_dir = os.path.dirname("editor_clips/")
        if output_dir:  # avoid empty string if no directory in path
            # exist_ok=True means it won't raise an error if the folder already exists, so no need for a manual check first. 
            os.makedirs(output_dir, exist_ok=True)

    def load_settings(self):
        
        if not os.path.exists(SETTINGS_FILE):
            print("no settings to load from")
            return
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
               
                self.username = (data.get("username", "person"))
                self.low_timings = (data.get("low_timings", []))
                self.low_timings_max = (data.get("low_timings_max", []))
                self.mid_timings = (data.get("mid_timings", []))
                self.mid_timings_max = (data.get("mid_timings_max", []))
                self.high_timings = (data.get("high_timings", []))
                self.high_timings_max = (data.get("high_timings_max", []))
                self.max_timings = (data.get("max_timings", 10))
                # Anything below this line could be part of a new version
                
                if data.get("version", "") != VERSION:
                    # messagebox.showinfo("Settings file doesn't match client", f"The new version will overwrite the old saved settings when closed. You can open the settings JSON file and save the data manualy if you're afraid of losing it")
                    return    

        except Exception as e:
            print(f'failed to load settings: {e}')
            # update_status(f"Failed to load settings: {e}","red")

    def save_settings(self):
        try:
            data = {
                "version": VERSION,
                "username": self.username,
                "low_timings": self.low_timings, # 
                "low_timings_max": self.low_timings_max,
                "mid_timings": self.mid_timings,
                "mid_timings_max": self.mid_timings_max,
                "high_timings": self.high_timings,
                "high_timings_max": self.high_timings_max,
                "max_timings": self.max_timings
            }
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f'failed to save settings {e}')
            #update_status(f"Failed to save settings: {e}","red")

    def update_log(self, data):
         pass
    
    def clear_log(self):
         pass

    def master_shutdown(self):
            print("Shutting down application...")
            self.save_settings()
            self.editor.shutdown()
            self.main_window.shutdown()



def main():
    try:
        CZVE = CloudZeroVideoEditor()
        # CZVE.editor = EditorEngine()
        # CZVE.app = QApplication()
        CZVE.main_window = MainWindow(CZVE, CZVE.editor)
        CZVE.editor.main_window = CZVE.main_window
        CZVE.main_window.show()
        CZVE.app.exec()
    except Exception as e:
         print(f'An error has occurred: {e}')
    

if __name__ == "__main__":
    main()