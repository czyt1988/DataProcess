from abc import *

import os
import os.path
import csv

import xlrd

import numpy as np


class IChannelData(object):
    """
    @brief 定义获取压力数据的接口
    """
    __metaclass__ = ABCMeta #指定这是一个抽象类
       
    @abstractmethod  
    def getRowCount(self):
        """
        @brief 获取数据的行数
        """
        pass

    
    @abstractmethod  
    def getColumnCount(self):
        """
        @brief 获取数据的列数
        """
        pass

    
    @abstractmethod  
    def getInfo(self):
        """
        @brief 获取数据的说明
        """
        pass
    @abstractmethod  
    def setInfo(self,info):
        """
        @brief 设置数据的说明
        """
        pass

    @abstractmethod  
    def getRowData(self,row):
        """
        @brief 获取一行数据
        """
        pass
    @abstractmethod  
    def getColumnData(self,col):
        """
        @brief 获取一列数据
        """
        pass

    @abstractproperty
    def rowCount(self):
        '''
        @brief 获取函数，为一个list包含2个，一个最小值和一个最大值
        '''
        pass

    @abstractproperty
    def columnCount(self):
        pass

    
    @abstractproperty  
    def datas(self):
        """
        @brief 获取所有数据
        """
        pass
    
    @abstractproperty  
    def names(self):
        """
        @brief 获取所有数据的names
        """
        pass

    @abstractproperty  
    def fs(self):
        pass

class BaseChannelData(IChannelData):
    '''
    @brief 基本压力数据接口
    '''
    __metaclass__ = ABCMeta #指定这是一个抽象类

    def __init__(self):
        self.clearValue()

    def clearValue(self):
        self.__rowCount = (0,0)#行数
        self.__datas = []#原始数据
        self.__names = []#原始数据对应的key,这样写是为了一个无序的dict
        self.__fs = 100#采样率
        self.__info = ""

    def getInfo(self):
        """
        @brief 获取数据的说明
        """
        return self.__info

    def setInfo(self,info):
        """
        @brief 设置数据的说明
        """
        self.__info = info
        
    def getRowCount(self):
        return self.__rowCount

    def setRowCount(self,minR,maxR):
        self.__rowCount = (minR,maxR)

    def getColumnCount(self):
        return len(self.__datas)

    @property
    def rowCount(self):
        return self.__rowCount

    @property
    def columnCount(self):
        return self.getColumnCount()

    @property  
    def datas(self):
        return self.__datas

    def setDatas(self,datas):
        self.__datas = datas

    @property  
    def fs(self):
        return self.__fs
    @fs.setter
    def fs(self,value):
        self.__fs = value
    

    @property
    def names(self):
        return self.__names

    def setNames(self,names):
        self.__names = names

    def getRowData(self,row):
        """
        @brief 获取某行数据
        """
        rowData = [];
        for col in self.__datas:
            if row < len(col):
                rowData.append(col[row])
            else:
                rowData.append('')
        return rowData

    def getColumnData(self,col):
        """
        @brief 获取一列数据
        """
        return self.__datas[col]

    @abstractmethod  
    def loadData(self,filePath):
        '''
        @brief 解析文件
        @param filePath 文件路径/目录
        '''
        pass


class PressureDataForExperiment(BaseChannelData):
    """
    @brief 北区实验
    """
    def __init__(self):
        super(BaseChannelData,self).__init__() 

    def loadData(self,filePath):
        self.clearValue()
        self.__getDataFromXls_experimentInBuctBeiqu(filePath)

    ##        
    # @brief 读取实验的测试数据
    # @param xlsFileFullPath xls文件的文件名包括路径
    # @return 返回一个hash
    def __getDataFromXls_experimentInBuctBeiqu(self,xlsFileFullPath):
        print(xlsFileFullPath)
        columnLens = []
        try:
            data = xlrd.open_workbook(xlsFileFullPath)
            table = data.sheets()[0]
            nrows = table.nrows
            ncols = table.ncols
            for c in range(2,ncols):
                column = table.col_values(c)
                colData = np.array(column[2:],float)
                self.names.append(column[1])
                self.datas.append(colData)
                columnLens.append(len(column[2:]))
                print("读取：{}数据{}个".format(column[1],columnLens[-1]))
            self.setRowCount( min(columnLens),max(columnLens) )
            return True
        except Exception as e:
            print("文件：{}，读取错误".format(xlsFileFullPath))
            print(e)
            return False

class PressureDataForSimulated(BaseChannelData):
    """
    @brief 处理模拟数据
    """
    def __init__(self):
        super(BaseChannelData,self).__init__()
        self.fs = 200

    def loadData(self,fileFolder):
        self.clearValue()
        #super(BasePressureData,self).clearValue()
        self.__getSimulatedDataFromFolder(fileFolder)

    def __getSimulatedDataFromFolder(self,fileFolder):
        for index,[root,dirs,files] in enumerate(os.walk(fileFolder)):
            PressureDataForSimulated.dealCsvFiles(self.names,self.datas,fileFolder,files)
            #更新rowCount columnCount等信息
            dlen = []
            for t in self.datas:
                dlen.append(len(t))
            self.setRowCount(min(dlen),max(dlen))
            break

    def dealCsvFiles(names,datas,dire,fis):
        print("in dir:" + dire)
        for f in fis:
            print("load file:" + f)
            if os.path.splitext(f)[1] == '.csv':
                with open(os.path.join(dire,f), 'r',encoding='gbk') as csvFile:
                    csvData =  csv.reader(csvFile)
                    PressureDataForSimulated.parserOneCsvFile(names,datas,csvData)
                    



    def parserOneCsvFile(names,datas,csvFileObj):
        """
	    @brief 提取csv文件里的数据
	    @param names 表头的引用
	    @param datas 数据的引用
	    """
        mark_name_index = -1
        data_start_index = -1
        name = ''
        meaData = []#保存通道的数据
        for index,row in enumerate(csvFileObj):
            if len(row) > 0:
                if row[0] == '[Name]':
                    if mark_name_index > 0:
                        datas.append(np.array(meaData,float)/1000.0)#把上一次提取的数据保存
                        meaData = [];
                    mark_name_index = index+1#标记名字的索引
                elif index == mark_name_index:
                    name = row[0][(row[0].find('@')+1):]
                    data_start_index = index + 4#更新数据索引
                    names.append(name)
                elif index >= data_start_index:
                    meaData.append(row[1])           
        datas.append(np.array(meaData,float)/1000.0)#把最后一个结果加入

class PressureDataForStandard(BaseChannelData):
    '''
    @brief 加载标准csv数据文件
    '''
    def __init__(self):
        super().__init__()

    def loadData(self,fileFolder):
        self.clearValue()
        info,names,datas = paserStandardCSVFile(fileFolder)
        self.setInfo(info[1])
        try:
            self.fs = float(info[2])
        except ValueError:
            print('文件读取异常，采样率（row:0,column:3）因为浮点型数据，请更正')
        self.setNames(names)
        #self.setDatas(np.array(cd) for cd in datas)
        dd= []
        lengthRow = []
        for cd in datas:
            y = np.array(cd,float)
            dd.append(y)
            lengthRow.append(len(y))
        self.setDatas(dd)
        self.setRowCount(min(lengthRow),max(lengthRow))


def paserStandardCSVFile(filePath):
    infomations = []
    names = []
    datas = []
    with open(filePath, 'r',encoding='gbk') as csvFile:
        csvData =  csv.reader(csvFile)
        for index,row in enumerate(csvData):
            if 0 == index:
                infomations = row
            elif 1 == index:
                names = row
                #同时初始化列表
                for ii in range(0,len(names)):
                    datas.append([])
            else:
                for ii,data in enumerate(row):
                    datas[ii].append(data)
    return [infomations,names,datas]

def loadData(path,dataType = 'std'):
    if dataType == 'sim':#模拟值
        data = PressureDataForSimulated()
        data.loadData(path)
    elif dataType == 'exp':
        data = PressureDataForExperiment()
        data.loadData(path)
    elif 'std':
        data = PressureDataForStandard()
        data.loadData(path)
    return data