from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from conf import config
from rename import rename
from tree import tree, read_tree

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        tree()
        rename(True, read_tree())

def watch():
    watch_file = Observer()
    input_paths = config["paths"]
    for input_path in input_paths:
        watch_file.schedule(FileHandler(), input_path, recursive=True)
    watch_file.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        watch_file.stop()