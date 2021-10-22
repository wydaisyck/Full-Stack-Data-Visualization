import pandas as pd
import numpy as np
from app.utils.groupCal import calcByCondition, calcRet, create_sharpe_ratio, create_drawdowns, calcByConditionOneFive
from app.utils.const import noneed_column


def getDatasInStore():
    data = pd.read_pickle(r'mongodata.pkl')
    return data


def getDataInTerm(datas, startdate, enddate):
    data = datas.loc[(datas['date'] >= startdate) & (datas['date'] <= enddate)]
    return data


def getChartsXaxis(datas, universe, frequency):
    datelist = datas[(datas.universe == universe) & (datas.frequency == frequency)]["date"].unique()
    return datelist.tolist()


def get_table1_result(dotdict):
    datas = getDatasInStore()
    datasTerms = getDataInTerm(datas, dotdict.startDate, dotdict.endDate)
    dotdict.datas = datasTerms
    dateList = getChartsXaxis(datasTerms, dotdict.universe, dotdict.frequency)
    allYAxisDatas = []
    save_dict_list = []
    groupList = [1.0, 2.0, 3.0, 4.0, 5.0]
    for group in groupList:
        dotdict.group = group
        conditionValues, multiValues = calcByCondition(dotdict)
        # 计算年化收益率的方法, 传入的值为初始序列
        rateByYearOne = calcRet(conditionValues)

        # 调用计算夏普比率的函数，返回一个数值类型的值
        sharpRatioOne = create_sharpe_ratio(conditionValues)

        # 调用最大回撤的函数，返回三个值，第一个值：最大回撤值，第二个值：开始时间，第三个值：结束时间
        # i j 只是列表的索引
        maxDownOne, i, j = create_drawdowns(multiValues)
        # print(maxDownOne, i, j)

        savedict = {'group': group,
                    'rateByYear': rateByYearOne,
                    'sharpRatio': sharpRatioOne,
                    'maxDown': maxDownOne,
                    'startDate': i,
                    "endDate": j}
        save_dict_list.append(savedict)
        allYAxisDatas.append(multiValues)

    # 2.计算1.0-5.0和5.0-1.0 计算时这两个和其他五个组分开计算
    conditionValuesOneFive, multiValuesOneFive = calcByConditionOneFive(dotdict)
    # 开始计算这两个的指标值
    for i, m, group_name in zip(conditionValuesOneFive, multiValuesOneFive, ['1.0-5.0', '5.0-1.0']):  # 1-5 和 5-1 共2个
        # 调用计算年化收益率的函数,返回一个数值类型的值
        rateByYearOne = calcRet(conditionValuesOneFive[i])
        # 调用计算夏普比率的函数，返回一个数值类型的值
        sharpRatioOne = create_sharpe_ratio(conditionValuesOneFive[i])
        # 调用计算最大回撤值的函数，返回一个数值类型的值
        maxDownOne, j, k = create_drawdowns(multiValuesOneFive[m])
        # 将返回值的结果放入列表中
        allYAxisDatas.append(multiValuesOneFive[m])
        savedict = {'group': group_name,
                    'rateByYear': rateByYearOne,
                    'sharpRatio': sharpRatioOne,
                    'maxDown': maxDownOne,
                    'startDate': j,
                    "endDate": k}
        save_dict_list.append(savedict)

    tabledata = pd.DataFrame(save_dict_list)

    # 因为最大回撤时间段需要最大回撤的计算之后，所以在最后进行计算，计算最大回撤时间段,传入三个参数，第一个日期列表，第二个开始时间数字列表，第三个，结束时间数字列表
    # 定义一个存储最大回撤开始和结束组合而成的序列

    tabledata['startDate'] = tabledata['startDate'].apply(lambda x: str(dateList[x]))
    tabledata['endDate'] = tabledata['endDate'].apply(lambda x: str(dateList[x]))
    tabledata['maxDownTimeTerms'] = tabledata['startDate'].str.cat([tabledata.endDate], sep='-')

    # 根据之前算的7个组的年化收益率和最大回撤值来计算收益回撤比，返回的也是一个List列表
    # 计算回撤收益比 先保留三位小数再去绝对值
    tabledata['getByMaxDown'] = (tabledata['rateByYear'] / tabledata['maxDown']).apply(lambda x: abs(round(x + 0.0001, 3)))

    # 展示表格的格式转换
    tabledata['rateByYear'] = tabledata['rateByYear'].apply(lambda x: format(x, '.2%'))
    tabledata['sharpRatio'] = tabledata['sharpRatio'].apply(lambda x: round(x + 0.0001, 2))
    tabledata['maxDown'] = tabledata['maxDown'].apply(lambda x: round(x, 4))
    tabledata['getByMaxDown'] = tabledata['getByMaxDown'].apply(lambda x: format(x, '.2%'))

    return tabledata, dateList, allYAxisDatas


def get_table2_result(dotdict):
    # 获取右边的表格
    # 调用方法拿到所有要求的字段名
    datas = getDatasInStore()
    datasTerms = getDataInTerm(datas, dotdict.startDate, dotdict.endDate)
    dotdict.datas = datasTerms
    columnNames = datasTerms.columns.values
    # 定义一个不需要的列名list const里面的noneed_column
    deleteColumn = np.array(noneed_column)
    columnNames = np.setdiff1d(columnNames, deleteColumn, assume_unique=False)

    table2_dict_list = []

    for columnName in columnNames:
        dotdict.columnName = columnName

        # 拿到1-5和5-1的初始值和累乘值，两个变量都是List，每个List中的每一个项都是List类型
        conditionValuesOneFive, multiValuesOneFive = calcByConditionOneFive(dotdict)
        for i, m, tf in zip(conditionValuesOneFive, multiValuesOneFive, [0, 1]):  # 1-5 和 5-1 共2个
            # 调用计算年化收益率的函数,返回一个数值类型的值
            rateByYearOne = calcRet(conditionValuesOneFive[i])
            # 调用计算最大回撤值的函数，返回一个数值类型的值
            maxDownOne, j, k = create_drawdowns(multiValuesOneFive[m])
            # 将返回值的结果放入列表中
            if tf == 0:
                table2_dict = {"columnName": columnName,
                               "rateByYear": rateByYearOne,
                               "maxDown": maxDownOne
                               }
            if tf == 1:
                table2_dict = {"columnName": '-' + columnName,
                               "rateByYear": rateByYearOne,
                               "maxDown": maxDownOne
                               }
            table2_dict_list.append(table2_dict)
        # 计算每一个指标收益回撤比，两个值1-5 和 5-1
        # 将年化收益率和收益回撤比分别加到List中去
        # 储存所有column的

    table2data = pd.DataFrame(table2_dict_list)

    table2data['getByMaxDown'] = (table2data['rateByYear'] / table2data['maxDown']).apply(lambda x: abs(round(x + 0.0001, 3)))

    # 表格排序，默认按照年化收益率倒叙排列
    table2_data = table2data[["columnName", 'rateByYear', 'getByMaxDown']].sort_values(by="rateByYear", ascending=False)

    # 展示表格的格式转换
    table2_data['rateByYear'] = table2_data['rateByYear'].apply(lambda x: format(x, '.2%'))
    table2_data['getByMaxDown'] = table2_data['getByMaxDown'].apply(lambda x: format(x, '.2%'))

    return table2_data
