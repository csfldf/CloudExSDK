#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
import xlsxwriter

performanceDataTableName = 'PerformanceData'

def getAvailabilityTup():
    dbcon = getDBConwithCloudExDB()
    selectStat = '''
        SELECT periodNo, availability
        FROM %s
    ''' % performanceDataTableName
    dbcur = dbcon.cursor()
    dbcur.execute(selectStat)
    periodNo = []
    av = []
    for item in dbcur:
        periodNo.append(item[0])
        av.append(item[1])
    dbcur.close()
    dbcon.close()
    return periodNo, av

index, av = getAvailabilityTup()

slaCons = [0.975] * len(index)



workbook = xlsxwriter.Workbook('./resultPicture/availabilityResult.xlsx')

availabilitySheet = workbook.add_worksheet('availability')

#这个仅仅影响表格中的字体, 表格中字体format有关可以看文档第九章
bold = workbook.add_format({'bold': 1})

headings = ['periodNo', 'availability']

availabilitySheet.write_row('A1', headings, bold)
availabilitySheet.write_column('A2', index)
availabilitySheet.write_column('B2', av)
availabilitySheet.write_column('C2', slaCons)




availabilityChart = workbook.add_chart({'type': 'scatter'})
availabilityChart.add_series({
        'categories': '=availability!$A$2:$A$' + str(1 + len(index)),
        'values': '=availability!$B$2:$B$' + str(1 + len(index)),
        'marker': {'type': 'x', 'fill' : {'none': True}, 'size' : 4, 'border': {'color': 'blue'}}
        })


#char 的 setXXX函数可以在文档第十章查，这里是设置图例的字体的方法，font是设置
#char Fonts 可参见16.15
#availabilityChart.set_legend({'font': {'size':8, 'name':'Times New Roman', 'bold':True}})


availabilityChart.set_size({'width': 700, 'height': 380})
availabilityChart.set_legend({'none':True})

slaLineChart = workbook.add_chart({'type': 'line'})
slaLineChart.add_series({
        'categories': '=availability!$A$2:$A$' + str(1 + len(index)),
        'values': '=availability!$C$2:$C$' + str(1 + len(index)),
        'line': {'color': 'red'}
        })

slaLineChart.combine(availabilityChart)
slaLineChart.set_size({'width': 700, 'height': 380})
slaLineChart.set_legend({'none':True})

#设置X轴
slaLineChart.set_x_axis({
        'name': 'Period Number',
        'name_font': {'size': 15, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 11, 'bold': True, 'name':'Times New Roman'},
        'interval_unit': 30,
        'interval_tick': 30
        })
#设置Y轴
slaLineChart.set_y_axis({
        'name': 'Availability of the Cloud Application',
        'name_font': {'size': 15, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 11, 'bold': True, 'name':'Times New Roman'},
        'num_format': '#,##0.00%',
        'max': 1
                })
#availabilityChart.set_title({'name': 'aaa', 'name_font': {'name': 'Times New Roman', 'size':80}})


availabilitySheet.insert_chart('E1', slaLineChart)


workbook.close()
