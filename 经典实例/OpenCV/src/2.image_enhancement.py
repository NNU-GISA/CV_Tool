# 功能；图像预处理之图像增强

# 图像增强是图像处理中一种常用的技术，它的目的是增强图像中全局或局部有用的信息。合理利用图像增强技术能够针对性的
# 增强图像中感兴趣的特征，抑制图像中不感兴趣的特征，这样能够有效的改善图像的质量，增强图像的特征。

# 计算机视觉主要有两部分组成：1、特征提取 2、模型训练
# 其中第一条特征提取在计算机视觉中占据着至关重要的位置，尤其是在传统的计算机视觉算法中，更为明显，例如比较著名的
# HOG、DPM等目标识别模型，主要的研究经历都是在图像特征提取方面。图像增强能够有效的增强图像中有价值的信息，
# 改善图像质量，能够满足一些特征分析的需求，因此，可以用于计算机视觉数据预处理中，能够有效的改善图像的质量，
# 进而提升目标识别的精度。

# 图像增强可以分为两类：1、频域法 2、空间域法
# 1、频域法就是把图像从空域利用傅立叶、小波变换等算法把图像从空间域转化成频域，
# 也就是把图像矩阵转化成二维信号，进而使用高通滤波或低通滤波器对信号进行过滤。采用低通滤波器（即只让低频信号通过）法，
# 可去掉图中的噪声；采用高通滤波法，则可增强边缘等高频信号，使模糊的图片变得清晰。

# 2、空间域法方法用的比较多，主要包括以下几种常用的算法：（1）直方图均衡化 （2）滤波
# （1）直方图均衡化的作用是图像增强，这种方法对于背景和前景都太亮或者太暗的图像非常有用。直方图是一种统计方法，
# 根据对图像中每个像素值的概率进行统计，按照概率分布函数对图像的像素进行重新分配来达到图像拉伸的作用，
# 将图像像素值均匀分布在最小和最大像素级之间。用直白的语言来描述：把像素按从小到大排序，统计每个像素的概率和累计概率，
# 然后用灰度级乘以这个累计概率就是映射后新像素的像素值。

# 比如一个4*4的区域
# 50  20  90  120
# 20  40  50  50
# 255 255 50  20
# 50  40  50  50
# 利用直方图对像素分布进行统计：
# 像素值  像素个数  概率    累积概率     新像素值
# 20      3        0.1875  0.1875     47.8125
# 40      2        0.125   0.3125     79.6875
# 50     ...
# ...
# 255     2        0.125   1(上面总和) 255


# （2)基于滤波的算法主要用于图像去噪，见image_denoising.py

import cv2
from matplotlib import pyplot as plt


# 1.读取图像并转化为灰度图
img = cv2.imread("../data/2007_000793.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 2.显示灰度直方图
def histogram(gray):
    hist = cv2.calcHist([gray], [0], None, [256], [0.0, 255.0])
    plt.plot(range(len(hist)), hist)
    plt.show()
histogram(gray)

# 3.直方图均衡化
dst = cv2.equalizeHist(gray)
histogram(dst)

cv2.imshow("img", img)
cv2.imshow("histogram", dst)
cv2.waitKey()