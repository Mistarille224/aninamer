import os
import json

def build_tree(paths):
    def inner_build_tree(current_path):
        tree = {}
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                tree[item] = [inner_build_tree(item_path), False]
            else:
                tree[item] = ""
        return tree
    result = {}
    for path in paths:
        result[path] = inner_build_tree(path)
    return result

def save_tree_to_json(tree, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)

def load_tree_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    
root_path = ["D:\\download\\Video\\anime","D:\\download\\Videohlink\\anime"]
root = build_tree(root_path)
save_tree_to_json(root, "backend\conf\directory_tree.json")

loaded_root = load_tree_from_json("backend\conf\directory_tree.json")


# def restore_paths(tree, base_path=''):
#     paths = []
#     for key, value in tree.items():
#         current_path = os.path.join(base_path, key)
#         if isinstance(value, dict):
#             paths.extend(restore_paths(value, current_path))
#         else:
#             paths.append(current_path)
#     return paths


# restored_paths = restore_paths(loaded_root)
# print(restored_paths)