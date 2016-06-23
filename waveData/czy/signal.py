import numpy as np
import math


def spectrum(datas,fs,fftSize = -1,fftType=1,scale='mag'):
    """
    @brief 频谱分析
    @param datas 原始波形
    @param fs 采样率
    @param OtherSet 其他设置
    'fftSize':0 or -1 or int size -1为自动延拓，0为不指定长度由自身长度决定
    'fftType':0 or 1 0为fft，1为rfft
    @return (freqs,y) (nump.array,nump.array) 频率序列，幅值序列
    """
    #fftSize = -1#-1为自动延拓，0为不指定长度由自身长度决定
    #fftType = 1#0为fft，1为rfft
    #scale='mag'#mag用正常幅值，db用分贝
    #if 'fftSize' in OtherSet:
    #    fftSize = OtherSet['fftSize']
    #if 'fftType' in OtherSet:
    #    fftType = OtherSet['fftType']
    #if 'scale' in OtherSet:
    #    scale = OtherSet['scale']
    if 0 == fftSize:
        fftSize = len(datas)
        if 0 == fftType:
            y = np.fft.fft(datas)
            y = y[0:len(y)/2]
        else:
            y = np.fft.rfft(datas)
    elif -1 == fftSize:
        fftSize = nextpow2(len(datas))
        if 0 == fftType:
            y = np.fft.fft(datas,fftSize)
            y = y[0:len(y)/2]
        else:
            y = np.fft.rfft(datas,fftSize)
    else:
        if 0 == fftType:
            y = np.fft.fft(datas,fftSize)
            y = y[0:len(y)/2]
        else:
            y = np.fft.rfft(datas,fftSize)
    if scale.lower() == 'db':
        y = 20*np.log10(np.clip(np.abs(y), 1e-20, 1e100))
    else:
        y /= len(datas)
    y = np.abs(y)
    if 0 == fftType:
        freqs = np.linspace(0, fs/2, fftSize/2)
    else:
        freqs = np.linspace(0, fs/2, fftSize/2+1)

    return (freqs,y)

def nextpow2(i):
    """
    @brief Find 2^n that is equal to or greater than.
    @param i [int] 数据长度
    @return 返回i长度的下个2**n次的n
    """
    n = 1
    while n < i: n *= 2
    return n

def getXByFs(waveLength,fs):
    '''
    @breif 根据采样率和波形，获取x轴值
    @param waveLength int 波形长度
    @param fs int 采样率
    '''
    detalT = 1.0/fs
    x = np.linspace(0,(waveLength-1)*detalT,waveLength)
    return x