import pystray
from PIL import Image
from os import _exit ,system
from watcher import rename

# 创建系统托盘图标
def create_tray_icon():
    # 从图片文件中加载图标
    image = Image.open("./icon/icon.png")

    # 创建系统托盘菜单
    menu = (
        pystray.MenuItem("手动重命名", lambda: rename()),
        pystray.MenuItem("点击打开config文件", lambda: open_app()),
        pystray.MenuItem("退出", lambda: exit_app())
    )

    # 创建系统托盘图标
    tray_icon = pystray.Icon("app_name", image, "aninamer", menu)

    # 设置图标的提示文本
    tray_icon.tooltip = "应用程序"

    # 显示系统托盘图标
    tray_icon.run()

# 点击“打开应用”菜单项的事件处理函数
def open_app():
    # TODO: 打开应用的具体逻辑
    system(f'start {"./conf/config.toml"}')

# 点击“退出”菜单项的事件处理函数
def exit_app():
    # TODO: 退出应用的具体逻辑
    _exit(0)