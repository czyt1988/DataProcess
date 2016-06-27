
#waveData 通用包，波形数据分析
##DataPlot 数据绘制
- _plotWaterFall 绘制频谱
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

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/01-_plotWaterFall-type-line.png)

type = 'poly'模式：

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/02-_plotWaterFall-type-poly.png)

type = 'line',sameColor='r' 模式：

![](https://github.com/czyt1988/DataProcess/raw/master/waveData/doc/DataPlot/03-_plotWaterFall-type-line-sameColor.png)
