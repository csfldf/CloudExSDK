#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
import xlsxwriter

performanceDataTableName = 'PerformanceData'

def getVMsInfoTuple():
    dbcon = getDBConwithCloudExDB()
    selectStat = '''
        SELECT vmNumbers, shouldVMNumbers, periodNo
        FROM %s
    ''' % performanceDataTableName
    dbcur = dbcon.cursor()
    dbcur.execute(selectStat)
    real = []
    should = []
    index = []
    for item in dbcur:
        real.append(item[0])
        should.append(item[1])
        index.append(item[2])
    dbcur.close()
    dbcon.close()
    return real, should, index

real, should, index = getVMsInfoTuple()

workbook = xlsxwriter.Workbook('./resultPicture/vmNumbersResult.xlsx')

vmNumbersSheet = workbook.add_worksheet('vmNumbers')

#这个仅仅影响表格中的字体, 表格中字体format有关可以看文档第九章
bold = workbook.add_format({'bold': 1})

headings = ['index', 'Needed', 'Available']

vmNumbersSheet.write_row('A1', headings, bold)
vmNumbersSheet.write_column('A2', index)
vmNumbersSheet.write_column('B2', should)
vmNumbersSheet.write_column('C2', real)




vmNumbersChart = workbook.add_chart({'type': 'line'})
vmNumbersChart.add_series({
        'categories': '=vmNumbers!$A$2:$A$' + str(1 + len(index)),
        'values': '=vmNumbers!$B$2:$B$' + str(1 + len(index)),
        'name': '=vmNumbers!$B$1',
        })

vmNumbersChart.add_series({
        'categories': '=vmNumbers!$A$2:$A$' + str(1 + len(index)),
        'values': '=vmNumbers!$C$2:$C$' + str(1 + len(index)),
        'name': '=vmNumbers!$C$1',
        })


#char 的 setXXX函数可以在文档第十章查，这里是设置图例的字体的方法，font是设置
#char Fonts 可参见16.15
#vmNumbersChart.set_legend({'font': {'size':8, 'name':'Times New Roman', 'bold':True}})


vmNumbersChart.set_size({'width': 700, 'height': 370})
#vmNumbersChart.set_legend({'font': {'size': 14, 'name': 'Times New Roman', 'bold': True}, 'position': 'bottom'})
vmNumbersChart.set_legend({'font': {'size': 14, 'name': 'Times New Roman', 'bold': True}})

vmNumbersChart.set_x_axis({
        'name': 'Period Number',
        'name_font': {'size': 14, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 11, 'bold': True, 'name':'Times New Roman'},
        'max': 500,
        'interval_unit': 30,
        'interval_tick': 30
        })

#设置Y轴
vmNumbersChart.set_y_axis({
        'name': 'The Number of VMs',
        'name_font': {'size': 14, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 11, 'bold': True, 'name':'Times New Roman'},
        'num_format': '#,##'
        })

vmNumbersSheet.insert_chart('E1', vmNumbersChart)


workbook.close()
