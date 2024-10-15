from time import sleep
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tree import tree, save_tree_to_json, read_tree_from_json
from rename import rename
from conf import data

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        json_path = Path('./conf/directory_tree.json')
        if not json_path.exists():
            save_tree_to_json({})
        tree(read_tree_from_json())

class JsonHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            rename(True, read_tree_from_json())
        except:
            sleep(1)
            rename(True, read_tree_from_json())

def watch():
    watch_json = Observer()
    watch_json.schedule(JsonHandler(), "./conf", recursive=False)

    watch_file = Observer()
    input_path = rf'{data["path"]["input_path"]}'
    watch_file.schedule(FileHandler(), input_path, recursive=True)

    watch_json.start()
    watch_file.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        watch_json.stop()
        watch_file.stop()

    watch_json.join()
    watch_file.join()
