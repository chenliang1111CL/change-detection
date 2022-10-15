from osgeo import gdal,ogr,osr
import os
from PIL import Image
def caijian(image_one,path,image_file):
    img = Image.open(image_one)
    f=image_file.split('.')
    w,h = img.size
    num = 1
    for r in range((h//256)-1):
        for c in range((w//256)-1):
            box = (c*256,r*256,c*256+512,r*256+512)
            file = os.path.join(path,f[0]+'_'+str(num)+'.tif')
            num = num+1
            rol = img.crop(box)
            rol.save(file)

root = r'D:\spacenet\train'
aois = [os.path.join(root, x) for x in os.listdir(root)]

for aoi in aois:
    if not os.path.isdir(os.path.join(root, aoi)):
        continue
    print(aoi)

    images_masked = os.path.join(aoi, "images_masked")
    img_files = [x for x in os.listdir(images_masked)]
    images_masked_3x = os.path.join(aoi, "images_masked_3x")
    out_path =  os.path.join(aoi, "images_masked_3x_divide")
    if not os.path.exists(images_masked_3x):
        os.makedirs(images_masked_3x)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    type = 'tif'
    for img_file in img_files:
        fppath = os.path.join(images_masked,img_file)
        fp2 = os.path.join(images_masked_3x,img_file)
        img = Image.open(fppath)
        img2 = img.resize((3072, 3072), Image.ANTIALIAS)
        img2.save(fp2)
        for image_file in os.listdir(images_masked_3x):
            image_one = os.path.join(images_masked_3x,image_file)
            caijian(image_one,out_path,image_file)
