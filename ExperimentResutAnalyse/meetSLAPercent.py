#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
import xlsxwriter

performanceDataTableName = 'PerformanceData'

def getMeetSLATuple():
    dbcon = getDBConwithCloudExDB()
    selectStat = '''
        SELECT periodNo, breakSLAPercent
        FROM %s
    ''' % performanceDataTableName
    dbcur = dbcon.cursor()
    dbcur.execute(selectStat)
    mslp = []
    periodNo = []
    for item in dbcur:
        periodNo.append(item[0])
        mslp.append(1 - item[1])
    dbcur.close()
    dbcon.close()
    return periodNo, mslp

index, mslp = getMeetSLATuple()

slaCons = [0.95] * len(index)



workbook = xlsxwriter.Workbook('./resultPicture/meetSLAPercentResult.xlsx')

meetSLAPercentSheet = workbook.add_worksheet('meetSLAPercent')

#这个仅仅影响表格中的字体, 表格中字体format有关可以看文档第九章
bold = workbook.add_format({'bold': 1})

headings = ['periodNo', 'meetSLAPercent']

meetSLAPercentSheet.write_row('A1', headings, bold)
meetSLAPercentSheet.write_column('A2', index)
meetSLAPercentSheet.write_column('B2', mslp)
meetSLAPercentSheet.write_column('C2', slaCons)




meetSLAPercentChart = workbook.add_chart({'type': 'scatter'})
meetSLAPercentChart.add_series({
        'categories': '=meetSLAPercent!$A$2:$A$' + str(1 + len(index)),
        'values': '=meetSLAPercent!$B$2:$B$' + str(1 + len(index)),
        'marker': {'type': 'x', 'fill' : {'none': True}, 'size' : 6, 'border': {'color': 'blue'}}
        })


#char 的 setXXX函数可以在文档第十章查，这里是设置图例的字体的方法，font是设置
#char Fonts 可参见16.15
#meetSLAPercentChart.set_legend({'font': {'size':8, 'name':'Times New Roman', 'bold':True}})


meetSLAPercentChart.set_size({'width': 700, 'height': 380})
meetSLAPercentChart.set_legend({'none':True})

slaLineChart = workbook.add_chart({'type': 'line'})
slaLineChart.add_series({
        'categories': '=meetSLAPercent!$A$2:$A$' + str(1 + len(index)),
        'values': '=meetSLAPercent!$C$2:$C$' + str(1 + len(index)),
        'line': {'color': 'red'}
        })

slaLineChart.combine(meetSLAPercentChart)
slaLineChart.set_size({'width': 700, 'height': 380})
slaLineChart.set_legend({'none':True})

#设置X轴
slaLineChart.set_x_axis({
        'name': 'Period Number',
        'name_font': {'size': 15, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 11, 'bold': True, 'name':'Times New Roman'},
        'max': 500,
        'interval_unit': 30,
        'interval_tick': 30
        })
#设置Y轴
slaLineChart.set_y_axis({
        'name': 'Percentage of Requests Meeting The Constraint',
        'name_font': {'size': 15, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 11, 'bold': True, 'name':'Times New Roman'},
        'num_format': '#,##0.00%',
        'max': 1
                })
#meetSLAPercentChart.set_title({'name': 'aaa', 'name_font': {'name': 'Times New Roman', 'size':80}})


meetSLAPercentSheet.insert_chart('E1', slaLineChart)


workbook.close()
