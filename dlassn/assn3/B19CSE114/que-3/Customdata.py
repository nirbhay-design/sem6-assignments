from PIL import Image
import torch
import torchvision
import numpy as np
import os
from config import config


class MapData(object):
    def __init__(self,root_dir):
        self.root_dir = root_dir
        self.images = os.listdir(root_dir)
        self.transformations = torchvision.transforms.Compose([
            torchvision.transforms.Resize((config.image_size,config.image_size)),
            torchvision.transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.images)

    def __getitem__(self,idx):
        image_name = self.images[idx]
        image_path = os.path.join(self.root_dir,image_name)
        img = Image.open(image_path).convert('RGB')
        np_img = np.array(img.getdata()).reshape(img.size[1],img.size[0],3)
        input_ig = Image.fromarray(np.uint8(np_img[:,:600,:]))
        output_ig = Image.fromarray(np.uint8(np_img[:,600:,:]))
        input_img = self.transformations(input_ig)
        output_img = self.transformations(output_ig)
        return (input_img,output_img)


def get_dataloader():
    train_map_data = MapData(config.train_path)
    test_map_data = MapData(config.val_path)

    train_loader = torch.utils.data.DataLoader(
        train_map_data,
        batch_size=config.batch_size,
        shuffle=True,
        pin_memory = config.pin_memory,
        num_workers=config.num_workers
    )

    val_loader = torch.utils.data.DataLoader(
        test_map_data,
        batch_size=config.batch_size,
        shuffle=True,
        pin_memory=config.pin_memory,
        num_workers=config.num_workers
    )

    return train_loader, val_loader


def load_img(img_path):
    img = Image.open(img_path).convert('RGB')    # return image as width,height
    np_img = np.array(img.getdata()).reshape(img.size[1],img.size[0],3) # passing it here as height, width
    input_img = np_img[:,:600,:]
    output_img = np_img[:,600:,:]
    return input_img,output_img

# load_img('1005.jpg')
