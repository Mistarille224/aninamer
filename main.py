from conf import create_conf
from log import create_log,clean_log
from tray import create_tray_icon
from watcher import watch
from tendo import singleton

me = singleton.SingleInstance()
     
# 创建配置文件
create_conf()

# 创建当日日志
create_log()

# 清除一月前日志
clean_log()


if __name__ == '__main__':
    create_tray_icon()
    watch()