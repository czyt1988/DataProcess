'''
论文绘图用文件
变量：
- DATA_FOLDER:string
    数据文件夹
- DATA_NAME:string
    数据名

- plotMassFlow
    绘制质量流量的波形和频谱
- loadData
    根据标示dataType来加载数据，返回IData类型
- plotWaterFallOneData
    绘制一个图形的瀑布图
'''

import os.path
#from pressureData import UnifyPressureData
from waveData import Data as pd
from waveData import DataPlot as dp
import numpy as np
import matplotlib.pyplot as plt  

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei','SimHei','Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

def plotMassFlow(massflowDataPath = 'd:/netDisk/sharebox/15001395919@163.com/PIV实验台协同目录/mass_flow_0.1478_NorthZone.txt'):
    """绘制质量流量波形和频谱

    Args:
        massflowDataPath: str
            质量流量文件的路径
    Return:
        [fig,ax]
    """
    t = np.genfromtxt(massflowDataPath,usecols=(0),delimiter=',')
    d = np.genfromtxt(massflowDataPath,usecols=(1),delimiter=',')
    fs = 1.0/(t[1]-t[0])
    fig,ax = plt.subplots(1,2,figsize=(10,5))
    dp._plotWave(d,fs,ax = ax[0])
    ax[0].set_xlim(0,1)
    ax[0].set_xlabel('Time(s)')
    ax[0].set_ylabel('Mass flow rate(kg/s)')
    #----------------------------------
    dp._plotSpectrum(d,fs,ax = ax[1],isShowPeaks=False)
    ax[1].set_xlim(0,100)
    ax[1].set_xlabel('Frequency(Hz)')
    ax[1].set_ylabel('Amplitude(kg/s)')
    fig.set_facecolor('w')
    plt.show()
    return [fig,ax]

def loadData(path,dataType = 'std'):
    if dataType == 'sim':#模拟值
        data = pd.PressureDataForSimulated()
        data.loadData(path)
    elif dataType == 'exp':
        data = pd.PressureDataForExperiment()
        data.loadData(path)
    elif 'std':
        data = pd.PressureDataForStandard()
        data.loadData(path)
    return data

def plotWaterFallOneData(dataPath,dataType,pdData=None,edgecolors = None,facecolors = None,color = 'r',scale='amp',type = 'line',**otherSet):
    if pdData is None:
        pdData = loadData(dataPath,dataType)
    [fig,ax]=dp.plotSpectrumWaterFall(pdData,edgecolors=edgecolors,
                    facecolors=facecolors,scale=scale,type=type,**otherSet)
    plt.show()
    
#绘制质量流量的波形及频谱
#plotMassFlow('X:/PIV实验台协同目录/mass_flow_0.1478_NorthZone.txt')

#绘制某个文件的频谱瀑布图
DATA_FOLDER = 'd:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析/'
DATA_NAME = '25m单容错位-开口-1.csv'

DATA_PATH = os.path.join(DATA_FOLDER,DATA_NAME)
plotWaterFallOneData(DATA_PATH,'std',type='poly',scale='amp',sameColor='r')

