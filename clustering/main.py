# coding:utf-8

import math
import onehot
import csv
import random
import time


def get_avg(data):
    '''
    平均值
    :param data: 一个list
    :return: result
    '''
    p1 = 0  # 数量
    age_sum = 0  # 总和
    for line in data:
        age_sum += float(line)
        p1 += 1
    result = age_sum/p1
    return result


def get_mode(data):
    '''
    计算众数
    :param data:一维list
    :return: list中的众数
    '''
    mode = []   # 用于储存众数
    age_appear = dict((a, data.count(a)) for a in data)  # 统计各个元素出现的次数
    if max(age_appear.values()) == 1:  # 如果最大的出现为1
        for k, v in age_appear.items():     # 就返回随机一个数
            mode.append(k)
            return mode
    else:
        for k, v in age_appear.items():  # 否则，出现次数最大的数字，就是众数
            if v == max(age_appear.values()):
                mode.append(k)
    return mode


def ed_relate_f(dataX, dataY):      # 计算浮点型欧氏距离
    '''
    :param dataX:第一行
    :param dataY: 第二行
    :return: 之间的相似度
    '''
    summ = 0
    if len(dataX) == len(dataY):
        for a in range(0, len(dataX)):
            if a == 0:
                if dataX[a] != dataY[a]:
                    summ = 2
                continue
            summ += (float(dataX[a])-float(dataY[a])) ** 2
        relate = math.sqrt(summ)
        return relate
    else:
        print 'len is not equal'
        return 0


def ed_relate(dataX, dataY):    # 计算整型欧氏距离
    '''
    :param dataX:第一行
    :param dataY: 第二行
    :return: 之间的相似度
    '''
    summ = 0
    if len(dataX) == len(dataY):
        for a in range(0, len(dataX)):
            if a == 0:
                if dataX[a] != dataY[a]:
                    summ = 2
                continue
            summ += (dataX[a]-dataY[a]) ** 2
        relate = math.sqrt(summ)
        return relate
    else:
        print 'len is not equal'
        return 0


def get_file():
    '''
    打开文件
    :return:全部数据，二维list
    '''
    csvfile = file('D:\\turkiye-student-evaluation_generic.csv', 'rb')
    reader = csv.reader(csvfile)
    data =[]
    for line in reader:
        data.append(line)
    del data[0]
    return data


def km_first(data,k):
    '''
    第一次km，初始化数据
    :param data:
    :return: 分割好的data
    '''
    mid = random.sample(data, k)
    ed_lenth = []   # 余弦距离
    for m in mid:   # 分别计算计算剩下的元素到k个簇中心的相异度
        temp = []
        for d in data:
            if m == d:
                continue
            else:
                temp.append(ed_relate_f(m[1:], d[1:]))
        ed_lenth.append(temp)
    ed_lenth = map(list, zip(*ed_lenth))
    new_data=[]
    for i in range(len(ed_lenth[0])):   # 初始化数组
        new_data.append([])
    for i in range(len(ed_lenth)):
        new_data[ed_lenth[i].index(min(ed_lenth[i]))].append(data[i])
    return new_data




def km(data):
    '''
    k-means
    :param data:三维；list
    :param k: 簇
    :return: 打印类内距离和，任意两点距离和，他们的比值和时间
    '''
    mid = []    # 中心值
    for line in data:      # 如果不是，就计算数值的均值和one-hot编码的众数
        if line:
            temp = []
            temp2 = []
            line = map(list, zip(*line))    # 转置取
            mode = get_mode(line[1])    # 众数
            for i in line[2:]:
                temp.append(get_avg(i))     # 均值
            temp2.append(mode[0])
            temp2.extend(temp)
            mid.append(temp2)
    ed_lenth = []   # 余弦距离
    for m in mid:   # 分别计算计算剩下的元素到k个簇中心的相异度
        temp = []
        for data_n in data:
            for d in data_n:
                if m == d:
                    continue
                else:
                    temp.append(ed_relate_f(m[0:], d[1:]))
        ed_lenth.append(temp)       # 每个mid对应每个元素的距离
    ed_lenth = map(list, zip(*ed_lenth))    # 每个元素对应每个mid的距离
    new_data = []
    for i in range(len(ed_lenth[0])):   # 初始化数组
        new_data.append([])
    data_n = sum(data, [])      # 压平二维数组
    for i in range(len(ed_lenth)):
        new_data[ed_lenth[i].index(min(ed_lenth[i]))].append(data_n[i])     # 将最小值对应的元素放入到new_data中
    print '迭代中...请稍等...'
    if new_data == data:
        lenth_sum = 0   # 类内距离和
        random_sum = 0      # 任意两点距离和
        for d1 in data:     # 计算类内距离和
            print '类内距离和计算中...'
            d1 = [[int(x) for x in row] for row in d1]
            for i in range(len(d1)):
                for j in range(i, len(d1)):
                    lenth_sum += ed_relate(d1[i][1:], d1[j][1:])
        print '类内距离和计算完毕'
        data_n = sum(data, [])
        data_n = [[int(x) for x in row] for row in data_n]
        start1 = time.time()
        for i in range(len(data_n)):    # 计算任意两点距离和
            for j in range(i+1, len(data_n)):
                random_sum += ed_relate(data_n[i][1:], data_n[j][1:])
        print '任意两点距离和计算完毕'
        end1 = time.time()
        print '任意两点距离和计算时间:'+str(end1 - start1)
        print lenth_sum
        print random_sum
        print lenth_sum/random_sum
    else:
        km(new_data)

if __name__ == '__main__':
    start = time.time()
    data = get_file()   # 获取到数据
    data = onehot.use_one_hot(data, 1)  # 将第二列标称型换为one-hot编码
    km(km_first(data, 15))    # 进行k-means算法
    end = time.time()
    print '总计算时间:'+str(end - start)
