import logging
from rename import rename
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from time import sleep
from conf import data

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
    
def watch():
    # 监测的文件夹路径
    input_path = rf'{data["path"]["input_path"]}'
    # 创建Observer对象
    observer = Observer()
    # 创建事件处理对象
    event_handler = MyHandler()
    # 将事件处理对象注册到Observer对象中
    observer.schedule(event_handler, input_path, True)
    # 启动Observer对象
    observer.start()
    try:
        while True:
            sleep(20)
    except KeyboardInterrupt:
        observer.stop()
