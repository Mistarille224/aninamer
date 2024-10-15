import os
import pystray
from PIL import Image
from tree import read_tree_from_json
from rename import rename

def create_tray_icon():
    image = Image.open("./lib/favicon.ico")
    menu = (
        pystray.MenuItem("手动重命名", lambda: rename(True, read_tree_from_json())),
        pystray.MenuItem("还原所有文件名", lambda: rename(False, read_tree_from_json())),
        pystray.MenuItem("点击打开config文件", lambda: open_app()),
        pystray.MenuItem("退出", lambda: exit_app())
    )
    tray_icon = pystray.Icon("app_name", image, "aninamer", menu)
    tray_icon.tooltip = "应用程序"
    tray_icon.run()

def open_app():
    os.system(f'start {"./conf/config.toml"}')

def exit_app():
    os._exit(0)
