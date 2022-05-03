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
device = torch.device(f'cuda:{config["gpu_id"]}' if torch.cuda.is_available() else 'cpu')


torch.backends.cudnn.benchmarks = True
torch.backends.cudnn.deterministic = True
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# print(config.device)

# train_data, val_data = get_dataloader()
# print(len(train_data))
# print(len(val_data))

model = return_model()
model = model.to(device)


model.load_state_dict(torch.load('resnet_opt.pt'))
model.eval()

x = torch.randn((1,3,224,224), dtype=torch.float32, device=device)

torch.onnx.export(model,                       # model being run
                  x,                           # model input (or a tuple for multiple inputs)
                  'resnet_opt.onnx',             # Path to saved onnx model
                  export_params=True,          # store the trained parameter weights inside the model file
                  opset_version=13,            # the ONNX version to export the model to
                  input_names = ['input'],     # the model's input names
                  output_names = ['output'],   # the model's output names
                  dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
                                'output' : {0 : 'batch_size'}})