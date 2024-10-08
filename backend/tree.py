from pathlib import Path
import json
from rename import load_rules, default_rules
from conf import data

def save_tree_to_json(tree):
    with open('backend/conf/directory_tree.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)

json_path = Path('backend/conf/directory_tree.json')
if not json_path.exists():
    save_tree_to_json({})

with json_path.open('r', encoding='utf-8') as f:
    conf = json.load(f)

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

root = build_tree([data["path"]["input_path"]], conf)
save_tree_to_json(root)


def rename_with_tree(tree, parent_key=''):
    for key, value in tree.items():
        path = Path(parent_key) / key if parent_key else Path(key)
        if isinstance(value, list):
            if value[1]:
                rename_with_tree(value[0], path)
        else:
            if Path(key).exists() and value:
                new_path = Path(parent_key) / value
                Path(path).rename(new_path)
                print(f"Renaming: {path} -> {new_path}")

rename_with_tree(root)
