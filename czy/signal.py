import numpy as np
import math


def spectrum(datas,fs,fftSize = -1,fftType=1,scale='amp',isDetrend = True):
    """频谱分析
    Args:
    datas: 原始波形
    fs: 采样率
    fftSize:int 
        fft的长度，0 or -1 or int size -1为自动延拓，0为不指定长度由自身长度决定
    fftType:int
        fft类型，0 or 1 0为fft，1为rfft
    isDetrend:bool
        是否对信号进行去均值处理
    scale:string
        幅值处理方式：amp幅值Amplitude,ampDB为幅值加上分贝,mag为幅度谱，只是对fft结果取模，
    Return:
        (freqs,y):(nump.array,nump.array) 频率序列，幅值序列
    """
    if isDetrend:
        datas = datas - np.mean(datas)

    if 0 == fftSize:
        fftSize = len(datas)
    elif fftSize<0:
        fftSize = nextpow2(len(datas))


    if 0 == fftType:
        y = np.fft.fft(datas,fftSize)
        y = y[0:len(y)/2]
    else:
        y = np.fft.rfft(datas,fftSize)

    amp = dealFFTMagnitude(y,scale,fftSize)
    freqs = dealFFTFrequency(fs,fftSize)
    return (freqs,amp)

def dealFFTMagnitude(mag,scale='amp',fftSize=0):
    """fft之后的幅值处理
    Args:
    mag: fft之后的波形
    scale:string
        幅值处理方式：amp幅值Amplitude,ampDB为幅值加上分贝,mag为幅度谱，只是对fft结果取模，
    Return:
    """
    
    if 0 == fftSize:
        fftSize = len(mag)
    elif fftSize<0:
        fftSize = nextpow2(len(mag))
    temp = 2/fftSize;
    spectrumSize = int(fftSize/2);
    endIndex = spectrumSize - 1;
    amp = np.zeros(spectrumSize)
    scale = scale.lower()
    if scale == 'amp':
        amp[0] = np.abs(mag[0])/fftSize
        amp[endIndex] = np.abs(mag[endIndex])/fftSize
        amp[1:endIndex] = np.abs(mag[1:endIndex])*temp
    elif scale == 'ampdb':
        amp[0] = np.abs(mag[0])/fftSize
        amp[endIndex] = np.abs(mag[endIndex])/fftSize
        amp[1:endIndex] = np.abs(mag[1:endIndex])*temp
        amp = 20*np.log10(np.clip(np.abs(amp), 1e-20, 1e100))
    elif scale == 'mag':
        amp = np.abs(mag[0:endIndex+1])
    else:
        raise ValueError('scale=\'amp\' or \'ampdb\' or \'mag\' ')
    return amp

def dealFFTFrequency(fs,fftSize):
    """根据采样率和fft的数目计算频率分布
    Args:
        fs: 采样率
        fftSize:傅里叶变换长度
    Return:
        计算得到的频率分布np.array like
    """
    freqs = np.linspace(0,fftSize/2-1,fftSize/2)*(fs/fftSize)
    return freqs

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
    根据采样率和波形长度，获取波形的x轴
    Args:
        waveLength 波形数据的长度
        fs 采样率
    Returns:
        x:numpy.array like
    '''
    detalT = 1.0/fs
    x = np.linspace(0,(waveLength-1)*detalT,waveLength)
    return x