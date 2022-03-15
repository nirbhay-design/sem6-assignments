## Nirbhay Sharma (B19CSE114)
## DLops lab-assignment - 2

---


**For gpu, n_workers in the hyperparameter can be ignored and rest other parameters are as it is**

### Hyperparameter1: (Batchsize = 32, epochs = 10, lr = 0.001, n_workers = 2)
|model | gpu-accuracy | gpu-time | gpu-optim-acc| gpu-optim-time|
|---|---|---|---|---|
|Resnet18| 0.9|8min 43s | 0.9205 | 5min 20s|
|Resnet50| 0.901|12min 60s| 0.8821 | 6min 21s|

### Hyperparameter2: (Batchsize = 16, epochs = 10, lr = 0.001, n_workers = 4)
|model | gpu-accuracy | gpu-time | gpu-optim-acc| gpu-optim-time|
|---|---|---|---|---|
|Resnet18| 0.876|12min 17s|0.9123|4min 25s| 
|Resnet50| 0.871 |12min 38s|0.88|5min 36s|