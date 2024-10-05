import tomllib
from toml import dumps
from pathlib import Path

def create_conf():
    # 引入配置文件
    toml_path = Path('./conf/config.toml')
    if not toml_path.exists():
        mk_conf = Path('conf')
        mk_conf.mkdir(exist_ok=True)
        init = {
            'path': {
                'input_path': 'D:/download/videohlink/anime',
                'origin_path': ''
            },
            'rules': {
                'special': [
                    ["[Nekomoe kissaten][", ""],
                    ["S2", "S02"]
                ]
            }
        }
        toml_str = dumps(init) + """
# 请务必修改路径input_path为你的目录（而不是我的），如果使用了硬链接，请在origin_path中填写原目录。
# 参考上文修改配置文件。确保标题不被包括在[]内，否则参考 *把"[Nekomoe kissaten]["替换成""即为删除。*  来让标题暴露出来。
# special按格式添加新条目就好,前一项是修改前的,后一项是修改后的。如果觉得不喜欢这两项,可以删除,但通常是不必要的。
# 删除方法如第一项所示,把"[Nekomoe kissaten]["替换成""即为删除。
# 修改方式如第二项所示,把"S2"替换成"S02"即为修改。
# 为季文件夹加上"-"后缀，比如把"videopath\S02\\E??.mp4"修改为"videopath\S02-\\E??.mp4"。可以自动将文件移动到上一季，并重命名。
# 如果修改之后出现问题或者有各种情况希望恢复初始状态,直接删除这个toml文件即可,程序会为你重新生成一份默认配置文件。
# 所以,初次见面,亦或是再次修改,也可能是删除后重新来过,不论如何,祝你好运！

# Please be sure to modify the path input_path(DO NOT USE MINE). If a hard link is used, please fill the original directory in origin_path.
# Refer to the above to modify the configuration file. Make sure the title is not surrounded by [], If not, please refer to *Replace "[Nekomoe kissaten][" with "" to delete.* to expose the title.
# Special Just add new entries according to the format. The former item is before modification, and the latter item is after modification. You can delete these items if you feel you don't like them, but they are usually unnecessary.
# The deletion method is as shown in the first item. Replace "[Nekomoe kissaten][" with "" to delete.
# The modification method is as shown in the second item, replacing "S2" with "S02" to modify.
# Add "-" suffix to the season folder, for example, change "videopath\S02\\E??.mp4" to "videopath\S02-\\E??.mp4".Files can be automatically moved to the previous season and renamed.
# If there are problems after modification or there are various situations where you want to restore the initial state, just delete the toml file and the program will regenerate a default configuration file for you.
# So, it's the first time to meet, or it may be modified again, or it may be deleted and started again, no matter what, GOOD LUCK!
"""
        with open(toml_path, 'w', encoding="utf-8") as w:
            w.write(toml_str)
        print(f'Configuration file created at {toml_path}')
        return

create_conf()

with open('./conf/config.toml', 'rb') as r:
    data = tomllib.load(r)

def modify_conf(new_config):
    with open('./conf/config.toml', 'w') as f:
            f.write(dumps(new_config))
