import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys

sets=[('2007', 'train'), ('2007', 'val')]

classes = ["person", "cloth", "noCloth"]

# soft link your VOC2018 under here
root_dir = './'


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open(os.path.join(root_dir, 'VOC%s/newClothAnnotations/%s.xml'%(year, image_id)))
    out_file = open(os.path.join(root_dir, 'VOC%s/labels/%s.txt'%(year, image_id)), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    labels_target = os.path.join(root_dir, 'VOC%s/labels/'%(year))
    print('labels dir to save: {}'.format(labels_target))
    if not os.path.exists(labels_target):
        os.makedirs(labels_target)
    image_ids = open(os.path.join(root_dir, 'VOC{}/ImageSets/Main/{}.txt'.format(year, image_set))).read().strip().split()
    list_file = open(os.path.join(root_dir, '%s_%s.txt'%(year, image_set)), 'w')
    for image_id in image_ids:
        img_f = os.path.join(root_dir, 'VOC%s/JPEGImages/%s.jpg\n'%(year, image_id))
        list_file.write(os.path.abspath(img_f))
        convert_annotation(year, image_id)
    list_file.close()

print('done.')