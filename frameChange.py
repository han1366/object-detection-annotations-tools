# 导入必要的软件包
import cv2

# 视频文件输入初始化
filename = "./data/thirdVideo/ch01_20210303090052.mp4"
camera = cv2.VideoCapture(filename)

# 视频文件输出参数设置
out_fps = 6.0  # 输出文件的帧率
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out1 = cv2.VideoWriter('./data/video/0319_5839.mp4', fourcc, out_fps, (1920, 1080))

# 初始化当前帧的前帧
lastFrame = None
i = 0

# 遍历视频的每一帧
while camera.isOpened():
    # 读取下一帧
    (ret, frame) = camera.read()
    i += 1

    if i%60 == 0 :
        i = 0
        # 如果不能抓取到一帧，说明我们到了视频的结尾
        if not ret:
            break

            # 调整该帧的大小
        #frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_CUBIC)

        # 如果第一帧是None，对其进行初始化
        if lastFrame is None:
            lastFrame = frame
            continue

            # 计算当前帧和前帧的不同
        frameDelta = cv2.absdiff(lastFrame, frame)

        # 当前帧设置为下一帧的前帧
        lastFrame = frame.copy()

        # 结果转为灰度图
        thresh = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)

        # 图像二值化
        thresh = cv2.threshold(thresh, 50, 255, cv2.THRESH_BINARY)[1]

        ''' 
        #去除图像噪声,先腐蚀再膨胀(形态学开运算) 
        thresh=cv2.erode(thresh,None,iterations=1) 
        thresh = cv2.dilate(thresh, None, iterations=2) 
        '''

        # 阀值图像上的轮廓位置
        cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        number = [cnt for cnt in cnts if cv2.contourArea(cnt) > 5000]
        print(len(number))

        # 遍历轮廓
        for c in cnts:
            # 忽略小轮廓，排除误差
            if cv2.contourArea(c) < 5000:
                continue

                # 计算轮廓的边界框，在当前帧中画出该框
            (x, y, w, h) = cv2.boundingRect(c)
            if w > 2*h or h > 2*w :
                continue
            print(cv2.contourArea(c))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 显示当前帧frameDelta
        cv2.imshow("frame", frame)
        #cv2.imshow("frameDelta", frameDelta)
        #cv2.imshow("thresh", thresh)

        # 保存视频
        out1.write(frame)

        # 如果q键被按下，跳出循环
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break

        # 清理资源并关闭打开的窗口
out1.release()
camera.release()
cv2.destroyAllWindows()