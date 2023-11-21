from time import sleep
import logging
from watchdog.observers import Observer
from log import log_path,today_date,clean_log
from watcher import MyHandler
from tray import create_tray_icon
from pathlib import Path
from conf import data,create_conf

# 创建配置文件
create_conf()

# 创建当日日志
mk_log = Path('log')
mk_log.mkdir(exist_ok=True)
logging.basicConfig(filename=f'{log_path}{today_date} change.txt',encoding='utf-8',level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# 清除一月前日志
clean_log()


if __name__ == '__main__':
    
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
    create_tray_icon()

    try:
        while True:
            sleep(20)
    except KeyboardInterrupt:
        observer.stop()