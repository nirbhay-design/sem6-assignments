# -*- coding: utf-8 -*-
"""assn2-que-2a.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j_i7cUM5cI9OHhr9EgwaquD8O_ITOsMQ
"""

import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import numpy as np
import torch.optim as optim
import random
import time
import os
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score,precision_recall_fscore_support,auc
from sklearn.preprocessing import label_binarize
import warnings
warnings.filterwarnings('ignore')

#from google.colab import drive
#drive.mount('/content/gdrive')

#path = "/content/gdrive/MyDrive/MaskNomaskdataset/tiny-imagenet-200.zip"
#import zipfile
#with zipfile.ZipFile(path, 'r') as zip_ref:
#    zip_ref.extractall('/content/tinyimgnet')

config = dict(
    train_data = "../../../dataset/miniimgnet_dlassignment/tinyimgnet/tiny-imagenet-200/train",
    test_data = "../../../dataset/miniimgnet_dlassignment/tinyimgnet/tiny-imagenet-200/val/images",
    test_anno="../../../dataset/miniimgnet_dlassignment/tinyimgnet/tiny-imagenet-200/val/val_annotations.txt",
    wnids = "../../../dataset/miniimgnet_dlassignment/tinyimgnet/tiny-imagenet-200/wnids.txt",
    lr = 0.001,
    EPOCHS = 20,
    BATCH_SIZE = 32,
    IMAGE_SIZE = 64,
    pin_memory = True,
    num_workers = 2,
    SEED = 42,
    GPU_ID=2,
    val_split = 0.2
)

class CustomTestDataset():
  def __init__(self,img_path):
    self.img_path = img_path
    with open(config['wnids']) as f:
      self.wnids = f.read().split('\n')
      self.wnids.remove('')

    with open(config['test_anno']) as f:
      self.test_anno = list(map(lambda x:x.split('\t')[:2],f.read().split("\n")))
      self.test_anno.remove([''])

    self.wnids = sorted(self.wnids,key = lambda x:x)
    self.mapping = dict(list(zip(self.wnids,list(range(200)))))
    # self.rev_mapping = {j:i for i,j in self.mapping.items()}
    self.transformations = transforms.ToTensor()

  def __len__(self):
    return len(self.test_anno)

  def __getitem__(self,idx):
    test_img, class_name = self.test_anno[idx]
    cls_idx = self.mapping.get(class_name,-1)
    
    img = Image.open(os.path.join(config['test_data'],test_img)).convert('RGB')
    img = self.transformations(img)
    return (img,cls_idx)

class CustomTrainDataset():
  def __init__(self,img_path):
    self.img_path = img_path
    with open(config['wnids']) as f:
      self.wnids = f.read().split('\n')
      self.wnids.remove('')
    self.wnids = sorted(self.wnids,key = lambda x:x)
    self.mapping = dict(list(zip(self.wnids,list(range(200)))))
    self.rev_mapping = {j:i for i,j in self.mapping.items()}

    img_class = os.listdir(self.img_path)
    self.img_map = {}
    for clss in img_class:
      cls_imgs = os.listdir(os.path.join(self.img_path,clss,'images'))
      self.img_map[clss] = cls_imgs
    
    self.transformations = transforms.ToTensor()

    self.lenn = np.array(list(map(lambda x:len(x),list(self.img_map.values())))).sum()
  def __len__(self):
    return self.lenn

  def __getitem__(self,idx):
    anc,neg = random.sample(list(range(200)),2)
    anc_class = self.rev_mapping.get(anc,-1)
    neg_class = self.rev_mapping.get(neg,-1)

    aimg1,aimg2 = random.sample(self.img_map[anc_class],2)
    nimg3 = random.choice(self.img_map[neg_class])

    img1 = Image.open(os.path.join(self.img_path,anc_class,'images',aimg1)).convert('RGB')
    img1 = self.transformations(img1)

    img2 = Image.open(os.path.join(self.img_path,anc_class,'images',aimg2)).convert('RGB')
    img2 = self.transformations(img2)

    img3 = Image.open(os.path.join(self.img_path,neg_class,'images',nimg3)).convert('RGB')
    img3 = self.transformations(img3)

    return (img1,img2,img3,anc)

# # ctd = CustomTestDataset(config['test_data'])
# # test_loader = torch.utils.data.DataLoader(ctd,batch_size=config['BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])

# cTd = CustomTrainDataset(config['train_data'])
# # print(len(cTd))
# train_loader = torch.utils.data.DataLoader(cTd,batch_size=config['BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])
# for idx,(img1,img2,img3,target) in enumerate(train_loader):
#   fig,(ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,4))
#   ax1.imshow(img1[0].permute(1,2,0))
#   ax2.imshow(img2[0].permute(1,2,0))
#   ax3.imshow(img3[0].permute(1,2,0))
#   plt.show()
#   print('-----------------------')
#   if (idx == 4):
#     break;

device = torch.device(f'cuda:{config["GPU_ID"]}' if torch.cuda.is_available() else 'cpu')
print(device)

config['DEVICE'] = device

torch.manual_seed(config['SEED'])
torch.cuda.manual_seed(config['SEED'])


transformations = {
  'train':torchvision.transforms.Compose([
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

def get_params(model):
  par = 0
  for params in model.parameters():
    if (params.requires_grad == True):
      par += params.numel()
  return par

class D_triplet(nn.Module):
  def __init__(self,num_class=200):
    super(D_triplet,self).__init__()
    self.n_class = num_class
    self.dnet = torchvision.models.densenet121(pretrained=True)
    self.dnet.classifier = nn.Sequential()
    self.classifier = nn.Linear(1024,self.n_class)
    print(get_params(self.dnet))

    for name,params in self.dnet.named_parameters():
      if (name == "features.denseblock4.denselayer16.norm1.weight"):
        break
      params.requires_grad = False

    print(get_params(self.dnet))

  def forward(self,x):
    x = self.dnet(x)
    x1 = self.classifier(x)
    return x,x1    

# print(Dnet)

def train(model,loader,lossfunction1,lossfunction2,optimizer,n_epochs=200):
  tval = {"trainloss":[]}
  starttime = time.time()
  for epochs in range(n_epochs):
      model.train()
      cur_loss = 0
      len_train = len(loader)
      for idx , (anc,pos,neg,target) in enumerate(loader):
          anc = transformations['train'](anc)
          pos = transformations['train'](pos)
          neg = transformations['train'](neg)    
          anc = anc.to(device)
          pos = pos.to(device)
          neg = neg.to(device)
          target = target.to(device)
          # model = model.to(device)

          e_a,scores_a = model(anc)
          e_p,_ = model(pos)
          e_n,_ = model(neg)    
          loss1 = lossfunction1(scores_a,target)
          loss2 = lossfunction2(e_a,e_p,e_n)

          loss = loss1 + loss2
          cur_loss += loss.item() / (len_train)
          
          optimizer.zero_grad()
          loss.backward()
          optimizer.step()

          print(f'TrainBatchDone:{idx}',end='\r') 
      
      tval['trainloss'].append(float(cur_loss))
      
      print(f'epoch:[{epochs+1}/{n_epochs}], TrainLoss:{cur_loss:.3f}') 

  time2 = time.time() - starttime
  print(f'done time {time2/60:.3f} Mins')
  return tval


def evaluate(model,loader,name='test'):
  model.eval()
  correct = 0;samples =0
  pre_prob = []
  lab = []
  predicted_labels = []

  with torch.no_grad():
      for idx,(x,y) in enumerate(loader):
          x = transformations['test'](x)
          x = x.to(device)
          y = y.to(device)
          # model = model.to(device)

          _,scores = model(x)
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
      
      print(f'correct are {correct/samples:.3f}')
      
  model.train()
  return np.array(lab),np.array(predicted_labels),np.array(pre_prob)

ctd = CustomTestDataset(config['test_data'])
test_loader = torch.utils.data.DataLoader(ctd,batch_size=config['BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])

cTd = CustomTrainDataset(config['train_data'])
train_data,_ = torch.utils.data.dataset.random_split(cTd,[30000,100000-30000])
train_loader = torch.utils.data.DataLoader(train_data,batch_size=config['BATCH_SIZE'],shuffle=True,num_workers=config['num_workers'],pin_memory=config['pin_memory'])
print(len(train_loader))
print(len(test_loader))

Dnet = D_triplet()
Dnet = Dnet.to(device)
lossfunction1 = nn.CrossEntropyLoss()
lossfunction2 = nn.TripletMarginLoss()

optimizer = optim.Adam(Dnet.parameters(),lr=config['lr'])

history = train(Dnet,train_loader,lossfunction1,lossfunction2,optimizer,n_epochs=config['EPOCHS'])

y_true,y_pred,pred_prob = evaluate(Dnet,test_loader)

precision,recall,f_score,_ = precision_recall_fscore_support(y_true,y_pred)
print('precision: ',np.array(precision).mean())
print('recall: ',np.array(recall).mean())
print('f_score: ',np.array(f_score).mean())



