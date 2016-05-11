#coding: utf-8
__author__ = 'xuelinf'

from numpy import *
import matplotlib.pyplot as plt

# 载入数据集
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])  # 逐行将两个属性加入,加一个1方便操作
        labelMat.append(int(lineArr[2]))  # 保存标签
    return dataMat, labelMat

# sigmoid 函数,输入实际上最佳的加权值
def sigmoid(inX):
    return 1.0/(1+exp(-inX))

# 获得回归后的系数列表,输入为属性数组,标签数组
def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)  # 转成矩阵,来使用numpy 操作
    labelMat = mat(classLabels).transpose()  # 旋转一下
    m,n = shape(dataMatrix)  # m 微数据个数,n 为维度
    alpha = 0.001  # 步长
    maxCycles = 500  # 迭代次数
    weights = ones((n,1))  # 初始系数全部为1
    # print dataMatrix * weights
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)  # 计算每次利用sigmod 预测的结果,获得与标签的差值
        error = (labelMat - h)
        weights = weights+alpha * dataMatrix.transpose() * error  # 根据差值修正weights
    return weights

# 随机梯度上升,参数与上相同,但是方法确实每次利用新样本,行增量式更新
def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights= ones(n)  # 一行
    for j in range(100):  # 增加迭代次数
        for i in range(m):
            h = sigmoid(sum(dataMatrix[i]*weights))  # 每次样本进来,就计算一次sigmoid,根据结果,对weights 更新
            error = classLabels[i] - h
            weights = weights+alpha*error*dataMatrix[i]  # 每次都更新
    return weights

# 改进的随机梯度上升,首先步长会越来越小,其次每次随机选取更新对象
def stocGradAscent1(dataMatrix, classLabels, numIter = 150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i) + 0.01   # 避免严格下降
            randIndex = int(random.uniform(0, len(dataIndex)))  # 随机选一个样本
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

# 分类预测,参数1是输入的向量,参数2是回归得到的系数
def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

# 采用改进的随机梯度上升方法,对数据集进行训练,然后进行预测
def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))  # 保存每行的向量
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 500)
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights))!=int(currLine[21]):  # 判断分类是否正确
            errorCount += 1
    errorRate = float(errorCount)/numTestVec
    print "the error arte: %f" %errorRate
    return errorRate

def plotBestFit(wei):
    weights = wei.getA()
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = [];ycord1 = []
    xcord2 = [];ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]); ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1]); ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2, ycord2,s=30,c='green')
    x = arange(-3.0,3.0,0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


if __name__ == '__main__':
    # dataArr, labelMat = loadDataSet()
    # weights = mat(stocGradAscent1(array(dataArr),labelMat))
    # weights2 = gradAscent(dataArr, labelMat)
    # new =  weights.transpose()
    # print new
    # plotBestFit(new)
    colicTest()