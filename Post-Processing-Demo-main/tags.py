import cv2
import os
import math
import csv

def extract_target_area_centercoor(cv2image):  # 提取离散目标中心坐标
    gray_img = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
    th, binary = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    coor = []
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        coor.append([cx, cy])
    return coor


def merge_images(imagelist):  # 拼合多个图像递归算法
    if len(imagelist) == 2:
        img1 = cv2.imread(imagelist.pop())
        img2 = cv2.imread(imagelist.pop())
        imgadd = cv2.add(img1, img2)
        return imgadd
    elif len(imagelist) == 0:
        return
    else:
        img = cv2.imread(imagelist.pop())
        imgadd = cv2.add(img, merge_images(imagelist))
        return imgadd


def merge(dir):  # 拼合图像
    dirs = os.listdir(dir)
    for i in range(len(dirs)):
        dirs[i] = os.path.join(dir, dirs[i])
    merge = merge_images(dirs)
    return merge


def coor_distance(coor1, coor2):  # 坐标距离
    distance = math.sqrt((coor1[0] - coor2[0]) ** 2 + (coor1[1] - coor2[1]) ** 2)
    return distance


def main(dir="image", distance=5, repeat=3):
    img = merge(dir)
    coors = extract_target_area_centercoor(img)
    imgist = os.listdir(dir)
    for i in range(len(imgist)):
        imgist[i] = os.path.join(dir, imgist[i])

    get_coors=[]
    template = open("./template/template.csv","w",newline='')#创建记录坐标及序号的csv模板
    writer = csv.writer(template)
    writer.writerow([ "pixel_x", "pixel_y","index"])
    for index,coor in enumerate(coors):
        repeat_count = 0
        for i in imgist:
            img_or = extract_target_area_centercoor(cv2.imread(i))
            for j in img_or:
                if coor_distance(coor, j) < distance:  # 目标中心距离限制  超出距离判定非同一目标
                    repeat_count += 1
        if repeat_count >= repeat:  # 置信度：重复次数下限  用于筛选可信
            get_coors.append(coor)
            writer.writerow([coor[0],coor[1],index])#将【x、y、序号】写入csv
    template.close()


    # for i in get_coors:
    #     print(i)
    #     [x,y] = i
    #     cv2.circle(img, (x, y), 4, (0, 0, 255), 4)
    cv2.imshow("test", img)
    cv2.waitKey(0)
