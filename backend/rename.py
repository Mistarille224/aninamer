from re import sub
from pathlib import Path
from conf import data
from time import sleep

# 获取规则
def load_rules():
    before = []
    after = []
    for sp in data["rules"]["special"]:
        before.append(str(sp))
        after.append(str(sp))
    return before, after

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
def rename_files(files, before, after):
    for name in files:
        origin = name
        if '[' in name:
            for bfr, aft in zip(before, after):
                name = name.replace(bfr, aft)
            new_name = default_rules(name)
            if 'v2' in origin and new_name in files:
                Path(new_name).unlink()
            try:
                Path(origin).rename(Path(new_name))
            except:
                sleep(1)
                try:
                    Path(origin).rename(Path(new_name))
                except Exception as e:
                    return f"Error when renaming: {e}"

# 默认规则
def default_rules(name):
    name = name.replace('(', '<').replace(')', '>')
    name = name.replace('[', '(').replace(']', ')').replace('v2', '').replace('_', ' ')
    name = sub(r'\((\d+)\)', lambda match: ' E' + match.group(1) + ' ', name)
    name = sub(r'\s(\d+)\s', lambda match: ' E' + match.group(1) + ' ', name)
    name = sub(r'(\d+)\-(\d+)', lambda match: ' E' + match.group(1) + ' ', name)
    name = sub(r'\([^)]*\)', '', name)
    name = name.replace('  ', ' ').strip()
    name = sub(r'^\s*', '', name)
    name = name.replace(' .', '.').replace(')', '')
    name = name.replace('<', '(').replace('>', ')')
    return name

def rename():
    before, after = load_rules()
    path = Path(data["path"]["input_path"])
    files = get_files(path)
    origin_path = Path(data["path"]["origin_path"])
    process_origin_files(origin_path)
    rename_files(files, before, after)

rename()
