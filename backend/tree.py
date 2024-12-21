import json
import os
import re
from pathlib import Path
from conf import config

TREE_PATH = Path(__file__).parent / 'conf' / 'directory_tree.json'

def read_tree_from_json():
    with TREE_PATH.open('r', encoding='utf-8') as f:
        return json.load(f)

def save_tree_to_json(tree):
    with TREE_PATH.open('w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)
        os.fsync(f.fileno())

def apply_rules(name):
    if name[name.find("]") + 1] == "[":
        name = name[:name.find("]") + 1] + name[name.find("]") + 2:]
    name = re.sub(r'\[(\d+)\]', r' E\1 ', name)
    name = re.sub(r' (\d+) ', r' E\1 ', name)
    name = re.sub(r'(\d+)-(\d+)', r' E\1-E\2 ', name)
    name = name.replace(' - ', ' ').replace('(v2)', ' - v2 ')
    name = re.sub(r'\[(\d+)v2\]', r' E\1 - v2 ', name)
    name = re.sub(r'\[ E(\d+)', r' E\1', name)
    name = re.sub(r'\[[^]]*\]', '', name).replace(']', '')
    if len(re.findall(r' E(\d+)', name)) > 1:
        if '1080' in re.findall(r' E(\d+)', name):
            name =  name.replace('E1080', '')
        if '720' in re.findall(r' E(\d+)', name):
            name =  name.replace('E720', '')
        for match in re.findall(r' E(\d+)', name)[:-1]:
            name = re.sub(r'E'+match,match,name,count=1)
    name = re.sub(r'\s+', ' ', name).replace(' .', '.').strip()
    return name

def build_tree(last_conf):
    def inner_build_tree(current_path, last_conf):
        tree = {}
        for item in current_path.iterdir():
            if item.is_dir():
                sub_tree = inner_build_tree(item, last_conf.get(item.name, [True, {}])[1])
                tree[item.name] = [last_conf.get(item.name, [True])[0], sub_tree]
            else:
                identifier = f'{item.stat().st_size}/{os.path.getctime(item.resolve())}'
                if identifier in last_conf:
                    original_name = last_conf[identifier][2]
                    formatted_name = apply_rules(last_conf[identifier][1])
                    if item.name != original_name and formatted_name != original_name:
                        item.rename(item.parent / formatted_name)
                    tree[identifier] = [last_conf[identifier][0], last_conf[identifier][1], formatted_name]
                else:
                    formatted_name = apply_rules(item.name)
                    tree[identifier] = [True, item.name, formatted_name]
        return tree

    tree_result = {}
    for path in config['paths']:
        if path:
            path_conf = last_conf.get(path, [True, {}])
            tree_result[path] = [path_conf[0], inner_build_tree(Path(path), path_conf[1])]
    return tree_result

def tree():
    if TREE_PATH.exists():
        last_tree = read_tree_from_json()
    else:
        last_tree = {}
    new_tree = build_tree(last_tree)
    save_tree_to_json(new_tree)

def extract_deleted_items(a, b):
    result = {}
    for key in b:
        if key not in a:
            result[key] = b[key]
        elif isinstance(b[key][1], dict):
            nested_result = extract_deleted_items(a[key][1], b[key][1])
            if nested_result:
                result[key][1] = nested_result
    return result

def restore_deleted_items(a, deleted_items):
    restored = a.copy()
    
    def restore_recursive(a, deleted_items):
        for key, value in deleted_items.items():
            if isinstance(value[1], dict):
                if key not in a:
                    a[key][1] = {}
                restore_recursive(a[key][1], value)
            else:
                a[key] = value

    restore_recursive(restored, deleted_items)
    return restored

