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
        pystray.MenuItem("手动重命名", lambda: rename(True,read_tree())),
        pystray.MenuItem("还原所有文件", lambda: rename(False,read_tree())),
        pystray.MenuItem("点击打开配置文件", lambda: open_app()),
        pystray.MenuItem("退出", lambda: exit_app())
    )
    tray_icon = pystray.Icon("app_name", image, "aninamer", menu)
    tray_icon.tooltip = "应用程序"
    tray_icon.run()
