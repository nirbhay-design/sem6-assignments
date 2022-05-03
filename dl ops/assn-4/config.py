import torchvision.transforms as transforms

config = dict(
    BATCH_SIZE = 32,
    epochs= 10,
    lr = 1e-3,
    # normal_data = "/workspace/Dlops-assignment/dataset/TB_Chest_Radiography_Database/Normal",
    normal_data = "/DATA/sharma59/dl-assignment/Dlops_assignment/dataset/TB_Chest_Radiography_Database/Normal",
    # abnormal_data = "/workspace/Dlops-assignment/dataset/TB_Chest_Radiography_Database/Tuberculosis",
    abnormal_data = "/DATA/sharma59/dl-assignment/Dlops_assignment/dataset/TB_Chest_Radiography_Database/Tuberculosis",
    pin_memory = True,
    num_workers=4,
    IMAGE_SIZE = 224,
    saved_model_resnet_normal = "/DATA/sharma59/dl-assignment/Dlops_assignment/scripts/resnet.pt", 
    saved_model_resnet_opt = "/DATA/sharma59/dl-assignment/Dlops_assignment/scripts/resnet_opt.pt", 
    saved_model_vgg_normal = "/DATA/sharma59/dl-assignment/Dlops_assignment/scripts/vgg.pt", 
    saved_model_vgg_opt = "/DATA/sharma59/dl-assignment/Dlops_assignment/scripts/vgg_opt.pt",
    model_ = 'resnet',
    val_split = 0.1,
    test_split = 0.2,
    optimized=True,
    seed=42,
    gpu_id=7,
    transformations = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    images_save_path = "/DATA/sharma59/dl-assignment/Dlops_assignment/scripts/loss_acc_resnet.svg",
    images_save_path_optimal = "/DATA/sharma59/dl-assignment/Dlops_assignment/scripts/loss_acc_resnet_opt.svg",
    verbosity = 0
)
