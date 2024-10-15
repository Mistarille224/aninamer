import json
from os.path import getctime
from os import fsync
from pathlib import Path
from re import sub
from conf import data

def read_tree_from_json():
    with Path("./conf/directory_tree.json").open('r', encoding='utf-8') as f:
        conf = json.load(f)
        return conf

def save_tree_to_json(tree):
    with open('./conf/directory_tree.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)
        fsync(f.fileno())

def tree(conf):
    def load_rules(name):
        before = []
        after = []
        for sp in data['rules']['special']:
            before.append(str(sp[0]))
            after.append(str(sp[1]))
        for bfr, aft in zip(before, after):
            name = name.replace(bfr, aft)
        return name

    def default_rules(name):
        name = name.replace('(', '<').replace(')', '>')
        name = name.replace('[', '(').replace(']', ')').replace('_', ' ')
        name = sub(r'\((\d+)\)',  r' E\1 ', name)
        name = sub(r' (\d+) ',  r' E\1 ', name)
        name = sub(r'(\d+)\-(\d+)', r' E\1-E\2 ', name)
        name = name.replace(' - ',' ')
        name = name.replace('(v2)',' - v2 ')
        name = sub(r'\((\d+)v2\)', r' E\1 - v2 ', name)
        name = sub(r'\( E(\d+)', r'E\1', name)
        name = sub(r'\([^)]*\)', '', name)
        name = name.replace('  ', ' ').strip()
        name = name.replace(' .', '.').replace(')', '')
        name = name.replace('<', '(').replace('>', ')')
        name = sub(r'^\s', '', name)
        return name

    def build_tree(paths, last_conf):
        def inner_build_tree(current_path, last_conf):
            tree = {}
            for item in current_path.iterdir():
                if item.is_dir():
                    if item.name in last_conf:
                        tree[item.name] = [last_conf[item.name][0], inner_build_tree(item, last_conf[item.name][1])]
                    else:
                        tree[item.name] = [True, inner_build_tree(item, {})]
                else:
                    tag = f'{item.stat().st_size}/{getctime(item.resolve())}'
                    if tag in last_conf:
                        if item.name == last_conf[tag][2] and not default_rules(load_rules(last_conf[tag][1])) == last_conf[tag][2]:
                             item.rename(f'{item.parent.resolve()}/{default_rules(load_rules(last_conf[tag][1]))}')
                        tree[tag] = [last_conf[tag][0], last_conf[tag][1], default_rules(load_rules(last_conf[tag][1]))]
                    else:
                        tree[tag] = [True, item.name, default_rules(load_rules(item.name)) if '[' in item.name else '']
            return tree
        result = {}
        for path in paths:
            if path in last_conf:
                result[path] = [last_conf[path][0], inner_build_tree(Path(path), last_conf[path][1])]
            else:
                result[path] = [True, inner_build_tree(Path(path), {})]
        return result

    tree = build_tree([data['path']['input_path']], conf)

    save_tree_to_json(tree)

