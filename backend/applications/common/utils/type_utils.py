type_map = ["", "变化检测", "目标检测", "地物分类", "场景分类", "图像复原"]


def str_to_type(strs):
    if strs in type_map:
        return type_map.index(strs)
    return None


def type_to_str(num):
    if num < len(type_map):
        return type_map[num]
    return ""


def items_handle(items):
    for t in items:
        if 'type' in t:
            t['type'] = type_to_str(t['type'])
