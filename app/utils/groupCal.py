import pandas as pd
import numpy as np

# 基础函数


def strIsContain(string, flag):
    if flag in string:
        return string[1:]
    return string


# 保留几位小数
def saveDigitalPoint(value, pointNums):
    newValue = round(value + pow(0.1, pointNums + 1), pointNums)
    return newValue


def getMultiesByGroupAndOthers(dataterms, group, universe, frequency, column):
    # 加入一个方法来判断是否有“-”符号，如果有去掉 （字符串开头会有-？？？）
    column = strIsContain(column, '-')
    # 拿到传过来的数据（在指定时间段内的所有字段数据List类型）,并进行遍历
    df = dataterms.loc[(dataterms['universe'] == universe) & (dataterms['frequency'] == frequency) & (dataterms['group'] == group)]
    result = df[column].tolist()
    return result


def getDataMulties(seriesList):
    multiSeries = []
    count = 0
    sum = 0
    for i in seriesList:
        count += 1
        if count == 1:
            multiSeries.append(1)
            sum = 1
        else:
            sum = sum * (1 + i)
            multiSeries.append(sum)
    return multiSeries


# 先得到初始序列和累乘值序列
def calcByCondition(category):
    # 传入已经选定日期的数据，组别，fre, universe, 列名
    conditionList = getMultiesByGroupAndOthers(category.datas, category.group, category.universe, category.frequency,
                                               category.columnName)
    # 加入判断的目的是求1-5和5-1只需调用一次方法，而其他的需要调用5次
    # 求累乘的序列,传入初始序列的值，得到一个新的累乘值序列
    multiSeries = getDataMulties(conditionList)
    # 返回得到的初始值序列和累乘值序列
    return conditionList, multiSeries


# 计算年化收益率

def calcRet(RET_A):
    N = len(RET_A)
    # 计算组合净值曲线
    capital_line = np.cumprod(1 + np.array(RET_A)).tolist()
    annual_rtn = pow(capital_line[-1] / capital_line[0], 250 / N) - 1
    res = saveDigitalPoint(annual_rtn, 4)  # 保留四位小数
    return res


# 计算夏普比率，传入的是最初始的序列，在数据库中取出的原始序列
def create_sharpe_ratio(returns, periods=252):
    ratio = np.sqrt(periods) * (np.mean(returns)) / np.std(returns)
    res = saveDigitalPoint(ratio, 4)
    return res


# 计算最大回撤与最大回撤时间，传入的是一个已经累乘过的序列
def create_drawdowns(equity_curve):
    # argmax 取出元素最大的索引
    i = np.argmax((np.maximum.accumulate(equity_curve) - equity_curve) / np.maximum.accumulate(equity_curve))
    # 如果没有找到最大回撤时间段，则不显示
    if i == 0:
        j = 0
        maxDown = 1.0
        return maxDown, j, i
    # 回撤开始的时间点
    j = np.argmax(equity_curve[:i])
    # i j是位置索引不是时间
    maxDown = (float(equity_curve[i]) / equity_curve[j] - 1)
    res = saveDigitalPoint(maxDown, 8)
    return res, j, i


# 1-5 5-1

# 定义一个根据字段名称、universe、frequency指标算出的1.0-5.0和5.0-1.0的初始序列、累乘序列
def calcOneFiveStartValueAndMultiValue(datas, columnName, universe, frequency):
    columnName = strIsContain(columnName, '-')

    result1 = datas.loc[(datas['universe'] == universe) & (datas['frequency'] == frequency) & (datas['group'] == 1.0)][columnName]
    result5 = datas.loc[(datas['universe'] == universe) & (datas['frequency'] == frequency) & (datas['group'] == 5.0)][columnName]

    # 对1.0和5.0两个组的初始序列进行减法运算
    result1_5 = list(map(lambda x: x[0] - x[1], zip(result1, result5)))
    result5_1 = list(map(lambda x: x[0] - x[1], zip(result5, result1)))

    # 对计算得来的两个初始值序列进行累乘计算，调用累乘的方法
    multiList1_5 = getDataMulties(result1_5)
    multiList5_1 = getDataMulties(result5_1)

    # 将两个序列追加到result中去，是一个List，List中的每一项也是List
    # 可以是一个dict
    result = {"cv15": result1_5,
              "cv51": result5_1}

    multiValue = {"mv15": multiList1_5,
                  "mv51": multiList5_1}

    return result, multiValue


# 根据条件计算1.0-5.0和5.0-1.0的值, 返回的是一个List，List的每一项也是List
def calcByConditionOneFive(category):
    # # 传入已经选定日期的数据，fre, universe, 列名, 拿到1-5 和 5-1 的初始序列
    conditionList1_5, multiesList1_5 = calcOneFiveStartValueAndMultiValue(category.datas, category.columnName,
                                                                          category.universe, category.frequency)
    return conditionList1_5, multiesList1_5


