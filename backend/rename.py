from re import sub
from pathlib import Path
from conf import data
from time import sleep


# 递归子文件夹
def get_files(path):
    return [str(file_path) for file_path in path.glob('**/*') if file_path.is_file()]

# 操作原文件夹
def process_origin_files(origin_path):
    if origin_path:
        origin_files = get_files(origin_path)
        for origin_name in origin_files:
            if 'v2' in origin_name:
                n = origin_name.replace('v2', '')
                if n in origin_files:
                    if '[]' in n:
                        Path(n.replace('[]', '')).unlink()
                    else:
                        Path(n).unlink()

# 重命名操作
def rename_files(files):
    for name in files:
        origin = name
        if '[' in name:
            name = load_rules(name)
            new_name = default_rules(name)
            try:
                Path(origin).rename(Path(new_name))
            except:
                sleep(1)
                try:
                    Path(origin).rename(Path(new_name))
                except Exception as e:
                    return f"Error when renaming: {e}"
                
# 获取规则
def load_rules(name):
    before = []
    after = []
    for sp in data["rules"]["special"]:
        before.append(str(sp[0]))
        after.append(str(sp[1]))
    for bfr, aft in zip(before, after):
        name = name.replace(bfr, aft)
    return name

# 默认规则
def default_rules(name):
    name = name.replace('(', '<').replace(')', '>')
    name = name.replace('[', '(').replace(']', ')').replace('_', ' ')
    name = sub(r'\((\d+)\)', lambda match: ' E' + match.group(1) + ' ', name)
    name = sub(r'\s(\d+)\s', lambda match: ' E' + match.group(1) + ' ', name)
    name = sub(r'(\d+)\-(\d+)', lambda match: ' E' + match.group(1) + ' ', name)
    name = sub(r'\s\-\s', ' ', name)
    name = sub(r'\((\d+)v2\)', lambda match: ' E' + match.group(1) + ' - v2 ', name)
    name = name.replace('(v2)',' - v2 ')
    name = sub(r'\([^)]*\)', '', name)
    name = name.replace('  ', ' ').strip()
    name = name.replace(' .', '.').replace(')', '')
    name = name.replace('<', '(').replace('>', ')')
    name = sub(r'^\s+', '', name)
    return name

def rename():
    origin_path = Path(data["path"]["origin_path"])
    process_origin_files(origin_path)

    path = Path(data["path"]["input_path"])
    files = get_files(path)
    rename_files(files)
