# This folder contains python script to train the vehicle's CV model for in situ object detecting
# 作者：DEEPLEARNING
## 程序：
### 基础库：
- paddledet
- paddleseg
- paddlex
+ 安装方法：进入命令行，输入`cd ~/env`进入env目录，运行`python setup.py`或直接输入`pip install -r requirements.txt`  

### 预测模型：
#### 目标检测：
- 架构：Faster RCNN 
- 骨架：HRNet_W18 + FPN
- 模型目录（inference格式）：model/fster_rcnn_hrnet_fpn_960x576
- 配置文件：model/fastscnn_cityscape_512x512/model.yml
#### 目标检测：
- 架构：FastSCNN 
- 骨架：cityscape
- 模型目录（inference格式）：model/fastscnn_cityscape_512x512
- 配置文件：model/fastscnn_cityscape_512x512/model.yml  

### 训练脚本
- 集成训练方法：进入命令行，输入`python train.py`
- 独立训练方法：进入命令行，输入`python det_train.py`或`python seg_train.py`

### 预测脚本
- predict.py
- 运行方法 python predict.py <检测图片列表（txt格式）> <json文件输出路径>
- 可选（若有TensorRT支持库，请将paddlex.deploy.Predictor中use_trt属性改为True，可在一定程度上提升运行速度）
