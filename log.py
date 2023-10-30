import os
from datetime import date

log_path = './log/'
today_date = str(date.today())
def clean_log():
    global log_path
    global today_date
	
    # 遍历目录下的所有日志文件
    for log in os.listdir(log_path):
        file_path = log_path + log      

    # 获取日志的年月，和今天的年月
        today_month = int(today_date[5:7])# 今天的月份
        log_month = int(log[5:7])# 日志的月份
        today_year = int(today_date[0:4])# 今天的年份
        log_year = int(log[0:4])# 日志的年份
    # 对上个月的日志进行清理
        if(log_month < today_month):
            if(os.path.exists(file_path)):# 判断生成的路径对不对，防止报错
                os.remove(file_path)# 删除文件
        elif(log_year < today_year):
            if(os.path.exists(file_path)):
                os.remove(file_path)
