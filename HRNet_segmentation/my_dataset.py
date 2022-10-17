import os
from PIL import Image
import numpy as np
from torch.utils.data import Dataset
import pandas as pd


class DriveDataset(Dataset):
    def __init__(self, root: str, train: bool, transforms=None):
        super(DriveDataset, self).__init__()
        self.transforms = transforms
        if train:
            # self.flag = "training"
            data = pd.read_csv('/home/user1/datasets/spacenet7/SN7_buildings_train/csvs/sn7_baseline_train_df.csv')
            self.img_list = data['image'].tolist()
            self.manual = data['label'].tolist()
        else:
            # self.flag = "test"
            data = pd.read_csv('/home/user1/datasets/spacenet7/SN7_buildings_train/csvs/sn7_baseline_test_df.csv')
            self.img_list = data['image'].tolist()
            self.manual = data['label'].tolist()


    def __getitem__(self, idx):
        img = Image.open(self.img_list[idx]).convert('RGB')
        # w = img.size[0]
        # h = img.size[1]
        # w1 = 584
        # h1 = 584
        # new_img = Image.new('RGB',(w1,h1),(0,0,0))
        # new_img.paste(img,(0,0))
        # img = new_img

        manual = Image.open(self.manual[idx]).convert('L')
        mask = np.array(manual) / 255


        # manual = Image.open(self.manual[idx]).convert('L')
        # manual = np.array(manual) / 255
        # mask = np.pad(manual, ((0, 72), (0, 72)), 'constant', constant_values=255)
        # # 这里转回PIL的原因是，transforms中是对PIL数据进行处理
        mask = Image.fromarray(mask)
        if self.transforms is not None:
            img, mask = self.transforms(img, mask)

        return img, mask
    def __len__(self):
        return len(self.img_list)

    @staticmethod
    def collate_fn(batch):
        images, targets = list(zip(*batch))
        batched_imgs = cat_list(images, fill_value=0)
        batched_targets = cat_list(targets, fill_value=255)
        return batched_imgs, batched_targets


def cat_list(images, fill_value=0):
    max_size = tuple(max(s) for s in zip(*[img.shape for img in images]))
    batch_shape = (len(images),) + max_size
    batched_imgs = images[0].new(*batch_shape).fill_(fill_value)
    for img, pad_img in zip(images, batched_imgs):
        pad_img[..., :img.shape[-2], :img.shape[-1]].copy_(img)
    return batched_imgs

