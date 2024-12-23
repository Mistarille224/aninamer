import json
import os
from pathlib import Path
import re
from datetime import datetime,timedelta
from conf import config

TREE_PATH = Path('./conf/directory_tree.json')
DELETED_TREE_PATH = Path('./conf/deleted_tree.json')

def read_tree(path=TREE_PATH):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def save_tree(tree, path):
    if tree:
        with path.open('w', encoding='utf-8') as f:
            json.dump(tree, f, ensure_ascii=False, indent=4)
            os.fsync(f.fileno())

def apply_rules(name):
    if name[name.find("]") + 1] == "[":
        name = name[:name.find("]") + 1] + name[name.find("]") + 2:]
    name = re.sub(r'\[(\d+)\]', r' E\1 ', name)
    name = re.sub(r' (\d+) ', r' E\1 ', name)
    name = re.sub(r'(\d+)-(\d+)', r' E\1-E\2 ', name)
    name = name.replace(' - ', ' ').replace('[v2]', ' - v2 ')
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

def extract_items(new, last):
    deleted_items = {}
    for key in last:
        if key not in new:
            deleted_items[key] = last[key]
        elif isinstance(last[key][1], dict):
            nested_result = extract_items(new[key][1], last[key][1])
            if nested_result:
                deleted_items[key] = [None,nested_result]
    return deleted_items

def combine_items(last, deleted_items):
    for key in deleted_items:
        if key in last:
            combine_items(last[key][1],deleted_items[key][1])
        else:
            last[key] = deleted_items[key]
    return last

def tree():
    last_tree = {}
    last_deleted_tree = {}

    if TREE_PATH.exists():
        last_tree = read_tree(TREE_PATH)
        if DELETED_TREE_PATH.exists():
            last_deleted_tree = read_tree(DELETED_TREE_PATH)
            last_tree = combine_items(last_tree, last_deleted_tree)
    new_tree = build_tree(last_tree)

    new_deleted_tree = extract_items(new_tree, last_tree)
    added_part = extract_items(last_deleted_tree, new_deleted_tree)
    deleted_part = extract_items(new_deleted_tree, last_deleted_tree)
    modified_part = combine_items(added_part, deleted_part)
    for key in new_deleted_tree:
        if key in modified_part:
            if len(new_deleted_tree[key]) == 3:
                new_deleted_tree[key][2] = datetime.now().isoformat()
            else:
                new_deleted_tree[key].append(datetime.now().isoformat())
        new_deleted_tree[key][2] = last_deleted_tree[key][2]
        if key in new_tree:
            if datetime.now() - datetime.fromisoformat(new_deleted_tree[key][2]) >= timedelta(days=7):
                del new_deleted_tree[key]
        else:
            if datetime.now() - datetime.fromisoformat(new_deleted_tree[key][2]) >= timedelta(days=30):
                del new_deleted_tree[key]
    save_tree(new_deleted_tree, DELETED_TREE_PATH)

    save_tree(new_tree, TREE_PATH)
