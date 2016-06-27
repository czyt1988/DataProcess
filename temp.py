# -*- coding: utf-8 -*-
import os.path
#from pressureData import UnifyPressureData
from waveData import Data as pd
from waveData import DataPlot as dp
import numpy as np
import matplotlib.pyplot as plt  
from czy import signal as czySignal

a = [12,21,32,43,15,36]
print(np.argmax(a))