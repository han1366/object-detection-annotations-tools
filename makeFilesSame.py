import sys
import os
import glob

# make sure that the cwd() in the beginning is the location of the python script (so that every path makes sense)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
parent_path = os.path.abspath(os.path.join(parent_path, os.pardir))
GT_PATH = os.path.join(parent_path, 'VOCdevkit/VOC2007', 'person')
DR_PATH = os.path.join(parent_path, 'VOCdevkit/VOC2007', 'Annotations')

backup_folder = 'backup_no_matches_found'  # must end without slash

os.chdir(GT_PATH)
gt_files = glob.glob('*.xml')
if len(gt_files) == 0:
    print("Error: no .xml files found in", GT_PATH)
    sys.exit()
os.chdir(DR_PATH)
dr_files = glob.glob('*.xml')
if len(dr_files) == 0:
    print("Error: no .xml files found in", DR_PATH)
    sys.exit()

gt_files = set(gt_files)
dr_files = set(dr_files)
print('total ground-truth files:', len(gt_files))
print('total detection-results files:', len(dr_files))
print()

gt_backup = gt_files - dr_files
dr_backup = dr_files - gt_files


def backup(src_folder, backup_files, backup_folder):
    # non-intersection files (txt format) will be moved to a backup folder
    if not backup_files:
        print('No backup required for', src_folder)
        return
    os.chdir(src_folder)
    ## create the backup dir if it doesn't exist already
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    for file in backup_files:
        os.rename(file, backup_folder + '/' + file)


backup(GT_PATH, gt_backup, backup_folder)
backup(DR_PATH, dr_backup, backup_folder)
if gt_backup:
    print('total ground-truth backup files:', len(gt_backup))
if dr_backup:
    print('total detection-results backup files:', len(dr_backup))

intersection = gt_files & dr_files
print('total intersected files:', len(intersection))
print("Intersection completed!")
