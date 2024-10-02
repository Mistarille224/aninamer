from functools import partial
import os
import threading
from conf import create_conf
from log import create_log,clean_log
from tray import create_tray_icon
from watcher import watch

if __name__ == '__main__':
    create_conf()
    create_log()
    clean_log()
    if os.name=='nt':
        threading.Thread(target=create_tray_icon).start()
    threading.Thread(target=partial(watch())).start()