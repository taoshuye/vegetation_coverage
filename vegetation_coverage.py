# vegetation coverage of grassland
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import cv2
import numpy as np


def vegetation_coverage(photo):
    try:
        # 读入照片/read-in photo
        photo_ori = cv2.imread(photo)

        # 转换为浮点数进行计算/generated matrix
        photo_f = np.array(photo_ori, dtype=np.float32) / 255.0

        # 通道拆分/The channel separation
        (b, g, r) = cv2.split(photo_f)
        photo_g = 2 * g - b - r

        # 求矩阵最大值和最小值/Get the maximum and minimum
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(photo_g)

        # 转换为u8类型，进行otsu二值化/Convert to u8 type and binaryzation
        photo_g_u8 = np.array((photo_g - minVal) / (maxVal - minVal)
                              * 255, dtype=np.uint8)

        (thresh, photo_otus) = cv2.threshold(
            photo_g_u8, -1.0, 255, cv2.THRESH_OTSU)
        # cv2.imshow('photo_otus', photo_otus)
        # cv2.imwrite('photo_otus.jpg', photo_otus)
        # cv2.waitKey()

        # 得到彩色的图像
        # (b8, g8, r8) = cv2.split(photo_ori)
        # photo_color = cv2.merge(
        #     [b8 & photo_otus, g8 & photo_otus, r8 & photo_otus])
        # cv2.imshow('photo_color', photo_color)
        # cv2.imwrite('photo_color.jpg', photo_color)
        # cv2.waitKey()

        # 轮廓识别/findContours
        a, b, c = cv2.findContours(
            photo_otus, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # photo_drawContours = cv2.drawContours(
        #     photo_ori, b, -1, (0, 0, 255), 1)
        # cv2.imshow("img", photo_drawContours)

        # cv2.waitKey()
        # cv2.imshow('photo_drawContours', photo_drawContours)
        # cv2.waitKey()
        # cv2.imwrite('photo_drawContours.jpg', photo_drawContours)

        # 遍历所有轮廓并计算总面积/range all the contours and calculate the total area
        area = 0
        for i in range(0, len(b)):
            cnt = b[i]
            area += cv2.contourArea(cnt)

        # print("该图片共包含：", len(b), "个面积计算区域")
        # print("面积/area：", area)area
        a1 = photo_ori.shape
        print("图片尺寸/photo size:", a1[0], "*", a1[1])
        vc = area / (a1[0] * a1[1]) * 100
        if vc >= 100:
            raise
        else:
            print("盖度/vegetation coverage：%.2f%%" % vc)
    except:
        print("请输入正确的图片地址和图片格式/Please enter the correct picture address and picture format:.jpg/.png/.tif/.bmp(24bit)")

vegetation_coverage("E:\\python\\opencv\\5.jpg")
