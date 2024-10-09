import json
from pathlib import Path
from re import sub
from conf import data

def rename(direction=True):
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
        name = sub(r'(\d+)\-(\d+)', lambda match: ' E' + match.group(0) + ' ', name)
        name = sub(r'\s\-\s', ' ', name)
        name = sub(r'\((\d+)v2\)', lambda match: ' E' + match.group(1) + ' - v2 ', name)
        name = name.replace('(v2)',' - v2 ')
        name = sub(r'\(\sE(\d+)', lambda match: match.group(0).replace('(',''), name)
        name = sub(r'\([^)]*\)', '', name)
        name = name.replace('  ', ' ').strip()
        name = name.replace(' .', '.').replace(')', '')
        name = name.replace('<', '(').replace('>', ')')
        name = sub(r'^\s+', '', name)
        return name

    def save_tree_to_json(tree):
        with open('./conf/directory_tree.json', 'w', encoding='utf-8') as f:
            json.dump(tree, f, ensure_ascii=False, indent=4)

    def build_tree(paths, last_conf):
        def inner_build_tree(current_path, last_conf):
            tree = {}
            for item in current_path.iterdir():
                if item.name in last_conf:
                    if item.is_dir():
                        tree[item.name] = [inner_build_tree(item, last_conf[item.name][0]), last_conf[item.name][1]]
                    else:
                        tree[item.name] = last_conf[item.name]
                else:
                    if item.is_dir():
                        tree[item.name] = [inner_build_tree(item, {}), True]
                    else:
                        def find_key_with_value(d, target_value):
                            for k, v in d.items():
                                if isinstance(v, list):
                                    result = find_key_with_value(v[0], target_value)
                                    if result:
                                        return result
                                elif v == target_value:
                                    return k
                            return None
                        result = find_key_with_value(conf, item.name)
                        if result:
                            tree[result] = item.name
                        else:
                            tree[item.name] = default_rules(load_rules(item.name)) if '[' in item.name else ''
            return tree
        result = {}
        for path in paths:
            if path in last_conf:
                result[path] = [inner_build_tree(Path(path), last_conf[path][0]), last_conf[path][1]]
            else:
                result[path] = [inner_build_tree(Path(path), {}), True]
        return result

    def rename_tree(tree, direction=True, parent_key=''):
        for key, value in tree.items():
            path = Path(parent_key) / key if parent_key else Path(key)
            if isinstance(value, list):
                new_direction = direction and value[1]
                rename_tree(value[0], new_direction, path)
            else:
                if direction:
                    if value:
                        src = path
                        dest = Path(parent_key) / value
                    else:
                        src = None
                else:
                    src = Path(parent_key) / value
                    dest = path
                
                if src and src.exists() and src.is_file():
                    src.rename(dest)


    json_path = Path('./conf/directory_tree.json')
    if not json_path.exists():
        save_tree_to_json({})

    with json_path.open('r', encoding='utf-8') as f:
        conf = json.load(f)

    root = build_tree([data["path"]["input_path"]], conf)

    save_tree_to_json(root)

    rename_tree(root,direction)