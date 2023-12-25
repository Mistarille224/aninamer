import logging
from pathlib import Path
from conf import create_conf
from log import log_path,today_date,clean_log
from tray import create_tray_icon
from watcher import watch

     
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
    create_tray_icon()
    watch()