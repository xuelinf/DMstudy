#coding: utf-8
__author__ = 'xuelinf'

from math import log
import operator
import pickle
import treePlotter

# 计算信息增益
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        labelCount[currentLabel] = labelCount.get(currentLabel, 0) + 1
    shannonEnt = 0.0
    for key in labelCount:
        prob = float(labelCount[key])/numEntries
        shannonEnt -= prob*log(prob, 2)
    return shannonEnt

# 按照给定特征划分,三个参数为数据集,待划分特征,需要返回的特征的值
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])  # 将需要划分的特征值等于value的放在一起,返回其他属性的值
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 计算最佳数据划分
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1  # 去掉最后一个标签
    baseEntropy = calcShannonEnt(dataSet)  # 起始信息熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [e[i] for e in dataSet]
        uniqueVals = set(featList)  # 保存出现过的属性
        newEntropy = 0.0 # 以某属性为划分的新信息熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)  # 对属性出现的每种值,获得子数据集
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy  # 信息增益
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

# 构建决策树,其方法和前边的kNN投票的方式相同
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def creatTree(dataSet, labels):
    classList = [e[-1] for e in dataSet] # 标签集
    if classList.count(classList[0]) == len(classList):  # 某类别中全部内容相同
        return classList[0]
    if len(dataSet[0]) == 1:  # 如果属性已经耗尽,标签依然未完全区分
        return majorityCnt(classList)  # 那就返回出现次数最多的的那个标签
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]  # 最佳划分的属性名
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [e[bestFeat] for e in dataSet]
    uniqueVals = set(featValues)  # 该最佳属性划分情况下,划分出多少个不同的类
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = creatTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

# # 简单测试集,删
# def creatDataSet():
#     dataSet = [[1, 1, 'yes'],
#                [1, 1, 'yes'],
#                [1, 0, 'no'],
#                [0, 1, 'no'],
#                [0, 1, 'no']]
#     labels = ['no surfacing', 'flippers']
#     return dataSet, labels

# 使用决策树事例,第一个是建成的树,第二个是标签列表,第三个是测试用例
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    print featLabels
    featIndex = featLabels.index(firstStr)  # 直接找到该属性在标签列表所处的位置
    key = testVec[featIndex]  # 这样直接就可以根据我们的测试例该位置的值,进行判断
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):  # 是否叶子节点,否则继续决策
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

# pickle模块,存储决策树,该模块是实现数据序列和反序列化,可以将对象保存在文件里
def storeTree(inputTree, filename):
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

# 使用pickle ,可以重构原来的python 对象,类似于java 的序列化
def grabTree(filename):
    fr = open(filename)
    return pickle.load(fr)

if __name__ == '__main__':
    # myDat, labels = creatDataSet()
    # featLabels = labels[:]
    # print chooseBestFeatureToSplit(myDat)
    # tree = creatTree(myDat, labels)
    # print tree
    # print classify(tree, featLabels, [1,0])
    fr = open('lenses.txt')
    lenses = [e.strip().split('\t') for e in fr.readlines()]
    lensesLabels = ['age', 'prescript','astigmatic', 'tearRate']
    tree = creatTree(lenses, lensesLabels)
    print tree
    # treePlotter.createPlot(tree)
    # storeTree(tree, 'storeTree.txt')
    print grabTree('storeTree.txt')