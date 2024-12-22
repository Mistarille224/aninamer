from pathlib import Path

def rename(direction, database, parent_key=''):
    for key, value in database.items():
        path = Path(parent_key) / key if parent_key else Path(key)
        if isinstance(value[1], dict):
            new_direction = direction and value[0]
            rename(new_direction, value[1], path)
        else:
            if direction and value[0]:
                if value[2]:
                    src = Path(parent_key) / value[1]
                    dest = Path(parent_key) / value[2]
                else:
                    src = None
            else:
                src = Path(parent_key) / value[2]
                dest = Path(parent_key) / value[1]
            
            if src and src.exists() and src.is_file():
                src.rename(dest)
