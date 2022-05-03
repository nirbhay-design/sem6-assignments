from config import config
import os
import torch
import torchvision
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import time
import torch.nn as nn
from custom_dataset import return_dataloader
from cnn_models import return_model
import torch.nn.functional as F
import torch.optim as optim
import os

device = torch.device(f'cuda:{config["gpu_id"]}' if torch.cuda.is_available() else "cpu")


def train(model,train_load,val_loader,optimizer,lossfunction,grad_scaler,n_epochs):
    tval = {'trainacc':[],"trainloss":[],"valacc":[],"valloss":[]}
    starttime = time.perf_counter()
    for epochs in range(n_epochs):
        model.train()
        cur_loss = 0
        curacc = 0
        cur_val_loss = 0
        curvalacc = 0
        len_train = len(train_load)
        for idx , (data,target) in enumerate(train_load):
            data = config['transformations'](data)    
            data = data.to(device)
            target = target.to(device)
            # model = model.to(device)
            with torch.cuda.amp.autocast():
                scores = model(data)    
                # print(scores.shape)
                loss = lossfunction(scores,target)

            cur_loss += loss.item() / (len_train)
            scores = F.softmax(scores,dim = 1)
            _,predicted = torch.max(scores,dim = 1)
            correct = (predicted == target).sum()
            samples = scores.shape[0]
            curacc += correct / (samples * len_train)

            optimizer.zero_grad()
            grad_scaler.scale(loss).backward()
            grad_scaler.step(optimizer)
            grad_scaler.update()
            # optimizer.step()

            if config['verbosity']:
                print('TrainBatchDone:{:d}'.format(idx),end='\r') 
        
        model.eval()

        len_val = len(val_loader)
        for idx,(data,target) in enumerate(val_loader):
            data = config['transformations'](data)
            data = data.to(device)
            target = target.to(device)

            scores = model(data)
            loss_value = lossfunction(scores,target)

            cur_val_loss += (loss_value.item() / len_val)  

            scores = F.softmax(scores,dim=1)
            _,predicted = torch.max(scores,dim=1)
            correct = (predicted == target).sum()
            samples = scores.shape[0]
            curvalacc += (correct/ (samples * len_val))
            
            if config['verbosity']:
                print(f'ValidationBatch:{idx}',end='\r')
        
        model.train()

  
        tval['trainacc'].append(float(curacc))
        tval['trainloss'].append(float(cur_loss))
        tval['valacc'].append(float(curvalacc))
        tval['valloss'].append(float(cur_val_loss))
      
        print('epoch:[{:d}/{:d}], TrainAcc:{:.3f}, TrainLoss:{:.3f}, ValAcc:{:.3f}, ValLoss:{:.3f}'.format(epochs+1,n_epochs,curacc,cur_loss,curvalacc,cur_val_loss)) 

    time2 = time.perf_counter() - starttime
    print(f'done time {int(time2//60)} Mins {int(time2%60)} Sec')
    return tval

def loss_acc_curve(tval,save_path): # tval -> [{tvals}]
    plt.figure(figsize=(5,4))
    plt.plot(list(range(1,config['epochs']+1)),tval['trainloss'],label="trainloss")
    plt.plot(list(range(1,config['epochs']+1)),tval['valloss'],label="valloss")
    plt.plot(list(range(1,config['epochs']+1)),tval['trainacc'],label="trainacc")
    plt.plot(list(range(1,config['epochs']+1)),tval['valacc'],label="valacc")
    plt.legend()
    plt.xlabel("epochs")
    plt.ylabel("loss / accuracy")
    plt.title('loss accuracy curve')
    plt.savefig(save_path,format='svg') 

def evaluate(model,loader,name='test'):
    model.eval()
    correct = 0;samples =0
    fpr_tpr_auc = {}
    pre_prob = []
    lab = []
    predicted_labels = []

    with torch.no_grad():
        for idx,(x,y) in enumerate(loader):
            x = config['transformations'](x)
            x = x.to(device)
            y = y.to(device)
            # model = model.to(device)

            scores = model(x)
            predict_prob = F.softmax(scores)
            _,predictions = predict_prob.max(1)

            predictions = predictions.to('cpu')
            y = y.to('cpu')
            predict_prob = predict_prob.to('cpu')

            predicted_labels.extend(list(predictions.numpy()))
            pre_prob.extend(list(predict_prob.numpy()))
            lab.extend(list(y.numpy()))

            correct += (predictions == y).sum()
            samples += predictions.size(0)

            if config['verbosity']:
                print('batches done : ',idx,end='\r')

        print('correct are {:.2f}'.format(correct/samples))
      
    model.train()
    accuracy = correct/samples
    return accuracy

def train_model_optimized():
    train_loader, test_loader, val_loader = return_dataloader()
    torchmodel = return_model()

    torch.manual_seed(config['seed'])
    torch.cuda.manual_seed(config['seed'])

    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"  
    # os.environ["CUDA_VISIBLE_DEVICES"]="2"

    torch.backends.cudnn.benchmarks = True
    torch.backends.cudnn.deterministic = True
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    torchmodel = torchmodel.to(device)
    lossfunction = nn.CrossEntropyLoss()
    optimizer = optim.Adam(params=torchmodel.parameters(),lr=config['lr'])
    grad_scaler = torch.cuda.amp.GradScaler()

    # getparams(torchmodel)
    history = train(torchmodel,train_loader,val_loader,optimizer,lossfunction,grad_scaler,n_epochs=config['epochs'])
    loss_acc_curve(history,config['images_save_path_optimal'])

    test_acc = evaluate(torchmodel,test_loader,name='test')
    print('test_accuracy',test_acc)

    if config['model_'] == 'resnet':
        torch.save(torchmodel.state_dict(),config['saved_model_resnet_opt'])
    elif config['model_'] == 'vgg':
        torch.save(torchmodel.state_dict(),config['saved_model_vgg_opt'])



