import torch
class configs(object):
    epochs = 50
    lr= 2e-4
    batch_size=16
    pin_memory = True
    num_workers=4
    seed = 42
    train_path = '/DATA/dataset/sat2map/maps/train'
    val_path = '/DATA/dataset/sat2map/maps/val'
    image_size= 256
    gpu_id=7
    save_test_imgs = './test.svg'
    device= torch.device(f'cuda:{gpu_id}' if torch.cuda.is_available else 'cpu') 
    save_loss_path = './loss.svg'
    verbose=True
    model_path = './generator.pt'

config = configs()