import numpy as np
import math
import matplotlib.pyplot as plt  

x = [0,1,2,3,4,5,6,7]
y = [1,2,1,3,2,3,4,1]
plt.plot(x,y)
plt.show()
##计算同流通面积
#Args:
#   originD:float
#       直径
#   
#Returns:圆形面积
def calcSameFlowArea(originD,secInput,calcD = False):
    S = calcCircleArea(originD)
    if calcD:#如果是计算直径，说明secInput是个数
        smallS = S / secInput
        return calcCircleDiameter(smallS)
    else:#如果是计算面积，说明secInput是直径
        smallS = calcCircleArea(secInput)
        return S/smallS

##计算圆形面积
#Args:
#   D:float
#       直径
#Returns:圆形面积
def calcCircleArea(D):
    return (math.pi * D**2)/4.0

##根据圆形面积计算直径
#Args:
#   S:float
#       面积
#Returns:直径
def calcCircleDiameter(S):
    return (4*S/math.pi)**0.5

pipeD = 0.157
orificeD = pipeD / 2
d = range(0.01,)
print(calcSameFlowArea(orificeD,0.018))

