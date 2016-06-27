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
d:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析/25m单容错位-开口-1.csv
'''
pressuresData = pd.loadData('d:/cloudDisk/share/python/北区第一次实验数据分析/25m单容错位-开口-1.csv')
colCount = pressuresData.columnCount
channelEnd = pressuresData.getColumnData(colCount-1)
channelN = pressuresData.getColumnData(0)
fs = pressuresData.fs
dataSize = 8192 if 8192 < len(channelEnd) else len(channelEnd)
channelEnd = channelEnd[0:dataSize]
channelN = channelN[0:dataSize]
print('fs :%d'%(fs))
print('nfft size:%d'%(dataSize))

# make a little extra space between the subplots
plt.subplots_adjust(wspace=0.5)
x = czySignal.getXByFs(dataSize,fs)
print('x:%d'%(len(x)))
plt.subplot(211)
plt.plot(x,channelN,'r')
plt.plot(x,channelEnd,'b')

plt.subplot(212)
cohereNFFTSize = int(dataSize/20)
cxy, f = plt.cohere(channelN,channelEnd,NFFT = cohereNFFTSize,Fs = fs,detrend='mean')


#fig,ax = plt.subplots()
#fig.set_facecolor('w')
#r = dp.plotSpectrum(pressuresData,1,ax,scale='amp',isShowPeaksNum=True,)
print('show')
plt.show()
