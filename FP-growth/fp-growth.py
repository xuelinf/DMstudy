#coding: utf-8
__author__ = 'xuelinf'

# 先来建立树节点的结构,包括值,出现次数,父亲节点,节点链,孩子们 = =!好多东西
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    # 增加节点计数
    def inc(self, numOccur):
        self.count += numOccur

    # 描绘树结构
    def disp(self, ind = 1):
        print '-'*ind, self.name, ' ',self.count
        for child in self.children.values():
            child.disp(ind+2)

# 主建树函数, 参数为数据集和最小支持
def createTree(dataSet, minSup = 1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]  # 此处dataSet 不指示每个事务出现次数的话,替换成1
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del headerTable[k]  # 删除支持不足最低支持
    freqItemSet = set(headerTable.keys())  # 频繁项集,去重,使用set,一会在查找时效率高
    if len(freqItemSet) == 0: return None,None  # 如果没有,可以直接返回
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]   # 因为是头指针表,还要维护一个指针,所以变换一下形式
    retTree = treeNode('Null Set', 1, None)  # 初始化
    for tranSet,count in dataSet.items():  # 还是要注意dataSet 的结构
        localD = {}  # 对每个事务里的每一项,排序
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        # 排序,从大到小
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p:p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count) # 建立FP 树
    return retTree, headerTable

# 更新FP 树,参数: 事务里有序项, 树, 头指针表, 这一事务的计数
def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:   # 对于第一项,要考虑是不是已有节点
        inTree.children[items[0]].inc(count)  # 有的话,直接将计数添加到该节点
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)   # 否则建立一个新节点,并记录在当前树的儿子列表中
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]  # 如果该项对应的头指针表,没有对应的列表,就添加
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])  # 如果已经有了,那么久要更新头指针表
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)  # 对于余下的项,递归

# 更新头指针表,参数: 头指针,要添加的对象
def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None):  # 指到链表结尾
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

# 将某节点前缀路径递归的加入到prefixPath中
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

# 找到所有节点的前缀路径
def findPrefixPath(basePat, treeNode): # 参数1 是后件,2是来自头指针表的对象
    condPats = {}
    while treeNode != None:  # 所以要顺着头指针表, 遍历所有的对象
        prefixPath = []
        ascendTree(treeNode, prefixPath)  # 获得前缀
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count # 这里获得还是对象,转化成一个frozenset
        treeNode = treeNode.nodeLink
    return condPats

# 递归查找频繁项集,参数:当前节点,头指针表,最小支持度,(初始列表),频繁项集列表
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p:p[1])]
    # 排序,最出现次数最小的开始找, lambda里用p[1]是先按p[1][0]排序,相等则比较p[1][1]指了多深,具体为什么还不清楚
    # print bigL
    for basePat in bigL:
        newFreqSet = preFix.copy()   # 深拷贝一个
        newFreqSet.add(basePat)   # 加上当前正在访问的节点
        freqItemList.append(newFreqSet)  # 因为这一定是一个支持度高于最低支持的一个频繁项,所以可以添加到结果里
        # print freqItemList
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])  # 找到当前节点对应的前缀们
        # print condPattBases
        myCondTree, myHead = createTree(condPattBases, minSup)  # 对于这些前缀,构造条件FP树,这样就剔除掉了低于支持度的点
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet,freqItemList)
            # 然后针对这个新树,继续按出现频率排序,从最小的频率往我们的频繁项集里放,
            # 再针对这一节点的前缀,构建其FP 条件树,递归下去,直到拿到结果

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDic = {}
    for trans in dataSet:
        retDic[frozenset(trans)] = 1
    return retDic

if __name__ == '__main__':
    # simpDat = loadSimpDat()
    # print simpDat
    # initSet = createInitSet(simpDat)
    # myFPtree, myHeaderTab = createTree(initSet, 3)
    # myFPtree.disp()
    # print myHeaderTab
    # print findPrefixPath('t', myHeaderTab['t'][1])
    # freqItemList = []
    # mineTree(myFPtree, myHeaderTab, 3, set([]), freqItemList)
    # print freqItemList
    parseDat = [line.split() for line in open('kosarak.dat').readlines()]
    initSet = createInitSet(parseDat)
    myFPtree, myHeaderTab = createTree(initSet, 70000)
    myFreqList = []
    mineTree(myFPtree,myHeaderTab,100000, set([]), myFreqList)
    print myFreqList