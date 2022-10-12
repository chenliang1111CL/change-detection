
root_dir = '/home/user1/datasets/spacenet7/wdata'

import pandas as pd
import os

out_dir = os.path.join(root_dir, 'csvs/')
pops = ['train', 'test']
os.makedirs(out_dir, exist_ok=True)

for pop in pops:
    d = os.path.join(root_dir, pop)
    outpath = os.path.join(out_dir, 'sn7_baseline_' + pop + '_df.csv')
    im_list, mask_list = [], []
    subdirs = sorted([f for f in os.listdir(d) if os.path.isdir(os.path.join(d, f))])
    for subdir in subdirs:

        masks = os.listdir(os.path.join(d, subdir, 'masks_3x_divide'))
        for f in masks:
            if f.endswith('.tif'):
                b = os.path.join(d, subdir, 'images_masked_3x_divide', f.replace('_Buildings', ''))
                if os.path.exists(b):
                    mask_list.append(os.path.join(d, subdir, 'masks_3x_divide', f))
                    im_list.append(b)


    # save to dataframes
    # print("im_list:", im_list)
    # print("mask_list:", mask_list)
    df = pd.DataFrame({'image': im_list, 'label':mask_list})

    df.to_csv(outpath, index=False)
    print(pop, "len df:", len(df))
    print("output csv:", outpath)