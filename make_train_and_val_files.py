import os
import glob
from os import getcwd


#用于形如VOC数据集的文件架构
#根据已划分的测试集,验证集,训练集的txt文件,将不同类型的图片
#从总图片文件夹里筛选出保存到对应train,val,test文件夹
#本文件与图片总文件夹属于同级目录

wd = getcwd()
print(wd)

imagePath = os.path.join(wd, 'images')


os.chdir(imagePath)
gt_files = glob.glob('*.jpg')
test_image_ids = open(os.path.join(wd, 'Main/test.txt')).read().strip().split()
val_image_ids = open(os.path.join(wd, 'Main/val.txt')).read().strip().split()

trainpath = 'train'
valpath = 'val'
testpath ='test'

for file in gt_files:
    if file.split('.')[0] in test_image_ids:
        if not os.path.exists(testpath):
            os.makedirs(testpath)
        #保存到对用文件夹
        os.rename(file, testpath + '/' + file)
    elif file.split('.')[0] in val_image_ids:
        if not os.path.exists(valpath):
            os.makedirs(valpath)
        os.rename(file, valpath + '/' + file)
    else:
        if not os.path.exists(trainpath):
            print("**")
            os.makedirs(trainpath)
        os.rename(file, trainpath + '/' + file)

print('done.')