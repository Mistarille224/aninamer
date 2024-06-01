from conf import create_conf
from log import create_log,clean_log
from tray import create_tray_icon
from watcher import watch
import threading

if __name__ == '__main__':
    create_conf()
    create_log()
    clean_log()
    threading.Thread(target=watch).start()
    threading.Thread(target=create_tray_icon).start()