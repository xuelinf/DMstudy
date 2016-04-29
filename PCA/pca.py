#coding: utf-8
__author__ = 'xuelinf'

from numpy import *

def loadDataSet(fileName, delim = '\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat = 9999999):
    meanVals = mean(dataMat, axis=0)  # 求平均值,
    print meanVals
    meanRemoved = dataMat - meanVals  # 去平均值
    covMat = cov(meanRemoved, rowvar=0)  # 协方差,rowvar =1表示每行看成一个整体,=0,表示一列看成一个整体,得到协方差矩阵
    print covMat
    eigVals, eigVects = linalg.eig(mat(covMat))  # 计算协方差矩阵特征值,和特征向量
    eigValInd = argsort(eigVals)  # 得到排序后的下标们
    eigValInd = eigValInd[:-(topNfeat+1):-1]  # 切片高级功能,找到topNfeat 这么多个元素,从后往前排
    print eigValInd
    print eigVects
    print eigVals
    redEigVects = eigVects[:,eigValInd]  # 保留那些特征向量
    print redEigVects
    lowDDataMat = meanRemoved*redEigVects  # 转换到新空间[N*m]*[m*newm]
    reconMat = (lowDDataMat*redEigVects.T) + meanVals  # 被重构后返回,用来和原来比较,用于调试
    print lowDDataMat
    print reconMat
    print dataMat
    return lowDDataMat, reconMat

if __name__ == '__main__':
    dataMat = loadDataSet('testSet.txt')
    lowDMat, reconMat = pca(dataMat, 1)
