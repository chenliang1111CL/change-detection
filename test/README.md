# 该文件夹下代码说明
* 利用image_3x_divide.py实现影像的上采样和分割
* label_3x_divide.py实现标注样本的栅格化、上采样及分割
* y以上两步操作完成后，手动在train文件夹下剪切一组数据放入test文件夹，用于网络的验证
* 利用makeCSV.py读取以上两个生成的两个文件夹，生成训练用的CSV
* 准备好后就可以输入网络进行训练了
* 该部分代码已经重写，无需使用比赛提供的docker镜像
* 预处理后的的文件结构
```/home/user1/datasets/spacenet7/SN7_buildings_train
  ├── csvs: 训练和验证数据的路径集合，在完成上面的工作后，使用该项目中/test/makeCSV.py生成
  ├── train: 训练数据
        ├── train: 训练数据
  ├── test: 验证数据。由于原数据集test_public中未提供标签，我这里没有使用，而是从train中直接剪切出了一个地区作为验证数据
```
