# -*- coding: utf-8 -*-
import os.path
#from pressureData import UnifyPressureData
from waveData import Data as pd
from waveData import DataPlot as dp
import numpy as np
import matplotlib.pyplot as plt  

'''
d:/cloudDisk/share/python/北区第一次实验数据分析/
d:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析/25m单容错位-开口-1.csv
'''
pressuresData = pd.loadData('d:/cloudDisk/share/python/北区第一次实验数据分析/25m单容错位-开口-1.csv')
fs = pressuresData.fs
fig,ax = plt.subplots()
fig.set_facecolor('w')
r = dp.plotSpectrum(pressuresData,1,ax)
ppd = r[0][2]
print(ppd)
plt.show()

