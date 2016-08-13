# coding:utf-8

import copy


# 本函数用来将传入的二维数据使用one-hot编码实现数值化，返回为编码后的data
def use_one_hot(data, i):
    one_hot1 = []    # 进行数值化
    for line in data:
        one_hot1.append(line[i])
    one_hot2 = one_hot(one_hot1)
    t = 0
    for line in data:
        line[i] = one_hot2[t]
        t += 1
    return data


# 本函数用来将传入的非数值数据使用one-hot编码实现数值化，返回为编码后的data
def one_hot(data):
    t = 0   # 游标
    l = 0   # one-hot编码长度
    data_set = copy.deepcopy(data)     # 将data赋给set
    data_dict = {}  # 命一个dict来对应储存one-hot编码
    data_set = set(data_set)     # 去重
    for s in data_set:  # 计算有多少个来觉得one-hot编码长度
        l += 1
    s_list = ['0'] * l  # 得出one-hot编码初始值
    for line in data_set:   # 循环得出one-hot编码与对应选项存入到dict里
        s_list[t] = '1'
        t += 1
        one_list = s_list
        one_list = ''.join(one_list)    # 将list转换为str
        data_dict[line] = one_list      # 将one-hot编码和数据对应存入到dict中
        s_list = ['0'] * l  # 初始化one-hot编码
    for a in range(0, len(data)):   # 根据数据替换为one-hot编码
        data[a] = data_dict[data[a]]
    return data