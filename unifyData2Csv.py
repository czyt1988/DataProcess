
import const
import os.path
from waveData import UnifyChannelData


'''
统一数据文件为一个csv
csv的格式为：
row 1:markdata,information,fs
row 2:names
row 3 and other :datas
'''
#const.TYPE_EXP = 'exp'
#const.Path = 'D:/快盘/PIV实验台协同目录/数据处理-压力传感器/北区实验数据/25米直管/0.103mpa/6-15,测25米直管0.103mpa11.xlsx'
#upd = PressureData.PressureDataForExperiment()
#upd.setData(const.Path)
#print(upd.names)
#print(upd.datas[0])
#定义的输出目录

#ROOT_SHARE_PATH = 'd:/cloudDisk/share/【论文】双罐/模拟分析/SingleTankSmall/'
##文件目录
#FILE_PATH = ''
##
#UNIFY_PATH = '统一格式'
#DATA_NAME = FILE_PATH
#UNIFY_NAME = '单一缓冲罐-全体积'

#filePath = os.path.join(ROOT_SHARE_PATH,FILE_PATH)
#unityPath = os.path.join(ROOT_SHARE_PATH,UNIFY_PATH,UNIFY_NAME)
#filePath = ''
#unityPath = ''
#UnifyPressureData.unifySimulatedPressureData(filePath,unityPath,fs=200,info=DATA_NAME)

DATA_PATH_FOR_EXP = 'd:/netdisk/PIV实验台协同目录/matlab/数据处理-压力传感器/北区实验数据/25米直管错位单容/25米后移两米错位单容开机不带压/实验数据6-15,测错位单容开机不带压'
SAVE_PATH = 'd:/netdisk/PIV实验台协同目录/shareCloud/python/北区第一次实验数据分析'
#DATA_NAME = '25m单容错位-1'
#unityPath = os.path.join(SAVE_PATH,DATA_NAME+'.csv')
#UnifyChannelData.unifyExprementPressureData(DATA_PATH_FOR_EXP,unityPath,fs=100,info=DATA_NAME)

for i in range(1,6):
    filePath = '%s%d.xlsx'%(DATA_PATH_FOR_EXP,i)
    DATA_NAME = '25m单容错位-开口-%d'%(i)
    unityPath = os.path.join(SAVE_PATH,DATA_NAME+'.csv')
    UnifyChannelData.unifyExprementPressureData(filePath,unityPath,fs=100,info=DATA_NAME)