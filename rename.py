from re import sub
from pathlib import Path
from conf import data
from copy import deepcopy

def rename():
    # 引入配置文件
    before = []
    after = []
    for sp in  data["rules"]["special"]:
        # 把元组的第一项转换为字符串并添加到first_items列表中
        before.append(str(sp[0]))
        # 把元组的第二项转换为字符串并添加到second_items列表中
        after.append(str(sp[1]))

    # 引入处理目录
    path = Path(rf'{data["path"]["input_path"]}')

    # 递归子文件夹
    files = [str(file_path) for file_path in path.glob('**/*') if file_path.is_file()]
    
    origin_path = Path(rf'{data["path"]["origin_path"]}')    
    if not origin_path == "":
        origin_files = [str(file_path) for file_path in origin_path.glob('**/*') if file_path.is_file()]
        for origin_name in origin_files:
         if 'v2' in origin_name:
            if origin_name.replace('v2', '') in origin_files:
                    n = origin_name.replace('v2', '')
                    if '[]' in n:
                        Path(n).replace('[]', '').unlink()
                    else:
                        Path(n).unlink()


    # 处理规则
    for name in files:
        origin = deepcopy(name)
        if '[' in name:
             # 引入特殊配置
            for bfr,aft in zip(before,after):
                name = name.replace(bfr,aft)
            # 引入固有配置
            standardize = name.replace('_', ' ').replace('Season ','S').replace('(', '<').replace(')', '>').replace('v2', '')
            substitute = standardize.replace('[', '(').replace(']', ')')
            episode = sub(r'\((\d+)\)', lambda match: ' E' + match.group(1) + ' ', substitute)
            episode = sub(r'\s(\d+)\s', lambda match: ' E' + match.group(1) + ' ', episode)
            episode = sub(r'(\d+)\-(\d+)', lambda match: ' E' + match.group(1) + ' ', episode)
            simplify = sub(r'(\D)\-(\D)', lambda match: match.group(1).replace ('-', ' '), episode)
            simplify = sub(r'\([^)]*\)', '', simplify)
            while '  ' in simplify:
                simplify = simplify.replace('  ', ' ')
            simplify = sub(r'^ ','', simplify)
            remove_space = simplify.replace(' .', '.')
            new_name = remove_space.replace(')', '').replace('<', '(').replace('>', ')')

            if 'v2' in origin:
                if new_name in files:
                    Path(new_name).unlink()
            # 重命名操作
            Path(origin).rename(Path(new_name))

rename()