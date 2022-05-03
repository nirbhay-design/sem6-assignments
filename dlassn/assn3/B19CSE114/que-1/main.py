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
from Customdatamodel import generator, discriminator, get_dataloader, train, config, init_wt

def plotloss(history):
    len_values = len(history['genloss'])
    plt.figure(figsize=(5,4))
    plt.plot(list(range(1,len_values + 1)),history['genloss'], label = 'genloss')
    plt.plot(list(range(1,len_values + 1)),history['discloss'], label = 'discloss')
    plt.xlabel('iterations')
    plt.ylabel('loss')
    plt.legend()
    plt.savefig(config.save_loss_path,format='svg')
    plt.show()
    
def pipeline():
    torch.manual_seed(config.seed)
    torch.cuda.manual_seed(config.seed)

    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"  
    # os.environ["CUDA_VISIBLE_DEVICES"]=config.gpu_id
    
    torch.backends.cudnn.benchmarks = True
    torch.backends.cudnn.deterministic = True
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    print(config.device)

    train_data, test_data = get_dataloader()
    gene = generator(config.z_dim,1,64)
    disc = discriminator(features_d=64,other=False)
    # gene = init_wt(gene)
    # disc = init_wt(disc)
    gene = gene.to(config.device)
    disc = disc.to(config.device)
    lossfunction = nn.BCEWithLogitsLoss()

    g_scaler = torch.cuda.amp.GradScaler()
    d_scaler = torch.cuda.amp.GradScaler()
    # lossfunction = nn.BCELoss()

    ogen = optim.Adam(gene.parameters(),lr=config.lr,betas = (0.5,0.999))
    odis = optim.Adam(disc.parameters(),lr=config.lr,betas = (0.5,0.999))

    history = train(gene, disc, train_data, lossfunction,ogen, odis,g_scaler,d_scaler, n_epochs = config.epochs)
    plotloss(history)

if __name__ == "__main__":
    pipeline()


'''
def showimg(train_data):
    img,label = next(iter(train_data))
    array = []
    for image in img:
        array.append(image.squeeze(0).numpy())
    i = 0
    stack_array = []
    for j in range(4):
        stack_array.append(np.hstack(array[i:i+8]))
        i += 8
    plt.imshow(np.vstack(stack_array),cmap='gray')
    plt.show()    

'''