import pystray
from PIL import Image
import os
from rename import rename
from tree import read_tree

def open_app():
    os.system(f'start {"./conf/paths.json"}')
def exit_app():
    os._exit(0)
    
def create_tray_icon():
    image = Image.open("./lib/icon.ico")
    menu = (
        pystray.MenuItem("Rename", lambda: rename(True,read_tree())),
        pystray.MenuItem("Recover", lambda: rename(False,read_tree())),
        pystray.MenuItem("Click to open config file", lambda: open_app()),
        pystray.MenuItem("Exit", lambda: exit_app())
    )
    tray_icon = pystray.Icon("app_name", image, "aninamer", menu)
    tray_icon.tooltip = "Application"
    tray_icon.run()
