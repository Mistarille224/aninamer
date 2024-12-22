import os
from conf import ensure_config_exists
from tree import tree
from watcher import watch

if __name__ == '__main__':
    ensure_config_exists()
    tree()
    if os.name=='nt':
        import threading
        from tray import create_tray_icon
        threading.Thread(target=create_tray_icon).start()
    watch()