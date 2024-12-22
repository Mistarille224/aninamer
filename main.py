from conf import ensure_config_exists
from tree import tree
from watcher import watch

if __name__ == '__main__':
    ensure_config_exists()
    tree()
    watch()