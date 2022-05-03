from config import config
import sys
import torchvision
import torch

def return_model():
    if config['model_'] == 'vgg':
        print('loading vgg')
        vgg_model = torchvision.models.vgg16(pretrained=True)
        vgg_model.classifier[6] = torch.nn.Linear(in_features=4096, out_features=2, bias=True)
        return vgg_model
    else:
        print('loading resnet')
        resnet_model = torchvision.models.resnet50(pretrained=True)
        resnet_model.fc = torch.nn.Linear(in_features=2048, out_features=2, bias=True)
        return resnet_model