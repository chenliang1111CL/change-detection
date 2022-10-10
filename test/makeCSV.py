
root_dir = '/home/user1/datasets/spacenet7/'

import pandas as pd
import os

out_dir = os.path.join(root_dir, 'csvs/')
pops = ['train', 'test_public']
os.makedirs(out_dir, exist_ok=True)

for pop in pops:
    d = os.path.join(root_dir, pop)
    outpath = os.path.join(out_dir, 'sn7_baseline_' + pop + '_df.csv')
    im_list, mask_list = [], []
    subdirs = sorted([f for f in os.listdir(d) if os.path.isdir(os.path.join(d, f))])
    for subdir in subdirs:

        if pop == 'train':
            im_files = [os.path.join(d, subdir, 'images_masked', f)
                        for f in sorted(os.listdir(os.path.join(d, subdir, 'images_masked')))
                        if f.endswith('.tif') and os.path.exists(
                    os.path.join(d, subdir, 'masks', f.split('.')[0] + '_Buildings.tif'))]
            mask_files = [os.path.join(d, subdir, 'masks', f.split('.')[0] + '_Buildings.tif')
                          for f in sorted(os.listdir(os.path.join(d, subdir, 'images_masked')))
                          if f.endswith('.tif') and os.path.exists(
                    os.path.join(d, subdir, 'masks', f.split('.')[0] + '_Buildings.tif'))]
            im_list.extend(im_files)
            mask_list.extend(mask_files)

        elif pop == 'test_public':
            im_files = [os.path.join(d, subdir, 'images_masked', f)
                        for f in sorted(os.listdir(os.path.join(d, subdir, 'images_masked')))
                        if f.endswith('.tif')]
            im_list.extend(im_files)

    # save to dataframes
    # print("im_list:", im_list)
    # print("mask_list:", mask_list)
    if pop == 'train':
        df = pd.DataFrame({'image': im_list, 'label':mask_list})
        # display(df.head())
    elif pop == 'test_public':
        df = pd.DataFrame({'image': im_list})
    df.to_csv(outpath, index=False)
    print(pop, "len df:", len(df))
    print("output csv:", outpath)