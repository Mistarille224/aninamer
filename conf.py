from tomllib import load as toml_load
from toml import dump
from pathlib import Path

def create_conf():
    # 引入配置文件
    toml_path = Path('./conf/config.toml')
    if not toml_path.exists():
        mk_conf = Path('conf')
        mk_conf.mkdir(exist_ok=True)
        init = {'path': {'input_path': 'D:/download/videohlink/anime'}, 'special': {'special_before': ['[Nekomoe kissaten][', '16bit ', 'S2'], 'special_after': ['', 'Sixteen bit ', 'S02']}}
        with open('./conf/config.toml', 'w') as w:
            dump(init, w)
        w.close
        with open('./conf/config.toml','rb') as r:
            data = toml_load(r) 

create_conf()

with open('./conf/config.toml','rb') as r:
    data = toml_load(r) 