#说明
这是为我girlfriend博士期间处理数据写的代码

#设计的内容
主要涉及以下内容
- 简单的信号处理(直接的频谱分析，时频分析等)
- 气流脉动的计算

#主要功能看我女友大神的要求

#功能说明
##czy 通用包
-signal 信号处理相关

###signal
- spectrum 频谱分析
- dealFFTMagnitude fft之后的幅值处理
- dealFFTFrequency 根据采样率和fft的数目计算频率分布
- nextpow2 Find 2^n that is equal to or greater than.
- getXByFs 根据采样率和波形长度，获取波形的x轴

#processExp_cohere.py - 信号相干性分析
此文件主要进行试验采集的通道数据进行频域相关分析
- 对应目标 实验数据
- #注意#
    数据需要有一个放空数据作为基准对比
- FILE_FOLDER 数据文件夹
- FILE_NAME 数据名
- CHANNEL_NUM 通道号，如果通道小于0，进行全局分析
- SHOW_TITLE 显示标题，以文件名作为标题(不带后缀)
- SHOW_AXIS_TEXT 坐标轴label
如：
两列信号的在频域上的相关分析

![](https://github.com/czyt1988/DataProcess/raw/master/doc/processExp_cohere/00.png)

![](https://github.com/czyt1988/DataProcess/raw/master/doc/processExp_cohere/01.png)

可以对多个信号进行相关分析，得到三维图:

![](https://github.com/czyt1988/DataProcess/raw/master/doc/processExp_cohere/03.png)
