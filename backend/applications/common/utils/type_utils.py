type_map = dict()
type_map["变化检测"] = 1
type_map["目标检测"] = 2
type_map["地物分类"] = 3
type_map["场景分类"] = 4

type_map_1 = dict()
type_map_1[1] = "变化检测"
type_map_1[2] = "目标检测"
type_map_1[3] = "地物分类"
type_map_1[4] = "场景分类"

def str_to_type(strs):
    if strs in type_map:
        return type_map[strs]
    return None


def type_to_str(num):
    if num in type_map_1:
        return type_map_1[num]
    return ""


def items_handle(items):
    for t in items:
        if 'type' in t:
            type_ = t['type']
            t['type'] = type_to_str(type_)
