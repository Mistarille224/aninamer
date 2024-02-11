from conf import create_conf
from log import create_log,clean_log
from tray import create_tray_icon
from watcher import watch
import threading

if __name__ == '__main__':
    # 创建配置文件
    create_conf()
    # 创建当日日志
    create_log()
    # 清除一月前日志
    clean_log()
    t = threading.Thread(target=watch) # 创建一个新的线程，目标函数为 watch
    t.start() # 启动线程
    create_tray_icon()