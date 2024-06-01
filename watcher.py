import logging
from rename import rename
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from time import sleep
from conf import data
from season import season_move
from tkinter import Tk,Label


def exit_window(error="未知错误",info=""):   
    # 创建窗口
    window = Tk()
    window.title("Aninamer") # 设置窗口标题
    window.iconbitmap("lib/icon.ico") # 设置窗口标题
    window.eval('tk::PlaceWindow . center')
    # 创建一个文本标签，设置对齐方式为居中
    label = Label(window, text = error +"，程序退出。\n"+ info , anchor = 'center')
    # 获取标签的请求宽度和高度
    width = label.winfo_reqwidth() + 80
    height = label.winfo_reqheight() + 48
    # 设置窗口的大小和位置
    window.geometry(f'{width}x{height}')
    # 将标签放置在窗口中
    label.place(relx=0.5, rely=0.5, anchor='center')
    # 主窗口循环运行
    window.mainloop()
    exit()


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # 处理文件新增事件
        try:
            rename()
            season_move()
        except Exception as e:
            exit_window("重命名错误",e)
        
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
