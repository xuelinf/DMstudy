#coding: utf-8
__author__ = 'xuelinf'

# 用于测试, 删
def loadDataSet():
    return [[1,3,4], [2,3,5],[1,2,3,5],[2,5]]

# 创建大小为1 的候选集,就是将他们不重复的加入到集合中
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if frozenset([item]) not in C1:
                C1.append(frozenset([item]))
    C1.sort()
    return C1

# D是我们的事务集,CK是频繁项集
def scanD(D, Ck, minSupport):
    ssCnt = {}  # 计算每个项的出现次数
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0) + 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:  # 计算每个项的支持度,根据最小支持度加入结果中
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

# 构建k 元频繁项集
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:   # 比较除最后一位外,让其他元素相同
                retList.append(Lk[i] | Lk[j])
    return retList

# apriori 完整流程
def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)  # 这里没用过这样的用法,构建关于set 的映射
    L1, supportData = scanD(D, C1, minSupport)  # 先产生我们一阶的高于支持度
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

# 产生关联规则,L是频繁项集,supportData 是支持度集合
def generateRules(L, supportData, minConf = 0.5):
    bigRuleList = []
    for i in range(1, len(L)):  # 从1 开始,表示我们从频繁二项集开始
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf = 0.5):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            print freqSet-conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq, conseq,conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf = 0.5):
    m = len(H[0])
    if len(freqSet) >(m+1):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet,Hmp1, supportData,brl,minConf)
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__ == '__main__':
    dataSet = loadDataSet()
    L, supportData = apriori(dataSet, minSupport=0.5)
    rules = generateRules(L, supportData, minConf=0.5)
    print rules