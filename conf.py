from tomllib import load as toml_load
from toml import dumps
from pathlib import Path
from os import system

def create_conf():
    # 引入配置文件
    toml_path = Path('./conf/config.toml')
    if not toml_path.exists():
        mk_conf = Path('conf')
        mk_conf.mkdir(exist_ok=True)
        init = {'path': {'input_path': 'D:/download/videohlink/anime'}, 'rules': {'special': [["[Nekomoe kissaten][","",],["S2","S02",]]}}
        toml_str = dumps(init)
        toml_str = toml_str + "\n# 参考上文修改配置文件。确保标题不被包括在[]内，否则参考 *把\"[Nekomoe kissaten][\"替换成\"\"即为删除。*  来让标题暴露出来。\n# special按格式添加新条目就好,前一项是修改前的,后一项是修改后的。如果觉得不喜欢这两项,可以删除,但通常是不必要的。\n# 删除方法如第一项所示,把\"[Nekomoe kissaten][\"替换成\"\"即为删除。\n# 修改方式如第二项所示,把\"S2\"替换成\"S02\"即为修改。\n# 如果修改之后出现问题或者有各种情况希望恢复初始状态,直接删除这个toml文件即可,程序会为你重新生成一份默认配置文件。\n# 所以,初次见面,亦或是再次修改,也可能是删除后重新来过,不论如何,祝你好运！\n\n# Refer to the above to modify the configuration file.Make sure the title is not surrounded by [], If not, please refer to *Replace \"[Nekomoe kissaten][\" with \"\" to delete.* to expose the title.\n# Special Just add new entries according to the format. The former item is before modification, and the latter item is after modification. You can delete these items if you feel you don't like them, but they are usually unnecessary.\n# The deletion method is as shown in the first item. Replace \"[Nekomoe kissaten][\" with \"\" to delete.\n# The modification method is as shown in the second item, replacing \"S2\" with \"S02\" to modify.\n# If there are problems after modification or there are various situations where you want to restore the initial state, just delete the toml file and the program will regenerate a default configuration file for you.\n# So, it's the first time to meet, or it may be modified again, or it may be deleted and started again, no matter what, GOOD LUCK!"
        with open('./conf/config.toml', 'w',encoding="utf-8") as w:
            w.write(toml_str)
        w.close
        system(f'start {"./conf/config.toml"}')

create_conf()

with open('./conf/config.toml','rb') as r:
    data = toml_load(r) 