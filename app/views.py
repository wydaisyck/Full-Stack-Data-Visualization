from app import app
from flask import render_template, redirect, jsonify, request, url_for
from app.entityOB.DotDict import DotDict
from app.utils.get_table_result import get_table1_result, get_table2_result
from app.utils.utils import convert_time, get_ini_time, initimepicker
from app.utils.myecharts import createChart
from app.utils.guiyinpics import getNameListsGuiyin, getGuiyinpics, return_img_stream, get_img_list
from app.utils.const import para_name_list
import os


colname = '12m_high/low'
universe = ""
frequency = ""
product_name = ""
para_name = ""
# 默认时间是最近一年
ini_start_time, ini_end_time = get_ini_time()

category_dict = DotDict()
category_dict.columnName = colname
category_dict.startDate = ini_start_time
category_dict.endDate = ini_end_time

category_dict2 = DotDict()
category_dict2.startDate = ini_start_time
category_dict2.endDate = ini_end_time


@app.route('/')
def hello_world():
    return redirect(url_for('createindex', paraname=para_name_list[0]))


@app.route('/<paraname>')
def createindex(paraname):
    guiyindict = getNameListsGuiyin()
    dict_keys = list(guiyindict.keys())
    global universe
    global frequency
    universe = paraname[:-3]
    frequency = paraname[-1]

    global category_dict
    global category_dict2
    category_dict.universe = universe
    category_dict.frequency = frequency

    category_dict2.universe = universe
    category_dict2.frequency = frequency

    inidate = initimepicker()
    ini_dict = {"inidate": inidate}
    return render_template('index.html', dict_keys=dict_keys, para_name_list=para_name_list, inidate=ini_dict)


@app.route("/getpics/<allname>")
def guiyinpics(allname):
    guiyindict = getNameListsGuiyin()
    dict_keys = list(guiyindict.keys())

    global product_name
    product_name = allname
    img_list, datelist = get_img_list(guiyindict, product_name)

    return render_template("pics.html", img_stream=img_list, datelist=datelist, dict_keys=dict_keys, para_name_list=para_name_list)


@app.route('/send_time', methods=['GET'])
def send_time():
    time = request.args['time']
    start_time, end_time = convert_time(time)
    global category_dict
    global category_dict2
    category_dict.startDate = start_time
    category_dict.endDate = end_time

    category_dict2.startDate = start_time
    category_dict2.endDate = end_time
    return "send time message successfully"


@app.route('/send_colname', methods=['GET'])
def send_colName():
    colName = request.args['colName']
    global colname
    colname = colName

    global category_dict
    category_dict.columnName = colname
    global category_dict2
    category_dict2.columnName = colname

    return "send column name message successfully"


@app.route('/mychart')
def create_mychart():
    global category_dict
    dateList = get_table1_result(category_dict)[1]
    allYAxisDatas = get_table1_result(category_dict)[2]

    colname = category_dict.columnName
    c = createChart(dateList, allYAxisDatas, colname)
    return c.dump_options_with_quotes()


@app.route('/get_table1_result')
def get_search_result1():
    global category_dict
    res1 = get_table1_result(category_dict)[0]
    resdict1 = res1.to_dict('records')

    return jsonify(resdict1)


@app.route('/get_table2_result')
def get_search_result2():
    global category_dict2
    res2 = get_table2_result(category_dict2)
    resdict2 = res2.to_dict('records')
    return jsonify(resdict2)


@app.route('/get_time_pics_updated', methods=['GET', 'POST'])
def get_time_pics_updated():
    timeperiod = request.get_json()
    global product_name
    key = product_name
    img_list = {}
    # 默认显示date最近的一个周
    path, picslist = getGuiyinpics(key, timeperiod['timeperiod'])
    for pic in picslist:
        img_path = os.path.join(path, pic)
        img_stream = return_img_stream(img_path)
        img_list[pic[:-4]] = img_stream

    return jsonify(img_list)

