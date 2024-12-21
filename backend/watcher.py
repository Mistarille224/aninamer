from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tree import tree, read_tree_from_json
from rename import rename
from conf import config,CONFIG_PATH

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        tree()

class TreeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            rename(True, read_tree_from_json())
        except:
            sleep(1)
            rename(True, read_tree_from_json())


watch_json = Observer()
watch_json.schedule(TreeHandler(), CONFIG_PATH, recursive=False)

watch_file = Observer()
input_paths = config["paths"]
for input_path in input_paths:
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
