from xml.etree.ElementTree import ElementTree, Element, parse
import xml.etree.ElementTree as ET
import os
import shutil

hole_path = './newMaskAnnotations'
arm_path = './person'
out_path = './Fusing'
print(os.listdir(hole_path))
# 格式化
def __indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


for hole_xml in os.listdir(hole_path):
    # 将同名xml合并
    if os.path.exists(os.path.join(arm_path,hole_xml)):
        print('fusing',hole_xml)
        tree_hole = parse(os.path.join(hole_path,hole_xml))
        root_hole = tree_hole.getroot()  # annotation

        new_hole = tree_hole

        tree_arm = parse(os.path.join(arm_path,hole_xml))
        root_arm = tree_arm.getroot()  # annotation
        object = (tree_arm.findall('object'))
        for i in range(len(object)):
            root_hole.append(object[i])
        __indent(root_hole)
        new_hole.write(os.path.join(out_path,hole_xml))
    # 不同名xml复制
    else:
        print('copying',hole_xml)
        shutil.copy(os.path.join(hole_path,hole_xml), out_path)


# 将不同名xml复制
for arm_xml in os.listdir(arm_path):
    if not os.path.exists(os.path.join(out_path,arm_xml)):
        print('copying')
        shutil.copy(os.path.join(arm_path, arm_xml), out_path)