import pandas as pd
import numpy as np
import torch
import torchvision                  
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torchtext.legacy.data import Field, TabularDataset, BucketIterator
import spacy
from nltk.tokenize import word_tokenize
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
# text preprocessing

def tokenize(text):
    return [tok for tok in word_tokenize(text)]



# tokenize = lambda x : x.split()

quote = Field(sequential=True,use_vocab=True,tokenize=tokenize,lower=True,batch_first=True)
score = Field(sequential=False,use_vocab=False,batch_first=True)

fields = {'text':('text',quote),'category':('category',score)}

train,validation,test = TabularDataset.splits(
    path = '',
    train='train.csv',
    test='test.csv',
    validation='validation.csv',
    format= 'csv',
    fields= fields
)

# print(len(test))
# print(train[0].__dict__.keys())
# print(train[0].__dict__.values())


quote.build_vocab(train,
                  max_size=10001,
                  min_freq = 2)

train_iter,test_iterator,validation_iter = BucketIterator.splits(
    (train,test,validation),
    batch_size=64,
    device='cpu'
)

print(len(train_iter))
print(len(test_iterator))
print(len(validation_iter))

# building models
# for i,value in enumerate(train_iter):
#     print(value.text.shape)
#     print(value.category.shape)


# embed = nn.Embedding(len(quote.vocab),300)
# for i , value in enumerate(train_iter):
#     part = embed(value.text)
#     print(part.shape)
    
class lstm(nn.Module):
    def __init__(self,vocab_size,embedding_dim,hidden_dim,output_dim,n_layers):
        super (lstm  ,self) .__init__()

        self.embedding = nn.Embedding(vocab_size,embedding_dim)

        self.lstm1 = nn.LSTM(input_size=embedding_dim,hidden_size=hidden_dim,num_layers=n_layers,batch_first=True)
        self.drop = nn.Dropout(p=0.5)
        self.fc = nn.Linear(hidden_dim,output_dim)

    def forward(self,text,text_len):

        # text [batchsize,sent_len]
        textEmb = self.embedding(text)
        #embeded [batchsize,sent_len,emb_dim]


        packed_input = pack_padded_sequence(textEmb,text_len,batch_first=True)

        packed_output ,(hidden,cell) = self.lstm1(packed_input)

        # hidden = [batchsize,numlayers*numdirections,hiddim]
        # cell = [batchsize,numlayers*numdirections,hiddendim]

        dense_output = self.fc(hidden)

        return dense_output


# model = lstm(vocab_size=len(quote.vocab),embedding_dim=300,hidden_dim=128,output_dim=6,n_layers=1)

# for idx , batch in enumerate(train_iter):
#     data = batch.text
#     # print(category,cat_len)
#     print(data.shape)
#     print()
#     print(data)
#     break
