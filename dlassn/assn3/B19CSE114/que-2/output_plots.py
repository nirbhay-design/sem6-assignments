import matplotlib.pyplot as plt
import sys
import os

title = sys.argv[1]
direct = sys.argv[2]

file_names = list(filter(lambda x:'txt' in x, os.listdir(direct)))
# print(file_names)

train_loss,val_loss,train_acc,val_acc = file_names
train_loss_path = os.path.join(direct,train_loss)
val_loss_path = os.path.join(direct,val_loss)
train_acc_path = os.path.join(direct,train_acc)
val_acc_path = os.path.join(direct,val_acc)

# print(train_loss_path,val_loss_path,train_acc_path,val_acc_path)


def plot_loss():
    with open(train_loss_path,'r') as f:
        data = f.read().split('\n')[:-1]
        train_loss_values = list(map(lambda x:float(x),data))
    with open(val_loss_path,'r') as f:
        data = f.read().split('\n')[:-1]
        val_loss_values = list(map(lambda x:float(x),data))
    train_len = len(train_loss_values)
    val_len = len(val_loss_values)
    plt.figure(figsize=(5,4))
    plt.plot(list(range(1,train_len+1)),train_loss_values,label='train_loss')
    plt.plot(list(range(1,val_len+1)),val_loss_values,label='val_loss')
    plt.xlabel('steps')
    plt.ylabel('loss')
    plt.title(title)
    plt.legend()
    plt.savefig(title+'loss.svg',format='svg')
    plt.show()

def plot_acc():
    with open(train_acc_path,'r') as f:
        data = f.read().split('\n')[:-1]
        train_acc_values = list(map(lambda x:float(x),data))
    with open(val_acc_path,'r') as f:
        data = f.read().split('\n')[:-1]
        val_acc_values = list(map(lambda x:float(x),data))
    train_len = len(train_acc_values)
    val_len = len(val_acc_values)
    plt.figure(figsize=(5,4))
    plt.plot(list(range(1,train_len+1)),train_acc_values,label='train_acc')
    plt.plot(list(range(1,val_len+1)),val_acc_values,label='val_acc')
    plt.xlabel('steps')
    plt.ylabel('accuracy')
    plt.title(title)
    plt.legend()
    plt.savefig(title+'acc.svg',format='svg')
    plt.show()

plot_loss()
plot_acc()

