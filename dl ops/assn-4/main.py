import sys
from config import config
from tb_gpu import train_model
from tb_gpu_optimized import train_model_optimized


if (sys.argv[2] == 'normal'):
    train_model()
elif (sys.argv[2] == 'optimize'):
    train_model_optimized()
else:
    print('--mode should be {normal/optimize}')

