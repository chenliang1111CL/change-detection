import os
from PIL import Image

data_root = r'/home/user1/datasets/DRIVE'
data_root2 = r'/home/user1/datasets/DRIVE2'
for i in os.listdir(data_root):
    for x in os.listdir(os.path.join(data_root, i)):
        for y in os.listdir(os.path.join(data_root, i, x)):
            img = Image.open(os.path.join(data_root, i, x ,y))
            w = img.size[0]
            h = img.size[1]
            w1 = img.size[0]
            h1 = img.size[1]
            if ((w % 2 != 0) or (h % 2 != 0)):
                if (w % 2 != 0):
                    w = w + 1
                if (h % 2 != 0):
                    h = h + 1
                new_img = Image.new('RGB', (w, h), (0, 0, 0))
                img = new_img.paste(img, (0, 0, w1, h1))
                img = Image.fromarray(img)
                new_img2 = Image.new('L', (w, h), (0))
                mask = new_img2.paste(mask, (0, 0, w1, h1))
                mask = Image.fromarray(mask)