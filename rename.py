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

    # 处理规则
    for names in files:
        origin = deepcopy(names)
        if '[' in names:
             # 引入特殊配置
            for bfr,aft in zip(before,after):
                names = names.replace(bfr,aft)
            # 引入固有配置
            standardize = names.replace('_', ' ').replace('Season ','S').replace('(', '<').replace(')', '>').replace('v2', '')
            substitute = standardize.replace('[', '(').replace(']', ')')
            episode = sub(r'\((\d+)\)', lambda match: ' E' + match.group(1) + ' ', substitute)
            episode = sub(r'\s(\d+)\s', lambda match: ' E' + match.group(1) + ' ', episode)
            episode = sub(r'(\d+)\-(\d+)', lambda match: ' E' + match.group(1) + ' ', episode)
            simplify = sub(r'(\D+)\-(\D+)', lambda match: match.group(1).replace ('-', ' '), episode)
            simplify = sub(r'\([^)]*\)', '', simplify)
            while '  ' in simplify:
                simplify = simplify.replace('  ', ' ')
            remove_space = simplify.replace(' .', '.')
            new_names = remove_space.replace(')', '').replace('<', '(').replace('>', ')')
        
            #字符串转换为目录
            filenames = Path(origin)
            new_filenames = Path(new_names)
            # 重命名操作
            filenames.rename(new_filenames)
