from pathlib import Path, PurePosixPath
from re import findall, sub, search
from shutil import move
from time import sleep
from conf import data


input_path = rf'{data["path"]["input_path"]}'

# 遍历文件生成列表
def get_file_list(directory, include_files=True):
    if include_files:
        return [str(file_path) for file_path in Path(directory).iterdir() if file_path.is_file()]
    else:
        return [str(file_path) for file_path in Path(directory).glob('**/*') if file_path.is_dir()]

# 提取规则内数字
def extract_number(pattern, text):
    return int(sub(r'\D+', '', str(findall(pattern, text))))

# 移动文件
def move_season_files():
    sub_paths = get_file_list(input_path, include_files=False)
    for sub_path in sub_paths:
        while search(r'\d+-', sub_path):
            original_files = get_file_list(sub_path)
            num_origins = [(extract_number(r'E\d+', ep), PurePosixPath(ep).suffix) for ep in original_files]
            season_number = extract_number(r'\d+-', sub_path)
            sub_path = sub(r'\d+-', str(season_number - 1), sub_path)
            if sub_path + '-' in sub_paths:
                sub_path += '-'
            last_season_files = get_file_list(sub_path)
            video_files = [item for item in last_season_files if item.endswith(('.mp4', '.mkv', '.flv', '.mov', '.avi')) and '..' not in item]
            ep_list = [(extract_number(r'E\d+', ep), ep) for ep in video_files]
            final_ep = sub(r'.\w+$', '', max(ep_list, key=lambda x: x))
            final_num = sub(r'\d+$', '', final_ep)
            for origin, num_origin in zip(original_files, num_origins):
                new_name = final_num + str(extract_number(r'E\d+', final_ep) + num_origin) + '.' + num_origin
                try:
                    move(origin, new_name)
                except Exception as e:
                    sleep(1)
                    try:
                        move(origin, new_name)
                    except Exception as e:
                        return f"Error when moving video file to last season: {e}"