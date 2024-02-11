from re import findall,sub,search
from pathlib import Path,PurePosixPath
from conf import data
from shutil import move


path = rf'{data["path"]["input_path"]}'

# 获取文件列表
def get_list(scripts,bool=True):
    if bool is False:
        return [str(file_path) for file_path in Path(scripts).glob('**/*') if file_path.is_dir()]
    else:
        return [str(file_path) for file_path in Path(scripts).iterdir() if file_path.is_file()]

# 提取规则内数字
def get_number(re,scripts):
     return int(sub(r'\D+','',str(findall(re,scripts))))

def season_move():
    sub_paths = get_list(path,False)
    for sub_path in sub_paths:
        # 循环检测有'-'的文件夹
        while search(r'S\d+-',sub_path):
            # 保留原文件目录
            origins = get_list(sub_path)
            num_origins = [(get_number(r'E\d+',ep),PurePosixPath(ep).suffix) for ep in origins]
            # 文件名合法化
            Season = get_number(r'S\d+-',sub_path)
            if Season >= 10:
                sub_path = sub(r'S\d+-','S'+str(Season-1),sub_path)
            else:
                sub_path = sub(r'S\d+-','S0'+str(Season-1),sub_path)
            # 回到循环
            if sub_path + '-' in sub_paths:
                sub_path = sub_path + '-'
            # 提取上季视频文件
            last_s = get_list(sub_path)
            last_v = []
            for item in last_s:
                if item.endswith(('.mp4','.mkv','.flv','.mov','.avi')) and '..'not in item :
                    last_v.append(item)
            #获得最大值
            num_last = [(get_number(r'E\d+',ep), ep) for ep in last_v]
            last_ep = sub(r'.\w+$','',max(num_last, key=lambda x: x[0])[1])
            last_num = sub(r'\d+$','',last_ep)
            #重命名
            for origin,num_origin in zip(origins,num_origins):
                num_origin = last_num + str(get_number(r'E\d+',last_ep) + num_origin[0]) +'.' + num_origin[1]
                # 移动文件
                move(origin, num_origin)

season_move()