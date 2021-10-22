import pyecharts.options as opts
from pyecharts.charts import Line


def createChart(dateList, allYAxisDatas, title) -> Line:
    dateList = list(map(converttime, dateList))

    c = (
        Line()
        .add_xaxis(dateList)
        .add_yaxis("1.0", allYAxisDatas[0], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False )
        .add_yaxis("2.0", allYAxisDatas[1], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False)
        .add_yaxis("3.0", allYAxisDatas[2], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False)
        .add_yaxis("4.0", allYAxisDatas[3], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False)
        .add_yaxis("5.0", allYAxisDatas[4], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False)
        .add_yaxis("1.0-5.0", allYAxisDatas[5], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False)
        .add_yaxis("5.0-1.0", allYAxisDatas[6], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True,
            ),
            xaxis_opts=opts.AxisOpts(type_="time", boundary_gap=False),
            brush_opts=opts.BrushOpts(tool_box=None),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left='right'),
        )
    )

    return c


def converttime(date):
    date = str(date)
    date = date[0:4]+'-'+date[4:6]+'-'+date[6:8]
    return date

