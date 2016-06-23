import os.path
#from pressureData import UnifyPressureData
from waveData import Data as pd
from waveData import DataPlot as dp
import numpy as np
import matplotlib.pyplot as plt  
plt.rcParams['font.sans-serif'] = ['SimHei']
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

def plotWaterFallOneData(dataPath,dataType,pdData=None,color = 'r'):
    if pdData is None:
        pdData = loadData(dataPath,dataType)
    [fig,ax]=dp.plotSpectrumWaterFall(pdData)

    plt.show()
    
#绘制质量流量的波形及频谱
#plotMassFlow('X:/PIV实验台协同目录/mass_flow_0.1478_NorthZone.txt')

#绘制某个文件的频谱瀑布图
plotWaterFallOneData('D:/快盘/PIV实验台协同目录/python/统一格式数据/实验/双容间距0.5m.csv'
                     ,'std')

