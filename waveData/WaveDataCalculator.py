
import numpy as np
class DatasCalculator(object):
    """
    @brief 用于统一计算的类
    数据都基于PressureData.IPressureData

    @namespace WaveDataCalculator.WaveDataCalculator 
    """

    def __init__(self,DataList):
        self.__pData = DataList
        self.__calcData = dict()
   
    def setCalculator(self,name,function):
        '''
        @brief 设置计算器，计算的结果可以用getResult获取
        '''
        self.__calcData[name] = map(function,self.__pData)

    def getResult(self,name,conver = True):
        '''
        @brief 获得计算的参数
        @param name str 名称
        @param conver bool 是否预先转换为list
        @return map object 返回一个map对象，用迭代器遍历，或者直接转换为list
        '''
        return list(self.__calcData[name]) if conver else self.__calcData[name]

class PressureDatasCalculator(DatasCalculator):
    def __init__(self,IPressureData):
        super().__init__(IPressureData.datas)
        super().setCalculator('mean',np.mean)
        super().setCalculator('var',np.var)
        super().setCalculator('std',np.var)
        super().setCalculator('max',np.max)
        super().setCalculator('min',np.min)
        super().setCalculator('argmax',np.argmax)
        super().setCalculator('argmin',np.argmin)
        super().setCalculator('ptp',np.ptp)
        super().setCalculator('median',np.median)


#import os.path
#import PressureData
#ROOT_SHARE_PATH = 'd:/netDisk/sharebox/15001395919@163.com/PIV实验台协同目录/数据处理-综合数据分析/北区实验新/统一格式'
##ROOT_SHARE_PATH = 'X:/PIV实验台协同目录/数据处理-综合数据分析/北区实验新/统一格式'#新笔记本
##ROOT_SHARE_PATH = 'D:/快盘/PIV实验台协同目录/数据处理-综合数据分析/北区实验新/统一格式'#旧笔记本
#FILE_PATH = '罐体长1米.csv'
#filePath = os.path.join(ROOT_SHARE_PATH,FILE_PATH)
#pds = PressureData.PressureDataForStandard()
#pds.loadData(filePath)
#wdc = PressureDatasCalculator(pds)
