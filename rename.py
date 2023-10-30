from re import sub
from pathlib import Path
from conf import data

def rename():
    # 引入配置文件
    before =['"' + bef + '"' for bef in data["special"]["special_before"]]
    after =['"' + aft + '"' for aft in data["special"]["special_after"]]
    replace = [f'{bef},{aft}' for bef, aft in zip(before,after)]

    # 引入处理目录
    path = Path(rf'{data["path"]["input_path"]}')

    # 递归子文件夹
    files = [str(file_path) for file_path in path.glob('**/*') if file_path.is_file()]

    # 处理规则
    for names in files:
       if '[' in names:
           # 将配置文件转换为代码
            special = eval('names.replace(' + ').replace('.join(replace) + ')')
            # 固有配置
            standardize = special.replace('[1080P]', '').replace(' - ', ' ').replace('[1080p]', '').replace("Season ","S").replace(' [', '[').replace('] ', ']').replace('(', '<').replace(')', '>')
            substitute = standardize.replace('[', '(').replace(']', ')')
            episode = substitute.replace('(0', ' E0').replace('(1', ' E1').replace('(2', ' E2').replace(' 0', ' E0').replace(' 1', ' E1').replace(' 2', ' E2')
            remove_brackets = sub(r'\([^)]*\)', '', episode)
            new_names = remove_brackets.replace(')', '').replace('<', '(').replace('>', ')')
        
            #字符串转换为目录
            filenames = Path(names)
            new_filenames = Path(new_names)
            # 重命名操作
            filenames.rename(new_filenames)

rename()