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
import onnx
import onnxruntime
# from model import return_models

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" 
# api_key = 'ae12d9032b94bfedc39f2e1beacfbf9909359ffc'
# os.environ['WANDB_API_KEY'] = api_key 
# os.environ["CUDA_VISIBLE_DEVICES"]=config.gpu_id

torch.backends.cudnn.benchmarks = True
torch.backends.cudnn.deterministic = True
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# print(config.device)

train_loader, test_loader, val_loader = return_dataloader()
print(len(test_loader))

print(onnxruntime.get_device())

session = onnxruntime.InferenceSession('resnet_opt.onnx',providers=['CUDAExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

print(input_name)
print(output_name)

sample_images,label = next(iter(test_loader))
sample_images = sample_images[:5]
print(sample_images.shape)
sample_images = sample_images.numpy()

result = session.run([output_name],{input_name:sample_images})[0]
print('model ouptut')
print(F.softmax(torch.from_numpy(result),dim=1).max(dim=1)[1])
print('ground truth')
print(label[:5])

