import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from paddlex.det import transforms
import paddlex as pdx

# 定义训练和验证时的transforms
# API说明 https://paddlex.readthedocs.io/zh_CN/develop/apis/transforms/det_transforms.html
train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(), transforms.Normalize(),
    transforms.ResizeByShort(
        short_size=800, max_size=1333), transforms.Padding(coarsest_stride=32)
])

eval_transforms = transforms.Compose([
    transforms.Normalize(), transforms.ResizeByShort(
        short_size=800, max_size=1333), transforms.Padding(coarsest_stride=32)
])

# 定义训练和验证所用的数据集
# API说明：https://paddlex.readthedocs.io/zh_CN/develop/apis/datasets.html#paddlex-datasets-vocdetection
train_dataset = pdx.datasets.CocoDetection(
    data_dir='/home/aistudio/data/dataset/detection/JPEGImages',
    ann_file='/home/aistudio/data/dataset/detection/train.json',
    transforms=train_transforms,
    shuffle=True)
eval_dataset = pdx.datasets.CocoDetection(
    data_dir='/home/aistudio/data/dataset/detection/JPEGImages',
    ann_file='/home/aistudio/data/dataset/detection/val.json',
    transforms=eval_transforms)

# 初始化模型，并进行训练
# 可使用VisualDL查看训练指标，参考https://paddlex.readthedocs.io/zh_CN/develop/train/visualdl.html
# num_classes 需要设置为包含背景类的类别数，即: 目标类别数量 + 1
num_classes = len(train_dataset.labels) + 1

# API说明: https://paddlex.readthedocs.io/zh_CN/develop/apis/models/detection.html#paddlex-det-fasterrcnn
model = pdx.det.FasterRCNN(num_classes=num_classes, backbone='ResNet50_vd')

# API说明: https://paddlex.readthedocs.io/zh_CN/develop/apis/models/detection.html#id5
# 各参数介绍与调整说明：https://paddlex.readthedocs.io/zh_CN/develop/appendix/parameters.html
model.train(
    num_epochs=12,
    train_dataset=train_dataset,
    train_batch_size=4,
    eval_dataset=eval_dataset,
    learning_rate=0.0025,
    lr_decay_epochs=[8, 11],
    save_dir='output/fster_rcnn_r50_vd_fpn',
    use_vdl=True)
