import os
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import time
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class configs(object):
    batch_size = 32
    lr = 2e-4
    data_directory = './'
    seed = 42
    pin_memory = True
    n_workers = 2
    epochs = 15
    base_dir_value = './'
    save_loss_path='./gendisc.svg'
    image_size = 64
    gpu_id="7"
    device = torch.device(f'cuda:{gpu_id}' if torch.cuda.is_available() else "cpu")
    verbose = False
    z_dim = 200

config = configs()

transformations = transforms.Compose([
    transforms.Resize((config.image_size,config.image_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.5],[0.5])
])

class generator(nn.Module):
    def __init__(self,z_dim, channels_img, features_g):
        super(generator,self).__init__()    
        self.gen = nn.Sequential(
            self._block(z_dim,features_g*16,4,1,0),
            self._block(features_g*16,features_g*8,4,2,1),
            self._block(features_g*8, features_g*4,4,2,1),
            self._block(features_g*4, features_g*2,4,2,1),
            nn.ConvTranspose2d(features_g*2,channels_img,kernel_size=4,stride=2,padding=1),
            nn.Tanh()
        )

    def _block(self,in_channels,out_channels,kernel_size, stride, padding):
        return nn.Sequential(
            nn.ConvTranspose2d(
                in_channels,
                out_channels,
                kernel_size,
                stride,
                padding,
                bias=False,
            ),
            nn.BatchNorm2d(out_channels),
            nn.ReLU()
        )

    def forward(self,x):
        return self.gen(x)


class discriminator(nn.Module):
    def __init__(self,channel_img=1,features_d=None,resnet=False,other=False):
        super(discriminator,self).__init__()
        if resnet:
            print('using resnet')
            self.disc = torchvision.models.resnet18(pretrained=False)
            self.disc.conv1 = nn.Conv2d(channel_img, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
            self.disc.fc = nn.Linear(in_features=512,out_features=1)
        elif other:
            print('using official implementation')
            self.disc = nn.Sequential(
                nn.Conv2d(channel_img,features_d,kernel_size=4,stride=2,padding=1),
                nn.LeakyReLU(0.2),
                nn.Conv2d(features_d,features_d*2,4,2,1),
                nn.BatchNorm2d(features_d*2),
                nn.LeakyReLU(0.2),
                nn.Conv2d(features_d*2,features_d*4,4,2,1),
                nn.BatchNorm2d(features_d*4),
                nn.LeakyReLU(0.2),
                nn.Conv2d(features_d*4,features_d*8,4,2,1),
                nn.BatchNorm2d(features_d*8),
                nn.LeakyReLU(0.2),
                nn.Conv2d(features_d*8,1,kernel_size=4,stride=2,padding=0)
            )
        else:
            print('using vgg')
            self.disc = torchvision.models.vgg16(pretrained=False)
            self.disc.features[0] = nn.Sequential(
                nn.Conv2d(in_channels=channel_img,out_channels=64,kernel_size=(3,3),stride=1,padding = 1),
                nn.BatchNorm2d(64))
            feature_array = [2,5,7,10,12,14,17,19,21,24,26,28]
            for feat in feature_array:
                self.disc.features[feat] = nn.Sequential(
                    self.disc.features[feat],
                    nn.BatchNorm2d(self.disc.features[feat].out_channels)
                )
            self.disc.classifier[6] = nn.Linear(in_features=4096,out_features=1,bias=True)
            print(self.disc)
        
        self.sigmoid = nn.Sigmoid()
    def forward(self,x):
        # x.shape = (N, 1, 64, 64)
        return self.disc(x)

def init_wt(model):
    for m in model.modules():
        if isinstance(m, (nn.Conv2d,nn.ConvTranspose2d,nn.BatchNorm2d)):
            nn.init.normal_(m.weight.data,0,0.02)
    return model


def get_dataloader():
    global config, transformations

    train_data = torchvision.datasets.MNIST(
        root=config.data_directory,
        train=True,
        download=True,
        transform = transformations
        )

    test_data = torchvision.datasets.MNIST(
        root=config.data_directory,
        train=False,
        download=True,
        transform = transformations
        )

    train_loader = torch.utils.data.DataLoader(
        train_data,
        shuffle=True,
        batch_size=config.batch_size,
        pin_memory=config.pin_memory,
        num_workers=config.n_workers
        )

    test_loader = torch.utils.data.DataLoader(
        test_data,
        shuffle=True,
        batch_size=config.batch_size,
        pin_memory=config.pin_memory,
        num_workers=config.n_workers
    )

    return train_loader, test_loader

# def test_generator(gene,cur_epochs,epochs,test_size,save_dir):
#     fig,ax = plt.subplots(2,5,figsize=(5*5,4*2))
#     row = 0
#     col = 0
#     if (cur_epochs == 1 or cur_epochs == epochs//2 or cur_epochs == epochs):    
#         for i in range(10):
#             with torch.no_grad():
#                 random_noise = torch.randn(test_size)
#                 random_noise = random_noise.to(config.device)
#                 image = gene(random_noise)
#                 image = image.squeeze()
#                 image = image.detach().numpy()
#                 ax[row,col].imshow(image)
#                 if (col == 4):
#                     row = 1;
#                 col = (col + 1) % 5
#         plt.savefig(save_dir,format='svg')

def test_generator(gene,test_size,save_dir):
    array = []  
    for _ in range(10):
        with torch.no_grad():
            random_noise = torch.randn(test_size)
            random_noise = random_noise.to(config.device)
            image = gene(random_noise)
            image = image.squeeze().detach()
            image = image.to('cpu').numpy()
            array.append(image)
    stk1 = np.hstack(array[:5])
    stk2 = np.hstack(array[5:])
    final_stack = np.vstack([stk1,stk2])
    plt.figure(figsize=(10,8))
    plt.imshow(final_stack,cmap='gray')
    plt.savefig(save_dir,format='svg')
    plt.show()
    print('saved')



def train(gene, disc, train_data, lossfunction,ogen, odis,g_scaler,d_scaler, n_epochs):
    global config
    time1 = time.perf_counter()
    history = {'genloss':[],'discloss':[]}
    gene.train()
    disc.train()
    for epoch in range(n_epochs):
        running_genloss = 0;
        running_discloss = 0;
        len_train_data = len(train_data)
        for idx, (real_img,_) in enumerate(train_data):
            noise_size = (real_img.shape[0],config.z_dim,1,1)   
            random_noise = torch.randn(noise_size).to(config.device)
            real_img = real_img.to(config.device)
            
            # training disc 
            with torch.cuda.amp.autocast():
                real_disc = disc(real_img).reshape(-1)
                loss_disc_real = lossfunction(real_disc,torch.ones_like(real_disc))
                # print(f'ldr:{loss_disc_real.item():.3f}')
                
                fake_img = gene(random_noise) # (N,1,64,64)
                fake_disc = disc(fake_img.detach()).reshape(-1)
                loss_disc_fake = lossfunction(fake_disc,torch.zeros_like(fake_disc))
                # print(f'ldf:{loss_disc_fake.item():.3f}')

                loss_disc = (loss_disc_fake + loss_disc_real) / 2
                # print(f'ld:{loss_disc.item():.3f}')
                # odis.zero_grad()
            
            disc.zero_grad()
            d_scaler.scale(loss_disc).backward()
            d_scaler.step(odis)
            d_scaler.update()
            # disc.zero_grad()
            # loss_disc.backward()
            # odis.step()

            # training generator
            with torch.cuda.amp.autocast():
                output = disc(fake_img).reshape(-1)
                gen_loss = lossfunction(output,torch.ones_like(output))
            # print(f'gl:{gen_loss.item():.3f}')

            # print('-'*50)

            # ogen.zero_grad()
            ogen.zero_grad()
            g_scaler.scale(gen_loss).backward()
            g_scaler.step(ogen)
            g_scaler.update()

            history['genloss'].append(gen_loss.item())
            history['discloss'].append(loss_disc.item())

            running_genloss += (gen_loss.item()/len_train_data)
            running_discloss += (loss_disc.item()/len_train_data)

            if config.verbose:
                print(f'batches done {idx}',end='\r')
            
        test_generator(gene,(1,config.z_dim,1,1),f'{epoch+1}_epoch.svg')
        print(f'epoch: [{epoch+1}/{n_epochs}], gene_loss: {running_genloss:.2f}, disc_loss: {running_discloss:.2f}')

    gene.eval()
    time2 = time.perf_counter() - time1

    print(f'training completed in {int(time2 // 60)} Mins {int(time2 % 60)} Sec')
    return history;



