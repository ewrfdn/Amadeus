项目初始化步骤
##windows 下部署开发

### 1. 安装cuda

###2. 下载cudnn


### 3. 设置环境变量

### 4. 创建conda env 环境
conda create -n Amadeus python==3.10

### 5. cd your-project-dir 激活环境
conda activate Amadeus
### 6.安装依赖
pip install -r ./requirement.text

如果conda 安装pytorch 失败，到https://pytorch.org/get-started/locally/ 中获取对应驱动程序对应的pyTorch
cuda 12.1 的安装命令如下
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

### 7. 确认pyTorch cuda 已经启用 打开python 
```python 
impprt torch
print(torch.cuda.is_available()) //如果返回为True 就是cuda已被启用
   ```
### 8. 编译相关依赖

cd 到 you-project/vits_server/vits/monotonic_align 下创建 monotonic_align 文件夹

初始化 monotonic_align
python setup.py build_ext --inplace
如果报错 No module named 'Cython
先 pip install cython  安装后再执行
如果 提示 error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
则需要去后面的链接下载Microsoft Visual C++ 14.0

## linux 下部署