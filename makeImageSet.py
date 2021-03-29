import sys
import os
import glob

# make sure that the cwd() in the beginning is the location of the python script (so that every path makes sense)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
print(parent_path)
GT_PATH = os.path.join(parent_path, 'data/thirdVideo', '2021_0312_pic')
#'data/secondVideo' is image parent path
#'first' is image file name
#these strings need modify

os.chdir(GT_PATH)
gt_files = glob.glob('*.jpg')
num = len(gt_files)
if num == 0:
    print("Error: no .jpg files found in", GT_PATH)
    sys.exit()

personNum = 8  #标注人员数量
i=0
backup_folder = 0
for i in range(1,personNum+1):
    if not os.path.exists(str(i)):
        os.makedirs(str(i))
for i,file in enumerate(gt_files):
    backup_folder = int(i%8)+1
    os.rename(file, str(backup_folder) + '/' + file)
print('over')