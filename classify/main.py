# -*- coding: utf-8 -*-

from math import log
import operator
import time

# 标签集，0为数值型，1为标称型
labelType = {'age':0,'job':1,'marital':1,'education':1,
             'default':1,'balance':0,'housing':1,'loan':1,
             'contact':1,'day':0,'month':1,'duration':0,
             'campaign':0,'pdays':0,'previous':0,'poutcome':1}


def calcShannonEnt(dataSet):
    """
    输入：数据集
    输出：数据集的香农熵
    描述：计算给定数据集的香农熵；熵越大，数据集的混乱程度越大
    """
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    """
    输入：数据集，选择维度，选择值
    输出：划分数据集
    描述：按照给定特征划分数据集；去除选择维度中等于选择值的项
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

def split_data_min(dataset, axis, value):
    '''
    将dataset按除开某一特征值划分
    :param dataset: 数据集
    :param axis: 数据集中的位置
    :param value: 特征值
    :return: 除开某一特征值的列表,属性为小于数值型
    '''
    retDataSet = []
    for featVec in dataset:
        try:
            if float(featVec[axis]) <= float(value):
                reducedFeatVec = featVec[:axis]
                reducedFeatVec.extend(featVec[axis+1:])
                retDataSet.append(reducedFeatVec)
        except:
            retDataSet.append(featVec[:axis+1])
            return retDataSet
    return retDataSet

def split_data_max(dataset, axis, value):
    '''
    将dataset按除开某一特征值划分
    :param dataset: 数据集
    :param axis: 数据集中的位置
    :param value: 特征值
    :return: 除开某一特征值的列表,属性为大于数值型
    '''
    retDataSet = []
    for featVec in dataset:
        try:
            if float(featVec[axis]) > float(value):
                reducedFeatVec = featVec[:axis]
                reducedFeatVec.extend(featVec[axis+1:])
                retDataSet.append(reducedFeatVec)
        except:
            retDataSet.append(featVec[:axis+1])
            return retDataSet
    return retDataSet


def chooseBestFeatureToSplit(dataset, labels):
    '''
    根据信息增益最大，选择最好的数据集划分特征
    :param dataset: 数据集
    :param labels:标签
    :return: 最优分割特征
    '''
    num = len(dataset[0]) - 1   # 数量
    baseEntropy = calcShannonEnt(dataset)    #信息熵
    bestInfoGain = 0.0  #信息增益
    bestFeature = -1    # 最优分割特征
    for i in range(num):
        if labelType[labels[i]]== 1:
            featList = [example[i] for example in dataset]
            uniqueVals = set(featList)
            newEntropy = 0.0
            for value in uniqueVals:
                subDataSet = splitDataSet(dataset, i, value)
                prob = len(subDataSet)/float(len(dataset))
                newEntropy += prob * calcShannonEnt(subDataSet)
            infoGain = baseEntropy - newEntropy
        else:
            infoGain=0.0
            featList = [example[i] for example in dataset]
            featList.sort()
            for j in range(0,len(featList)-1,3000):     # 分箱
                value=(float(featList[j])+float(featList[j+1]))/2.0
                minDataSet=split_data_min(dataset, i, value)
                maxDataSet=split_data_max(dataset, i, value)
                prob = (j+1)/len(featList)
                newEntropy = prob * calcShannonEnt(minDataSet)+(1-prob)*calcShannonEnt(maxDataSet)
                subinfoGain = baseEntropy - newEntropy
                if subinfoGain>infoGain:
                    infoGain=subinfoGain
                    labelType[labels[i]]=str(value)
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    """
    输入：分类类别列表
    输出：子节点的分类
    描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
          采用多数判决的方法决定该子节点的分类
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1))
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    """
    输入：数据集，特征标签
    输出：决策树
    描述：递归构建决策树，利用上述的函数
    """
    if len(dataSet) == 0:
        return '"no"'
    if len(dataSet) == 1:
        return '"no"'
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return classList[0]
    if len(dataSet[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet,labels)
    bestFeatLabel = labels[bestFeat]
    name=labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    # 得到列表包括节点所有的属性值
    if labelType[name] == 1:
        featValues = [example[bestFeat] for example in dataSet]
        uniqueVals = set(featValues)
        for value in uniqueVals:
            subLabels = labels[:]
            myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    else:
        subLabels = labels[:]
        myTree[bestFeatLabel]['low'+str(labelType[name])] = createTree(split_data_min(dataSet, bestFeat, labelType[name]),subLabels)
        subLabels = labels[:]
        myTree[bestFeatLabel]['high'+str(labelType[name])] = createTree(split_data_max(dataSet, bestFeat, labelType[name]),subLabels)
    return myTree


def classify(inputTree, featLabels, testVec):
    """
    输入：决策树，分类标签，测试数据
    输出：决策结果
    描述：跑决策树
    """
    global classLabel
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if labelType[firstStr] == 1:
            if testVec[featIndex] == key:
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = classify(secondDict[key], featLabels, testVec)
                else:
                    classLabel = secondDict[key]
        else:
            if 'low' in key:
                if float(testVec[featIndex]) <= float(key[3:]):
                    if type(secondDict[key]).__name__ == 'dict':
                        classLabel = classify(secondDict[key], featLabels, testVec)
                    else:
                        classLabel = secondDict[key]
            elif 'high' in key:
                if float(testVec[featIndex]) > float(key[4:]):
                    if type(secondDict[key]).__name__ == 'dict':
                        classLabel = classify(secondDict[key], featLabels, testVec)
                    else:
                        classLabel = secondDict[key]
    return classLabel

def classifyAll(inputTree, featLabels, testDataSet):
    """
    输入：决策树，分类标签，测试数据集
    输出：决策结果
    描述：跑决策树
    """
    classLabelAll = []
    for testVec in testDataSet:
        classLabelAll.append(classify(inputTree, featLabels, testVec))
    return classLabelAll

def storeTree(inputTree, filename):
    """
    输入：决策树，保存文件路径
    输出：
    描述：保存决策树到文件
    """
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    """
    输入：文件路径名
    输出：决策树
    描述：从文件读取决策树
    """
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

def format_data(text):
    '''
    格式化数据
    :return: 数据集和标签
    '''
    t = file("bank-full.{0}".format(text), "rb")
    data = []
    dataset = []
    newlabel = []
    for line in t:
        data.append(line.split(';'))
    for line in data:
        line[16] = line[16].strip()
        dataset.append(line[0:])
    label = dataset.pop(0)
    label = label[:-1]
    for line in label:
        newlabel.append("".join([a for a in line if a.isalpha()]))
    t.close()
    return dataset, newlabel

def createDataSet():
    """
    从format_data获取train
    """
    dataSet = format_data('train')[0]
    labels = format_data('train')[1]
    return dataSet, labels

def createTestSet():
    """
    从format_data获取test
    """
    testSet = format_data('test')[0]
    return testSet


def getTrueAns():
    '''
    得到真实数据正确答案
    :return:list
    '''
    t = file("bank-full.test", "rb")
    data = []
    ans = []
    for line in t:
        data.append(line.split(';'))
    del data[0]
    for line in data:
        line[16] = line[16].strip()
        ans.append(line[-1])
    return ans


def main():
    starttr = time.time()
    dataSet, labels = createDataSet()
    labels_tmp = labels[:] # 拷贝，createTree会改变labels
    desicionTree = createTree(dataSet, labels_tmp)
    endtr = time.time()
    print '训练时间'+str(endtr - starttr)
    #storeTree(desicionTree, 'classifierStorage.txt')
    #desicionTree = grabTree('classifierStorage.txt')
    # print('desicionTree:\n', desicionTree)
    startte = time.time()
    testSet = createTestSet()
    # print('classifyResult:\n', classifyAll(desicionTree, labels, testSet))
    me = classifyAll(desicionTree, labels, testSet)
    endte = time.time()
    print '测试时间'+str(endte - startte)
    ans = getTrueAns()
    yy=0
    yn=0
    ny=0
    nn=0
    for i in range(0,len(me)):
        if me[i] == ans[i]:
            if me[i] == '"yes"':
                yy += 1
            else:
                nn += 1
        else:
            if me[i] == '"yes"':
                ny += 1
            else:
                yn += 1
    print '混淆矩阵'+str((yy,yn,nn,ny))
    print '准确率'+str(float((yy+nn))/float(yy+yn+ny+nn))
    print 'yes召回率'+str(float(yy)/float(yy+yn))
    print 'no召回率'+str(float(nn)/float(ny+nn))
    print 'yes命中率'+str(float(yy)/float(yy+ny))
    print 'no命中率'+str(float(nn)/float(yn+nn))
    print 'yes的f-1 '+str(float(yn)/float(yy+yn))
    print 'no的f-1 '+str(float(ny)/float(nn+ny))


if __name__ == '__main__':
    main()