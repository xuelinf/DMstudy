# coding:utf-8
__author__ = '$USER'

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir

# 简单测试,删
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

# 简单的kNN算法,计算欧氏距离, 输入向量, 数据集, 标签, k
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1))-dataSet  # tile 复制成矩阵
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1) # axis=1代表矩阵每一行相加
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort() # distances排序之后返回索引,这个溜
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1  # 字典中如果有,获取之,如果没有,创建之,赋值0
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse = True)
    # 针对字典每个对象排序,排序关键词为第二域元素,降阶
    return sortedClassCount[0][0]

# 从文件中读取,分析数据,储存前三个属性,以及标签项
# 代码很整洁,值得学习
def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = zeros((numberOfLines, 3)) # 库内函数, 初始化一个全0的矩阵
    d = {'largeDoses': 3, 'smallDoses': 2, 'didntLike': 1} # 数据集有一点问题,做一个小处理,实际中用不到

    classLabelVector = []
    index = 0
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]  # 矩阵的快速表达方式,index 为行数,后边为每行列表
        if type(listFromLine[-1]) == type('string'):
            temp = d[listFromLine[-1]]
            classLabelVector.append(int(temp))
        else:
            classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector   # 前者是前三个属性建立的矩阵,后者是每行对应的标签

# 数据归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0) # 参数0,表示选出最小, 每列的最小值,它是一个数组
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet)) # shape,但这里是比照DataSet 建立全0矩阵
    # print normDataSet 可以看出来
    m = dataSet.shape[0] # 第一维度长度
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


# 离散图测试
def draw_data():
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()

# 测试归一化数据
def norm_test():
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    print normMat, ranges, minVals

# 测试kNN效果
def datingClassTest():
    hoRatio = 0.15  # 选择用于测试的大小
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)  # 测试的大小
    errorCount = 0.0
    # 前边那么多作为测试集,后边的是训练集
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m],5)
        print "the came back with: %d, real answer: %d" %(classifierResult, datingLabels[i])
        if(classifierResult != datingLabels[i]):
            errorCount += 1.0
    print errorCount/float(numTestVecs)

# 将图像矩阵转换成数组形式
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(lineStr[j])
    fr.close()
    return returnVect

# 训练数字识别
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')  # 保存文件夹内所有内容, mac 下文件内第一个文件是.DS_Store 注意识别
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    print m
    for i in range(1, m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' %fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(1, mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' %fileNameStr)
        classifierRest = classify0(vectorUnderTest, trainingMat, hwLabels, 4)
        print "compute answer is: %d, read answer is: %d" % (classifierRest, classNumStr)
        if(classifierRest != classNumStr):
            errorCount += 1
    print '\nthe total errors number: %d' %errorCount
    print '\nerror rate is: %f' % (errorCount/float(mTest))

if __name__ == '__main__':
    handwritingClassTest()