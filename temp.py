# -*- coding: utf-8 -*-
import os.path
#from pressureData import UnifyPressureData
from waveData import Data as pd
from waveData import DataPlot as dp
import numpy as np
import matplotlib.pyplot as plt  
from czy import signal as czySignal

'''
d:/cloudDisk/share/python/北区第一次实验数据分析/
d:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析/
'''
FILE_FOLDER = 'd:/cloudDisk/share/python/北区第一次实验数据分析/'
FILE_NAME = '25m单容错位-开口-1.csv'
FILE_PATH = os.path.join(FILE_FOLDER,FILE_NAME)
pressuresData = pd.loadData(FILE_PATH)#加载文件
fs = pressuresData.fs#采样率
wave = pressuresData.datas[0]
dataSize = len(wave)
NFFTSize = 512 if int(dataSize/20)>512 else int(dataSize/20)#相关分析进行频谱的阶段长度

dp.plotSpectrum(wave,Fs = fs,detrend = 'mean',NFFT = NFFTSize,noverlap=int(NFFTSize/4),mode='amplitude')
plt.show()
