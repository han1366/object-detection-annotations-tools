import cv2
import os

def video2image(num,getvideo,tofiles):

    isExists=os.path.exists(tofiles)
    if not isExists:
        os.makedirs(tofiles)


    print('开始运行:',end=' ')
    vc = cv2.VideoCapture(getvideo)
    c = 1

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    timeF = 150 #timeF帧保留一张图片

    while rval:
        rval,frame = vc.read()
        try:
            if(c%timeF == 0):
                cv2.imwrite(tofiles+'0325'+str(num)+'-'+str(c)+'.jpg',frame)
                print(c//timeF)
            c=c+1
        except:
            break
        #cv2.waitKey(1)
    vc.release()
    print('\n 运行结束!')


 


if __name__=='__main__':
    tofiles = './data/0325_pic/'
    file_dir = './data/forthVideo/'
    for root, dirs, files in os.walk(file_dir):
        for i, file in enumerate(files):
            path = root + '/' +file
            print(path)  # 当前路径下所有非目录子文件
            video2image(i,path, tofiles)
