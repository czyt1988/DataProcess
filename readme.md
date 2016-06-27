#说明
这是为我girlfriend博士期间处理数据写的代码

#设计的内容
主要涉及以下内容
- 简单的信号处理(直接的频谱分析，时频分析等)
- 气流脉动的计算

#主要功能看我女友大神的要求

#功能说明
##czy 通用包
-signal 信号处理相关

###signal
- spectrum 频谱分析
- dealFFTMagnitude fft之后的幅值处理
- dealFFTFrequency 根据采样率和fft的数目计算频率分布
- nextpow2 Find 2^n that is equal to or greater than.
- getXByFs 根据采样率和波形长度，获取波形的x轴
