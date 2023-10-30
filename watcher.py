import logging
from rename import rename
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # 处理文件新增事件
        rename()
    
    def on_deleted(self, event):
        # 处理文件删除事件
        pass

    def on_modified(self, event):
        # 处理文件修改事件
        if '.' in event.src_path:
            logging.info(f'File modified: {event.src_path}')