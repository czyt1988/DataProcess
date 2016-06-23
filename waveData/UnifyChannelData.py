import os.path
from waveData import Data 
import csv


class UnifyChannelData(object):
    """用于统一不同数据的类
    数据都基于Data.ChannelData
    Namespace:
        UnifyChannelData.UnifyChannelData 
    """

    def __init__(self,IChannelData):
        self.__pData = IChannelData
   
    def saveStandardCSVDataFile(self,filePath):
        with open(filePath,'w',encoding='gbk',newline='') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            #第一行写入文件 辨别码,信息,采样率
            wr.writerow([1234567890,self.__pData.getInfo(),self.__pData.fs])
            #第二行写入表头
            wr.writerow(self.__pData.names)
            #后面开始写入数据
            for i in range(0,self.__pData.rowCount[1]):
                wr.writerow(self.__pData.getRowData(i))

def unifySimulatedPressureData(simulatedDataFolder,unifyDataPath,fs = 200,info = ''):
    '''
    @brief 统一模拟文件为标准数据文件
    @param simulatedDataFolder 模拟数据的文件夹
    @param unifyDataPath 统一标准后的文件位置
    '''
    simData = Data.PressureDataForSimulated()
    simData.loadData(simulatedDataFolder)
    if 0 == simData.rowCount:
        return False
    simData.fs = fs
    simData.setInfo(info)
    upd = UnifyChannelData(simData)
    upd.saveStandardCSVDataFile(unifyDataPath)
    return True

def unifyExprementPressureData(exprementPressureDataPath,unifyDataPath,fs = 100,info = ''):
    '''
    @brief 统一实验文件为标准数据文件
    @param exprementPressureDataPath 实验数据的文件位置
    @param unifyDataPath 统一标准后的文件位置
    '''
    expData = Data.PressureDataForExperiment()
    expData.loadData(exprementPressureDataPath)
    if 0 == expData.rowCount:
        return False
    expData.fs = fs
    expData.setInfo(info)
    upd = UnifyChannelData(expData)
    upd.saveStandardCSVDataFile(unifyDataPath)
    return True

