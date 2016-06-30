
#waveData 通用包，波形数据分析
##DataPlot 数据绘制

### _plotWave 绘制波形
	只需要一个wave数据，和采样率即可绘制波形
    Args:
        wave:numpy.array 波形
        fs:int 采样率
        ax:matplotlib.ax 绘图坐标系
        color:str or rgb 绘图颜色
        **kwargs:matplotlib.axes.plot的**kwargs参数
    Returns:
        [x,[fig,ax]]:list
            x值，[fig,ax]
例如：
```Python
print('_plotWave example')
fs = 10
wave = [1,2,3,5,1,2,4,7,4,6,7,3,2,4,6,8,9,7,6,5,4,2,4,7]
dp._plotWave(wave,fs)
plt.show()
```
![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/06-_plotWave.png)


### plotWave  绘制一个波形 _plotWave的封装，适用IData数据
绘制一个压力图形
    Args:L
        iWaveData:Data参数，需先加载一个csv参数
        indexOrName:int/str
            索引或者是通道名称，索引从0开始，通道名称为str类型

    Returns:
        [[x,y,otherInfo],[fig,ax]]



### _plotWaterFall 绘制频谱

Args:
    x: list
        x轴数据list,，每个元素是需要绘制的x轴数据
    y: list
        y轴数据list,，每个元素是需要绘制的y轴数据,
        ！！注意：这里的y，会以z轴绘制
    type:string
        type = 'line'以曲线形式绘制waterfall，type='poly'或者非line，以填充形状形式绘制
    fig: matplotLib.figure
        绘图容器，若传入，而没有ax，会以它生成ax
    ax:
        坐标系，默认为None,会自动生成
    order: list
        每个x,y对应的序号,如果设置，从1开始自增到len(x)
    edgecolors:
        边界线颜色
        (0,0,0,0):int,int,int,int:R,G,B,A
    facecolors:
        填充颜色
        (0,0,0,0):int,int,int,int:R,G,B,A
	sameColor:
        设置在type='line'时，颜色一致
        (0,0,0,0):int,int,int,int:R,G,B,A
Return:
    [fig,ax] : list
        返回fig和ax，若指定，返回原样，若没指定将生成新的
type = 'line'模式：

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/01-_plotWaterFall-type-poly.png)

type = 'poly'模式：

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/02-_plotWaterFall-type-line.png)

type = 'line',sameColor='r' 模式：

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/03-_plotWaterFall-type-line-sameColor.png)


### plotSpectrum

进行时频分析STFT,与matplotlib.plt.spectrum接口一致，但是，幅值处理有amplitude，通过mode设置，如：

dp.plotSpectrum(wave,Fs = fs,detrend = 'mean'
,NFFT = NFFTSize,noverlap=int(NFFTSize/4),mode='amplitude'
,plotType = 'other',scale='linear',sameColor='r')
![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/04-plotSpectrum.png)

plotType = '3d'时，将以线的方式绘制

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/05-plotSpectrum-3d.png)