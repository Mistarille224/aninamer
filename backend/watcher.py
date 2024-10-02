import logging
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from time import sleep
from rename import rename
from conf import data
from season import move_season_files


class RenameHandler(FileSystemEventHandler):
    def on_created(self, event):
        rename()
        move_season_files()
    def on_deleted(self, event):
        # 处理文件删除事件
        pass

    def on_modified(self, event):
        # 处理文件修改事件
        if '.' in event.src_path:
            logging.info(f'File modified: {event.src_path}')
    
def watch():
    # 监测的文件夹路径
    input_path = rf'{data["path"]["input_path"]}'
    observer = Observer()
    event_handler = RenameHandler()
    observer.schedule(event_handler, input_path, True)
    observer.start()
    try:
        while True:
            sleep(20)
    except KeyboardInterrupt:
        observer.stop()
