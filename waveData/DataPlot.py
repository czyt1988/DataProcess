import os.path
from itertools import cycle
#----
import matplotlib.pyplot as plt  
from matplotlib.widgets import Cursor
from matplotlib import colors
from matplotlib import lines
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
#----
import numpy as np
#----
from waveData import Data
from czy import signal as czySignal
from waveData import detectPeaks as dp


LINE_STYLES = lines.lineStyles.keys()
LineCycler = cycle(LINE_STYLES)

LINE_MARKERS = []
for m in Line2D.markers:
    try:
        if m != ' ' and len(m)==1:
            LINE_MARKERS.append(m)
    except TypeError:
        pass
LineMarksCycler = cycle(LINE_MARKERS)

LINE_COLORS = ['b','g','r','c','m','k','y']
LineColorCycler = cycle(LINE_COLORS)

def plotWave(iWaveData,indexOrName,ax = None,color = 'r',**otherSet):
    '''绘制一个压力图形
    Args:L
        iWaveData:Data参数，需先加载一个csv参数
        indexOrName:int/str
            索引或者是通道名称，索引从0开始，通道名称为str类型
    Returns:
        [[x,y,otherInfo],[fig,ax]]
    '''
    y,otherInfo = getY(iWaveData,indexOrName)
    info = otherInfo[1]
    fig = None
    if ax is None:
        fig,ax = plt.subplots(1, 1, figsize=(8, 4))
    [x,[fig,ax]] = _plotWave(y,otherInfo[0],ax=ax,color=color)
    ax.set_xlabel("times(s)")
    ax.set_ylabel("pressure(KPa)")
    if 'title' in otherSet:
        ax.set_title(otherSet['title'])
    if not fig is None:
        fig.set_facecolor('w')
    return [[x,y,otherInfo],[fig,ax]]

def _plotWave(wave,fs,ax=None,color='r'):
    '''绘制一个压力图形
    Args:
        wave:numpy.array 波形
        fs:int 采样率
        ax:matplotlib.ax 绘图坐标系
        color:str or rgb 绘图颜色
    Returns:
        [x,[fig,ax]]:list
            x值，[fig,ax]
    '''
    x = czySignal.getXByFs(len(wave),fs)
    fig=None
    if ax is None:
        fig,ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(x,wave,color)
    ax.set_xlim([x[0],x[-1]])
    if not fig is None:
        fig.set_facecolor('w')
    return [x,[fig,ax]]

def plotSpectrum(iWaveData,indexOrName,ax = None,**otherSet):
    '''
    Args:
        iWaveData:data数据类型，包含多通道数据，以及数据的采样率
        indexOrName:int or string
            通道编号或者通道名称
        ax:matplotlib object
            绘图用坐标轴
        otherSet:
            fftN:int 
                fft的数量，-1为自动寻找下个2基，0为当前长度，其他为自定义
            scale:string
                幅值处理方式：amp幅值Amplitude,ampDB为幅值加上分贝,mag为幅度谱，只是对fft结果取模
            isShowPeaks:bool
                是否捕获峰值
            markPeaksNum:int
                标记峰值的点数目
            isShowPeaksNum:bool
                标记峰值的数字显示
            autoMarkType:string
                自动标记的类型，如果为'y'，表示标记y值，'x'表示标记x值，'xy'表示标记x，y值
    Returns:
        [[fre,mag,ppd],[fig,ax]]:list
            [[频率，幅值，峰值索引],[fig,ax]]
    '''
    x,y,otherInfo = getXY(iWaveData,indexOrName)
    fs = otherInfo[0]
    fftN = -1
    isShowPeaks = True
    markPeaksNum = 5
    scale = 'amp'
    autoMarkType = 'y'
    if 'fftN' in otherSet:
        fftN = otherSet['fftN']
    if 'isShowPeaks' in otherSet:
        isShowPeaks = otherSet['isShowPeaks']
    if 'markPeaksNum' in otherSet:
        markPeaksNum = otherSet['markPeaksNum']
    if 'scale' in otherSet:
        scale = otherSet['scale']
    if 'isShowPeaksNum' in otherSet:
        isShowPeaksNum = otherSet['isShowPeaksNum']
    if 'autoMarkType' in otherSet:
        autoMarkType = otherSet['autoMarkType']
    [[fre,mag,ppd],[fig,ax]] = _plotSpectrum(y,fs,ax
                                             ,fftN=fftN
                                             ,isShowPeaks=isShowPeaks
                                             ,markPeaksNum=markPeaksNum
                                             ,scale = scale
                                             ,**otherSet)
    if isShowPeaksNum:
        ppdShow = ppd[::-1][0:markPeaksNum if len(ppd)>markPeaksNum else len(ppd)]
        markPoints(ax,fre[ppdShow],mag[ppdShow],autoType=autoMarkType)
    return [[fre,mag,ppd],[fig,ax]]

def _plotSpectrum(wave,fs,ax=None,fftN = -1,isShowPeaks = True,markPeaksNum = 5,scale = 'amp',**otherSet):
    '''绘制频谱图
    Args:
        wave:numpy.array 
            波形
        fs:int 
            采样率
        ax:matplotlib object
            绘图用坐标轴
        fftN:int 
            fft的数量，-1为自动寻找下个2基，0为当前长度，其他为自定义
        isShowPeaks:bool
            是否捕获峰值
        scale:string
            幅值处理方式：amp幅值Amplitude,ampDB为幅值加上分贝,mag为幅度谱，只是对fft结果取模
        peaksMarkStyle:string
            标记极值点的样式，默认为'or'
    Returns:
        [[fre,mag,ppd],[fig,ax]]:list
            [[频率，幅值，峰值索引],[fig,ax]]
    '''
    ppd = None
    fig = None
    peaksMarkStyle = 'or'
    if 'peaksMarkStyle' in otherSet:
        markStyle = otherSet['peaksMarkStyle']
    fre,mag = czySignal.spectrum(wave,fs,fftN,1,scale)
    if ax is None:
        fig,ax = plt.subplots(1, 1, figsize=(8, 4))
        fig.set_facecolor('w')
    ax.plot(fre,mag,**otherSet)
    if isShowPeaks:
        if ppd is None:
            ppdShow = detectPeaks(mag,markPeaksNum)
            #ppd = dp.detectPeaks(mag,sorting = True,edge='falling')
            #ppdShow = ppd[0:markPeaksNum if len(ppd)>markPeaksNum else len(ppd)]
        ax.plot(fre[ppdShow],mag[ppdShow],peaksMarkStyle)
    return [[fre,mag,ppd],[fig,ax]]

def plotWaveAndSpectrum(iWaveData,indexOrName,ax = None,**otherSet):
    '''
    @brief 绘制一个波形和频谱
    @iData Data参数，需先加载一个csv参数
    @indexOrName 索引或者是通道名称，索引从0开始，通道名称为str类型
    ---
    'rc':(2,1) subplot的分解，默认为2,1，可以设置为1,2
    'title':[str] 标题
    'isDetectPeaks':True/False 是否显示峰值
    'isShowPeaks':True/False 是否显示峰值
    ''' 
    rc = (2,1)
    if 'rc' in otherSet:
        rc = otherSet['rc']
    fig = None
    if ax is None:
        fig,ax = plt.subplots(rc[0],rc[1], figsize=(8, 6))
    ax1 = ax[0]
    [[x,y,otherInfo],_] = plotWave(iWaveData,indexOrName,ax1)
    fs = otherInfo[0]
    info = otherInfo[1]
    if 'title1' in otherSet:
        ax1.set_title(otherSet['title1'])
    #----------------------------------------
    ax2 = ax[1]
    [[fre,mag,ppd],_] = _plotSpectrum(y,fs,ax2)
    ax2.set_xlabel("frequency(Hz)")
    ax2.set_ylabel("amplitude(KPa)")   
    #----------------------------------------
    if not ax is None:
        fig.set_facecolor('w')
    #Cursor(plt.gca(), horizOn=False, color='r', lw=1) #horizOn=True时，两个坐标都有显示光标   
    return [[x,y,fre,mag,ppd],[fig,ax]]

def getXY(iWaveData,indexOrName):
    '''获取x，y值
    Args:
        Data:int
            参数，需先加载一个csv参数
        indexOrName:int/str
            索引或者是通道名称，索引从0开始，通道名称为str类型
    Returns:
        (x,y,otherInfo):tuple
            x值，y值，和附加信息
    '''
    y = getY(iWaveData,indexOrName)
    otherInfo = getDatasInfo(iWaveData)
    fs = otherInfo[0]
    x = czySignal.getXByFs(len(y),fs)
    return (x,y,otherInfo)

def getX(iWaveData):
    '''获取x值
    Args:
        iWaveData : IData
            数据接口,Data参数，需先加载一个csv参数
    Return: x list like 获取的x值
    '''
    r = iWaveData.rowCount[1]
    otherInfo = getDatasInfo(iWaveData)
    fs = otherInfo[0]
    x = czySignal.getXByFs(r,fs)
    return x

def getY(iWaveData,indexOrName):
    '''获取y值
    Args:
        iWaveData : IData
            数据接口,Data参数，需先加载一个csv参数
        indexOrName:int/str
            索引或者是通道名称，索引从0开始，通道名称为str类型
    Return: y list like 获取的y值
    '''
    y = np.array(float)
    if isDigit(indexOrName):
        y = iWaveData.datas[indexOrName]
    else:
        if indexOrName in iWaveData.names:
            index = iWaveData.names.index(indexOrName)
            y = iWaveData.datas[index]
    return y

def getDatasInfo(iWaveData):
    '''获取文件的信息
    Args:
        iWaveData : IData
            数据接口
    Return:
        info : list
            info列表，第一项为fs，第二项为info
    '''
    try:
        fs = float(iWaveData.fs)
    except ValueError:
        print('文件读取异常，采样率（row:0,column:3）因为浮点型数据，请更正')
    info = [fs,iWaveData.getInfo()]
    return info

def isDigit(my_str):
    try:
        int(my_str)
    except ValueError:
        return False
    return True

def makeSubPlot(row,colum,datas,x=None,xs = None,titles = None,figsize=(8, 4),colors = None,isSameColor = False):
    """绘制多个子图
    Args:
    row: int
        绘制子图的分割行数
    column: int
        绘制子图分割的列数
    x: array_like
        x轴的值 所有子图公用一个x轴值,如果x是不同值，可以设置xs
    xs: list
        每个subplot的x值，如果公用一个x轴值,可以设置x，若都不设置，自动从1递增
    datas: list
        y轴的值，datas的长度不超过row*column
    titles: list
        给每个图添加的标题


    """
    fig,axs = plt.subplots(row,colum,figsize=figsize)
    if isSameColor:
        sameclr = next(LineColorCycler)
    index = 0
    for r in range(0,row):
        for c in range(0,colum):
            print(next(LineColorCycler))
            if index < len(datas):
                xData = list(range(1,len(datas[index])+1))
                if not x is None:
                    xData = x
                elif not xs is None:
                    xData = xs[index]
                axs[r][c].plot(xData,datas[index]
                        ,color = sameclr if isSameColor else next(LineColorCycler))
                if not titles is None:
                    axs[r][c].set_title(titles[index])
            else:
                break
            index+=1
    fig.set_facecolor('w')
    

def _plot3(x,y,z,ax=None,fig=None,color = None):
    if ax is None:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
    if color is None:
        ax.plot(x,y,z)
    else:
        ax.plot(x,y,z,color=color)
    return [fig,ax]

def _plotWaterFall(xs,ys,orders=None,ax=None,fig=None,isShow = False,edgecolors = None,facecolors = None):
    '''绘制瀑布图
    Args:
        x: list
            x轴数据list,，每个元素是需要绘制的x轴数据
        y: list
            y轴数据list,，每个元素是需要绘制的y轴数据
        order: list
            每个x,y对应的序号,如果设置，从1开始自增到len(x)
    Return:
        [fig,ax] : list
            返回fig和ax，若指定，返回原样，若没指定将生成新的
    '''
    if ax is None:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
    #if orders is None:
    #    orders = range(1,min([len(xs),len(ys)])+1)
    #for index,yy in enumerate(y):
    #    ys = np.ones(len(x))*yy
    #    if color is None:
    #        _plot3(x,ys,z[index],ax = ax,fig = fig)
    #    elif color is list:
    #        _plot3(x,ys,z[index],ax = ax,fig = fig,color = color[index])
    #    else:
    #        _plot3(x,ys,z[index],ax = ax,fig = fig,color = color)
    if orders is None:
        orders = range(1,min([len(xs),len(ys)])+1)
    verts = []



    for i,z in enumerate(orders):
        verts.append(list(zip(xs[i], ys[i])))

    if facecolors is None:
        facecolors = []
        for z in orders:
            facecolors.append(colorConverter.to_rgba('r',alpha=0.5))
    if edgecolors is None:
        edgecolors = []
        for z in orders:
            edgecolors.append(colorConverter.to_rgba('r',alpha=0.8))

    poly = PolyCollection(verts,edgecolors=edgecolors, facecolors=facecolors)
    poly.set_alpha(0.5)

    minxs = np.min(list(map(np.min,xs)))
    maxxs = np.max(list(map(np.max,xs)))
    minys = np.min(list(map(np.min,ys)))
    maxys = np.max(list(map(np.max,ys)))
    ax.add_collection3d(poly, zs=orders, zdir='y')
    ax.set_xlim3d(minxs,maxxs)
    ax.set_ylim3d(np.min(orders),np.max(orders))
    ax.set_zlim3d(minys,maxys)
    if isShow:
        plt.show()
        
    return [fig,ax]

def plotSpectrumWaterFall(iWaveData,ax = None,isShow = False,edgecolors = None,facecolors = None):
    z = iWaveData.datas
    fs = getDatasInfo(iWaveData)[0]
    z = list(map(lambda d:czySignal.spectrum(d,fs),z))
    x = list(map(lambda d:d[0],z))#把频率提取出来
    z = list(map(lambda d:d[1],z))#把幅值提取出来
    [fig,ax] = _plotWaterFall(x,z,edgecolors = edgecolors,facecolors=facecolors)
    if isShow:
        plt.show()
    return [fig,ax]

def plotTrend(xdatas,ydatas,names,ax = None,isShow = False):
    '''绘制趋势图
        趋势图是指数据量不大，用于显示趋势的图形
    Args:
        datas:list
            数据，多个列表则绘制多个对比图
        names:list/str
            每个图形对应的名字
        ax:matplotlib.ax
        isShow:bool
            是否显示图形
    Returns
    '''
    if ax is None:
        fig,ax = plt.subplots(1, 1, figsize=(8, 4))
    for i,y in enumerate(ydatas):
        ax.plot(xdatas[i],y,color=next(LineColorCycler),)
    fig.set_facecolor('w')
    if isShow:
        plt.show()

def markPoints(ax,xs,ys,text=None,autoType='y'):
    '''
    标记数据在图表上
    Args
        ax:matplotlib->axes
            坐标系
        xs:list
            要标记数据的x值
        ys:list
            要标记数据的y值
        text:list
            要标记数据的内容，如果没有，则标记数据的x,y或者x，或者y，具体由autoType控制
        autoType:string
            自动标记的类型，如果为y，表示标记y值，x表示标记x值，xy表示标记x，y值        
    '''
    for (x,y) in zip(xs,ys):
        if autoType == 'y':
            label = '%g'%(y)
        elif autoType == 'x':
            label = '%g'%(x)
        else:
            label = '%g,%g'%(x,y)
        ax.annotate(label,xy=(x,y),xycoords='data'
            ,xytext=(-20, 20), textcoords='offset points'
            ,arrowprops=dict(arrowstyle="->"))
    
def detectPeaks(data,peakNums = 10,mpd = 1,sorting = True,edge = 'falling'):
    '''
    获取峰值，默认降序，投一个为最大的峰值索引
    Args:
        data:
            数据
        peakNums:int
            要获取的峰值数量，default:10
        mpd:int
            positive integer, optional (default = 1)
            detect peaks that are at least separated by minimum peak distance (in
            number of data).
        sorting:bool
            是否排序，默认为True
        edge:string
            排序方式，默认为falling，可以为{None, 'rising', 'falling', 'both'}, 
            for a flat peak, keep only the rising edge ('rising'), only the
            falling edge ('falling'), both edges ('both'), or don't detect a
            flat peak (None).

    '''
    ppd = dp.detectPeaks(data,mpd = mpd,sorting = sorting,edge=edge)
    return ppd[0:peakNums if len(ppd)>peakNums else len(ppd)]
