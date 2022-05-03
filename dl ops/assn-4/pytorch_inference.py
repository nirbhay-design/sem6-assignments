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
from config import config
from custom_dataset import return_dataloader
# from model import return_models

def return_model():
    print('loading resnet')
    resnet_model = torchvision.models.resnet50()
    resnet_model.fc = torch.nn.Linear(in_features=2048, out_features=2, bias=True)
    return resnet_model

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" 
# api_key = 'ae12d9032b94bfedc39f2e1beacfbf9909359ffc'
# os.environ['WANDB_API_KEY'] = api_key 
# os.environ["CUDA_VISIBLE_DEVICES"]=config.gpu_id

torch.backends.cudnn.benchmarks = True
torch.backends.cudnn.deterministic = True
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

device = torch.device(f'cuda:{config["gpu_id"]}' if torch.cuda.is_available() else 'cpu')
print(device)

train_loader, test_loader, val_loader = return_dataloader()
print(len(test_loader))
torchmodel = return_model()

print('loading pretrained weights')
print(torchmodel.load_state_dict(torch.load('resnet_opt.pt')))
torchmodel = torchmodel.eval()
torchmodel = torchmodel.to(device)

def test_model(torchmodel,test_data):
    torchmodel.eval()
    class_map = {0:'normal',1:'abnormal'}
    x,y = next(iter(test_data))
    x = x.to(device)
    y = y.to(device)
    for i in range(15):
        x_i = x[i].unsqueeze(0)
        y_i = y[i].item()
        scores = torchmodel(x_i)

        prediction = F.softmax(scores,dim=1)
        _,pred_class = prediction.max(dim=1)
        pred_class = pred_class[0].item()

        print(f'image_name: {i+1}_example.png, ground_truth: {class_map[y_i]}, predicted: {class_map[pred_class]}')
    
        plt.figure(figsize=(10,8))
        plt.imshow(x_i.squeeze().permute(1,2,0).detach().cpu().numpy())
        plt.savefig(f'{i+1}_example.png')
        plt.show()


def test_model_accuracy(torchmodel,test_data):
    torchmodel.eval()
    class_map = {0:'normal',1:'abnormal'}
    accuracy = 0
    correct = 0
    samples = 0
    len_test = len(test_data)
    for idx,(x,y) in enumerate(test_data):
        x = x.to(device)
        y = y.to(device)
        scores = torchmodel(x)

        prediction = F.softmax(scores,dim=1)
        _,pred_classes = prediction.max(dim=1)
        correct += (pred_classes == y).sum()
        samples += x.shape[0]

        print(f'done {idx}',end='\r')
    accuracy = correct / samples
    print(accuracy)

        
# gene.load_state_dict(torch.load(config.model_path))
# test_model(torchmodel,test_loader)
test_model_accuracy(torchmodel,test_loader)