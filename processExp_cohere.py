'''
此文件主要进行试验采集的通道数据进行频域相关分析
- 对应目标 实验数据
- #注意#
    数据需要有一个放空数据作为基准对比
- FILE_FOLDER 数据文件夹
- FILE_NAME 数据名
- CHANNEL_NUM 通道号，如果通道小于0，进行全局分析
- SHOW_TITLE 显示标题，以文件名作为标题(不带后缀)
- SHOW_AXIS_TEXT 坐标轴label
- MARK_MAX 标记最大值
'''
import os.path
from waveData import Data as pd
from waveData import DataPlot as dp
import numpy as np
import matplotlib.pyplot as plt  
import matplotlib.mlab as mlab
from czy import signal as czySignal

'''
d:/cloudDisk/share/python/北区第一次实验数据分析/
d:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析/
'''
FILE_FOLDER = 'd:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析/'
FILE_NAME = '25m单容错位-开口-1.csv'
CHANNEL_NUM = -1#定义需要观察的通道数
SHOW_TITLE = True#是否显示标题
SHOW_AXIS_TEXT = True#是否显示坐标轴标题
MARK_MAX = True#标记最大值


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei','SimHei','Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

FILE_PATH = os.path.join(FILE_FOLDER,FILE_NAME)
pressuresData = pd.loadData(FILE_PATH)#加载文件
fs = pressuresData.fs#采样率
colCount = pressuresData.columnCount#通道数
channelEnd = pressuresData.getColumnData(colCount-1)#放空通道
dataSize = 8192 if 8192 < len(channelEnd) else len(channelEnd)#数据长度
cohereNFFTSize = 512 if int(dataSize/20)>512 else int(dataSize/20)#相关分析进行频谱的阶段长度
channelEnd = channelEnd[0:dataSize]
print('数据点数%d\n相关分析的点数:%d'%(dataSize,cohereNFFTSize))
titleText =  FILE_NAME.split('.')[0:-1]

if CHANNEL_NUM<0:#通道数如果小于0，就进行全局分析
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    maxCxyIndexs = []
    maxCxy = []
    maxFre = []
    for i in range(1,colCount-1):
        channelN = pressuresData.getColumnData(i)[0:dataSize]
        print('读取通道%d'%(i))
        cxy,f = mlab.cohere(channelN,channelEnd,NFFT = cohereNFFTSize,Fs = fs,detrend='mean')
        ax.plot(f,np.ones(len(f))*i,cxy)#绘制3d的相关系数
        maxCxyIndexs.append( np.argmax(cxy) )
        maxCxy.append(cxy[maxCxyIndexs[-1]])
        maxFre.append(f[maxCxyIndexs[-1]])
    #标记最大
    if MARK_MAX:
        ax.plot(maxFre,range(1,colCount-1),maxCxy,'o')
    if SHOW_AXIS_TEXT:
        ax.set_xlabel('frequency(Hz)')
        ax.set_ylabel('channel nums')
        ax.set_zlabel('coherence')
    plt.subplots_adjust(hspace=0.31)#水平间距
    plt.title(titleText)
else:#对特定通道进行分析
    channelN = pressuresData.getColumnData(CHANNEL_NUM)[0:dataSize]
    plt.subplots_adjust(wspace=0.5)
    x = czySignal.getXByFs(dataSize,fs)
    print('进行%d通道相关分析'%(CHANNEL_NUM))
    plt.subplot(211)
    plt.plot(x,channelN,'r')
    plt.plot(x,channelEnd,'b')
    if SHOW_AXIS_TEXT:
        plt.xlabel('times(s)')
        plt.ylabel('amplitude')
    if SHOW_TITLE:
        plt.title(titleText)

    plt.subplot(212)
    cxy,f = plt.cohere(channelN,channelEnd,NFFT = cohereNFFTSize,Fs = fs,detrend='mean')
    if MARK_MAX:
        index = np.argmax(cxy)
        plt.plot(f[index],cxy[index],'o')
    if SHOW_AXIS_TEXT:
        plt.xlabel('frequency(Hz)')
        plt.ylabel('coherence')
    

plt.gcf().set_facecolor('w')
plt.show()

