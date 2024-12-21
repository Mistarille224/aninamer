import re

def apply_default_rules(name):
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

print(apply_default_rules("[Tsukigakirei][Ao no Hako 3][1-4][WEBrip][1080][CHS&JPN]"))