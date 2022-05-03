from config import config
import os
import torchvision
from PIL import Image
import torch

class CustomDataset:
    def __init__(self,normal_path,abnormal_path):
        self.normal_path = normal_path
        self.abnormal_path = abnormal_path
        self.normal = os.listdir(normal_path)
        self.abnormal = os.listdir(abnormal_path)
        
        self.images = list(zip(self.normal,[0]*len(self.normal))) + list(zip(self.abnormal,[1]*len(self.abnormal)))
        
        self.transformations = torchvision.transforms.Compose([
                                torchvision.transforms.Resize((config['IMAGE_SIZE'],config['IMAGE_SIZE'])),
                                torchvision.transforms.ToTensor()])
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self,idx):
        image,clas = self.images[idx]
        img_path = os.path.join(self.normal_path,image)
        if clas == 1:
            img_path = os.path.join(self.abnormal_path,image)
        img = Image.open(img_path).convert('RGB')
        img = self.transformations(img)
        return (img,clas)
    
def return_dataloader():
    data = CustomDataset(config['normal_data'],config['abnormal_data'])
    len_data = len(data)
    val_split = int(config['val_split'] * len_data)
    test_split = int(config['test_split'] * len_data)
    train_split = len_data - (val_split + test_split)
    train_data, test_data, val_data = torch.utils.data.dataset.random_split(data,[train_split,test_split,val_split])
    if (config['optimized']):
        print("loading optimized data")
        train_loader = torch.utils.data.DataLoader(train_data,shuffle=True,batch_size=config['BATCH_SIZE'],pin_memory=config['pin_memory'],num_workers=config['num_workers'])
        val_loader = torch.utils.data.DataLoader(val_data,shuffle=True,batch_size=config['BATCH_SIZE'],pin_memory=config['pin_memory'],num_workers=config['num_workers'])
        test_loader = torch.utils.data.DataLoader(test_data,shuffle=True,batch_size=config['BATCH_SIZE'],pin_memory=config['pin_memory'],num_workers=config['num_workers'])
    else:
        print('loading data normally')
        train_loader = torch.utils.data.DataLoader(train_data,shuffle=True,batch_size=config['BATCH_SIZE'])
        val_loader = torch.utils.data.DataLoader(val_data,shuffle=True,batch_size=config['BATCH_SIZE'])
        test_loader = torch.utils.data.DataLoader(test_data,shuffle=True,batch_size=config['BATCH_SIZE'])

    return train_loader, test_loader , val_loader


    
# mydata = CustomDataset(normal_path=config['normal_data'],
#                       abnormal_path=config['abnormal_data'])