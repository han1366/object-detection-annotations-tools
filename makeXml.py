import xml.etree.ElementTree as ET
import shutil
import os

original_path = "./VOC2007"
target_path = "./VOC2007"
target_classes = ["person"]  # 需要的类别


# 寻找包含"person", "bus", "car"三个类别的文件,并将xml、jpg复制到指定文件夹
def search_file(Annotations):
    print("step1: search file.")
    for file_name in os.listdir(os.path.join(original_path, "updateLabels")):
        old_ann_path = os.path.join(original_path, "updateLabels", file_name)
        #old_img_path = os.path.join(original_path, "JPEGImages", file_name.split('.')[0] + '.jpg')
        new_ann_path = os.path.join(target_path, Annotations, file_name)
        #new_img_path = os.path.join(target_path, "JPEGImages", file_name.split('.')[0] + '.jpg')

        print(old_ann_path)

        # 打开xml文件进行解析
        in_file = open(old_ann_path)
        tree = ET.parse(in_file)   # ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
        root = tree.getroot()  # 获取根节点

        for obj in root.findall('object'):  # 找到根节点下所有“object”节点
            name = str(obj.find('name').text)  # 找到object节点下name子节点的值，不考虑part下的name。
            if name in target_classes:
                # 将符合的文件（xml、jpg）复制到指定文件夹
                shutil.copyfile(old_ann_path, new_ann_path)
                #shutil.copyfile(old_img_path, new_img_path)
                break


# 找到文件中的"person", "bus", "car"，并删除其他类别和part标签。
def search_person_vehicle(Annotation):
    print("step2: filter classes.")
    for file_name in os.listdir(os.path.join(target_path, Annotation)):
        file_path = os.path.join(target_path, Annotation, file_name)
        print(file_path)
        in_file = open(file_path)
        tree = ET.parse(in_file)  # ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
        root = tree.getroot()  # 获取根节点

        for obj in root.findall('object'):  # 找到根节点下所有“object”节点
            name = str(obj.find('name').text)  # 找到object节点下name子节点的值，不考虑part下的name。
            # 判断:如果不是列出的，（这里可以用in对保留列表成员进行审查），则移除该object节点及其所有子节点。
            if not (name in target_classes):
                root.remove(obj)

            # 移除person目标上的其他标签（hand、foot等）
            for pa in obj.findall('part'):
                obj.remove(pa)

            # 将name为car、bus的节点，改为vehicle
            # if name in target_classes[1::]:
            #     name = obj.find('name')
            #     name.text = "vehicle"

        tree.write(file_path)


if __name__ == '__main__':
    Annotation = "person"
    search_file(Annotation)
    search_person_vehicle(Annotation)

