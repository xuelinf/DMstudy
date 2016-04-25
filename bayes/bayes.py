#coding: utf-8
__author__ = 'xuelinf'
import operator
from numpy import *
import re
import feedparser

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

# 创建一个词汇库,将之前所有词汇并起来获得并集
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

# 获得inputSet 的向量对于词汇库的向量,也就是词汇表中的词在文档中是否出现
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0 for i in range(len(vocabList))]
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1  # 本质上,就是将一组单词转换为一组数字
        else:
            print "the word: %s is not in my Vocabulary!" %word
    return returnVec

# 词袋模型,其实只是考虑到有些单词出现不止一次
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0 for i in range(len(vocabList))]
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1  # 出现一次,多加一次
    return returnVec

# 训练出两个概率模型
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)   # 训练集的数量
    numWords = len(trainMatrix[0])  # 每个训练项的维度
    pAbusive = sum(trainCategory) / float(numTrainDocs)   # 这样写只支持二分方式,1&0,表示其中为1的比率
    p0Num = ones(numWords)  # 为了优化,改成初始为1
    p1Num = ones(numWords)
    p0Denom = 2.0  # 初始为2
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:  # 为1 则在1的文档里添加,同时总数加到父母上
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)  # 改用对数,解决下溢出问题,而且不会对结果造成任何损失
    p0Vect = log(p0Num/p0Denom)
    return p0Vect, p1Vect, pAbusive

# 对测试向量,判断哪个概率更大,则倾向于哪一种
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify*p1Vec) + log(pClass1)
    p0 = sum(vec2Classify*p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

# 较为完整的流程,装载测试集,建立词汇表,训练
def testNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['stupid', 'garbage', 'dog']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, classifyNB(thisDoc, p0V, p1V, pAb)

# 数据内容处理,去除长度小于2 的分组,去除非字母分组
def textParse(bigString):
    listOfTokens = re.split(r'\W+', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

# 测试流程,读取email 中的内容,贝叶斯的方式进行处理
def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat =[]
    trainClass = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0V, p1V,pSpam = trainNB0(array(trainMat), array(trainClass))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V,p1V,pSpam) != classList[docIndex]:
            print docList[docIndex]
            errorCount += 1
    print 'error rate is:', errorCount/float(len(testSet))

# 将单词出现次数排序,可以获得词频最高的单词
def calcMostFreq(vocabList, fullText):
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(),key=operator.itemgetter(1), reverse = True)
    print sortedFreq[:20]
    return sortedFreq[:40]
# 和上边的处理方式是一样的, 只是添加了获取rss 的过程
def localWords(feed1, feed0):
    docList = []
    classList = []
    fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)
    for pairW in top30Words:  # 移除高频词汇, 可以打印出来看一下, 大部分都是主语和辅助词汇,意义不大
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])
    trainingSet = range(2*minLen)
    testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClass = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0V, p1V, Pspam = trainNB0(array(trainMat), array(trainClass))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, Pspam) != classList[docIndex]:
            errorCount += 1
    print "the error is", errorCount, "the rate:", float(errorCount)/float(len(testSet))
    return vocabList, p0V, p1V

def getTopWord(ny, sf):
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []
    topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0: topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0: topNY.append((vocabList[i], p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair:pair[1], reverse = True) # 这里的lambda 以前没这么用过
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "SFSFSFSFSFSFSFSSFSFSFSFSFS"
    for e in sortedSF:
        print e
    print "NYNYNYNYNYNYNYNYNYNYNYNYNY"
    for e in sortedNY:
        print e

if __name__ == '__main__':
    # listOPosts, listClasses = loadDataSet()
    # myVocabList = createVocabList(listOPosts)
    # trainMat = []
    # for p in listOPosts:
    #     trainMat.append(setOfWords2Vec(myVocabList,p))
    # P0V,P1V,PAb = trainNB0(trainMat, listClasses)
    # print P0V
    # print P1V
    # print PAb
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    getTopWord(ny, sf)
