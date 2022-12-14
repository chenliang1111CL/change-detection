# 项目说明
* 深度学习遥感影像项目支撑
* 已上传原始spacenet7基线代码
* 已上传比赛前5名代码
* 已上传一个实验性的分割网络项目

# 基线代码的使用
* 拉取基线代码环境镜像docker pull kostagiolasn/sn7_baseline_image
* 建立环境容器docker run -it --gpus all  -p 8080:6006 -p 10001:22 -v 代码路径:/tmp -v 数据路径:/data  -ti --ipc=host --name sn7_gpu0(容器名称) f61e8c2b094b(镜像编号)  /bin/bash
* 进入镜像solaris环境（在容器命令行输入conda activate solaris）
* 启动jupyter服务jupyter-notebook --allow-root --ip=0.0.0.0 --port=22
* 在本地用浏览器打开jupyter-notebook（127.0.0.1：10001），输入上一步中启动时返回的token
* 即可打开基线notebooks代码，完成数据准备等操作，注意修改数据集路径


# 分割网络的实验
* 我上传了一个项目，HRNet_segmentation，里边包含了一个UNet和一个HRNet，只需要在创建网络的时候切换一下就行了，具体的说明在文件夹里有单独的readme

# 后处理部分
* 利用分割网络的预测结果，进行后处理，得到时间序列上的预测效果，可以参考基线代码完成
* 分割完成后的后处理部分同学们尽快熟悉一下，最尽快走完全流程，最好能根据参赛者的思路，直接用GDAL库来实现，绕开基线代码用到的solaris，个人感觉它在安装上不太友好，不便于之后我们的部署。个人认为这一部分是需要优先完成的东西，如何认定房屋的增加，对时间序列上的考虑，都是在这一过程中完成

# 工作安排
* test文件夹中为辅助代码，文件夹中有具体说明，特别是后处理部分，希望同学们早日走通全流程

# 更新

## 2022.11.05 Update by JG
上传后处理思路实现Demo
