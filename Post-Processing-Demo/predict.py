import tags
import cv2

import numpy as np

#tags.main("image",5,2)
img2bpredicted=r"./test/predict.png"
img = cv2.imread(img2bpredicted)

coors = tags.extract_target_area_centercoor(img)
coortemp = np.loadtxt(open("./template/template.csv","rb"),delimiter=",",skiprows=1,usecols=[0,1,2])

flag = 0#是否重复标志
for i in coors:
    for j in coortemp:
        if tags.coor_distance(i,j)<5:
            flag=1#如果检测到一个相近点，则表示重复
    if flag==0:
        [x, y] = i
        cv2.circle(img, (x, y), 4, (0, 0, 255), 4)
    else:
        flag=0

cv2.imshow("test", img)
cv2.waitKey(0)
