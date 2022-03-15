import PIL
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import copy
import matplotlib.pyplot as plt
import os
import time
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

#--------------------------------------------------Optimizations-------------------------------------------

from torchvision.transforms.transforms import Resize
config = dict(
    DATA_PATH = "../../../dataset/DogvsCats_dlassignment/dogcat/PetImages",
    lr = 0.001,
    EPOCHS = 20,
    BATCH_SIZE = 1,
    IMAGE_SIZE = 128,
    pin_memory = True,
    num_workers = 2,
    SEED = 42,
    GPU_ID=2,
    MINI_BATCH_SIZE = 32,
    test_split = 0.3
)
device = torch.device(f'cuda:{config["GPU_ID"]}' if torch.cuda.is_available() else 'cpu')
print(device)

config['DEVICE'] = device

torch.manual_seed(config['SEED'])
torch.cuda.manual_seed(config['SEED'])


transformations = {
  'general':torchvision.transforms.Compose([
          torchvision.transforms.Resize((config['IMAGE_SIZE'],config['IMAGE_SIZE'])),
          torchvision.transforms.ToTensor(),
          torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ]),
  'train':torchvision.transforms.Compose([
          torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ]),
  'val':torchvision.transforms.Compose([
          torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ]),
  'test':torchvision.transforms.Compose([
          torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ]),
}

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"  
# os.environ["CUDA_VISIBLE_DEVICES"]="2"

torch.backends.cudnn.benchmarks = True
torch.backends.cudnn.deterministic = True
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

#--------------------------------------------------LoadData-------------------------------------------
# get the dataset
traindata = torchvision.datasets.ImageFolder(root=config['DATA_PATH'],transform = transformations['general'])
train_len = len(traindata)
test_len = int(config['test_split'] * train_len)
effective_train_len = train_len - test_len 
print('train samples -> ',effective_train_len)
print('test samples ->', test_len)
print(traindata.class_to_idx)

train_data,test_data = torch.utils.data.dataset.random_split(traindata,[effective_train_len,test_len])
train_loader = torch.utils.data.DataLoader(dataset=train_data,batch_size=config['BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])
test_loader = torch.utils.data.DataLoader(dataset=test_data,batch_size=config['BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])

train_loader_minibatch = torch.utils.data.DataLoader(dataset=train_data,batch_size=config['MINI_BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])
test_loader_minibatch = torch.utils.data.DataLoader(dataset=test_data,batch_size=config['MINI_BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])

# print(len(train_loader),len(test_loader))
# print(len(train_loader_minibatch),len(test_loader_minibatch))

# img1 = PIL.Image.open(config['DATA_PATH']+'/Cat/3739.jpg')
# print(img1.size)

#----------------------------------------------Model-----------------------------------------------------
class model1(torch.nn.Module):
    
    def __init__(self,in_channels = 3,n_class=2):
        super(model1,self).__init__()
        self.n_class= n_class
        self.conv1 = torch.nn.Conv2d(in_channels=in_channels,out_channels=128,kernel_size=(3,3),bias=False)
        self.bn1 = nn.BatchNorm2d(128)
        self.relu1 = nn.ReLU()
        self.maxpool1 = torch.nn.MaxPool2d(kernel_size=(2,2),stride=2)
        self.conv2 = torch.nn.Conv2d(in_channels=128,out_channels=64,kernel_size=(3,3))
        self.relu2 = nn.ReLU()
        self.maxpool2 = torch.nn.MaxPool2d(kernel_size=(2,2),stride=2)
        self.conv3 = torch.nn.Conv2d(in_channels=64,out_channels = 32,kernel_size=(3,3),bias=False)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu3 = nn.ReLU()
        
        # output layer
        self.aap = nn.AdaptiveAvgPool2d((8,8))
        self.fc1 = torch.nn.Linear(in_features=32*8*8,out_features=self.n_class)

    def forward(self,x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)
        x = self.conv3(x)
        x = self.bn2(x)
        x = self.relu3(x)
        # x => [B,32,H,w] => [B,32 * H * W]
        x = self.aap(x)
        x = torch.flatten(x,start_dim=1)
        x = self.fc1(x)
        return x

#-------------------------------------------train-------------------------------------------

def train(model,train_load,lossfunction,optimizer,n_epochs=200):
    tval = {'trainacc':[],"trainloss":[]}
    starttime = time.time()
    for epochs in range(n_epochs):
        model.train()
        cur_loss = 0
        curacc = 0
        len_train = len(train_load)
        for idx , (data,target) in enumerate(train_load):
            data = transformations['train'](data)    
            data = data.to(device)
            target = target.to(device)
            # model = model.to(device)

            scores = model(data)    
            loss = lossfunction(scores,target)
            cur_loss += loss.item() / (len_train)
            scores = F.softmax(scores,dim = 1)
            _,predicted = torch.max(scores,dim = 1)
            correct = (predicted == target).sum()
            samples = scores.shape[0]
            curacc += correct / (samples * len_train)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print('TrainBatchDone:{:d}'.format(idx),end='\r') 
  
        tval['trainacc'].append(float(curacc))
        tval['trainloss'].append(float(cur_loss))
      
        print('epoch:[{:d}/{:d}], TrainAcc:{:.3f}, TrainLoss:{:.3f}'.format(epochs+1,n_epochs,curacc,cur_loss)) 

    time2 = time.time() - starttime
    print('done time {:.3f} Mins'.format(time2/60))
    return tval

def getparams(model):
    total_parameters = 0
    for name,parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        param = parameter.numel()
        total_parameters += param
    print(f"total_trainable_parameters are : {total_parameters}")

def loss_curve(tval,save_path): # tval -> [{tvals}]
    # print(tval['trainacc'])
    label_map = {0:'vanilla sgd',1:'MB sgd',2:'MB momentum',3:'MB adam'}
    plt.figure(figsize=(5,4))
    for i in range(len(tval)):
        plt.plot(list(range(1,config['EPOCHS']+1)),tval[i]['trainloss'],label=f'{label_map[i]}')
    plt.legend()
    plt.xlabel("epochs")
    plt.ylabel("loss")
    plt.title('loss curve')
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
            x = transformations['test'](x)
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

            print('batches done : ',idx,end='\r')

        print('correct are {:.2f}'.format(correct/samples))
      
    model.train()
    accuracy = correct/samples
    return accuracy

#--------------------------------vannilla sgd------------------------------------
torchmodel = model1()
torchmodel = torchmodel.to(device)

lossfunction = nn.CrossEntropyLoss()
optimizer = optim.SGD(params=torchmodel.parameters(),lr=config['lr'])

getparams(torchmodel)
history1 = train(torchmodel,train_loader,lossfunction,optimizer,n_epochs=config['EPOCHS'])

test_acc = evaluate(torchmodel,test_loader,name='test')
print('test_accuracy (vanilla sgd) ',test_acc)

#---------------------------------mini batch sgd----------------------------------
torchmodel = model1()
torchmodel = torchmodel.to(device)

lossfunction = nn.CrossEntropyLoss()
optimizer = optim.SGD(params=torchmodel.parameters(),lr=config['lr'])

# getparams(torchmodel)
history2 = train(torchmodel,train_loader_minibatch,lossfunction,optimizer,n_epochs=config['EPOCHS'])

test_acc = evaluate(torchmodel,test_loader_minibatch,name='test')
print('test_accuracy (Mb sgd) ',test_acc)

#-------------------------------mini batch + momentum ------------------------------

torchmodel = model1()
torchmodel = torchmodel.to(device)

lossfunction = nn.CrossEntropyLoss()
optimizer = optim.SGD(params=torchmodel.parameters(),lr=config['lr'],momentum=0.9)

# getparams(torchmodel)
history3 = train(torchmodel,train_loader_minibatch,lossfunction,optimizer,n_epochs=config['EPOCHS'])

test_acc = evaluate(torchmodel,test_loader_minibatch,name='test')
print('test_accuracy (Mb momentum) ',test_acc)

#--------------------------------mini batch + adam-------------------------------------
torchmodel = model1()
torchmodel = torchmodel.to(device)

lossfunction = nn.CrossEntropyLoss()
optimizer = optim.Adam(params=torchmodel.parameters(),lr=config['lr'])

# getparams(torchmodel)
history4 = train(torchmodel,train_loader_minibatch,lossfunction,optimizer,n_epochs=config['EPOCHS'])

test_acc = evaluate(torchmodel,test_loader_minibatch,name='test')
print('test_accuracy (Mb adam) ',test_acc)


#-------------------------------------plotting curves------------------------------------


history = [history1,history2,history3,history4]

loss_curve(history,'visual_curves/cnn_optim.svg')