#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
import xlsxwriter

workloadVMMapTableName = 'WorkloadVMMap'

def getAllMapTuple():
    dbcon = getDBConwithCloudExDB()
    selectStat = '''
        SELECT vmNumbers, workloadLevel
        FROM %s
    ''' % workloadVMMapTableName
    dbcur = dbcon.cursor()
    dbcur.execute(selectStat)
    mapInfoList = [0] * 11
    for item in dbcur:
        if item[0] > 10:
            break

        if mapInfoList[item[0]] < item[1]:
            mapInfoList[item[0]] = item[1]
    dbcur.close()
    dbcon.close()
    mapInfoList.pop(0)
    return mapInfoList

mil = getAllMapTuple()


index = range(1, 11)

workbook = xlsxwriter.Workbook('./resultPicture/workloadVMMapResult.xlsx')

vmMapSheet = workbook.add_worksheet('vmMap')

#这个仅仅影响表格中的字体, 表格中字体format有关可以看文档第九章
bold = workbook.add_format({'bold': 1})

headings = ['vmNumbers', 'workloadLevel']

vmMapSheet.write_row('A1', headings, bold)
vmMapSheet.write_column('A2', index)
vmMapSheet.write_column('B2', mil)




vmMapChart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
vmMapChart.add_series({
        'categories': '=vmMap!$A$2:$A$' + str(1 + len(index)),
        'values': '=vmMap!$B$2:$B$' + str(1 + len(index)),
        })


#char 的 setXXX函数可以在文档第十章查，这里是设置图例的字体的方法，font是设置
#char Fonts 可参见16.15
#vmMapChart.set_legend({'font': {'size':8, 'name':'Times New Roman', 'bold':True}})


vmMapChart.set_size({'width': 700, 'height': 380})
vmMapChart.set_legend({'none':True})

#设置X轴
vmMapChart.set_x_axis({
        'name': 'Number of VMs',
        'name_font': {'size': 15, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 12, 'bold': True, 'name':'Times New Roman'},
        'max': 10.5,
        'min': 0,
        'major_unit': 1
                })
#设置Y轴
vmMapChart.set_y_axis({
        'name': 'Workload Level (step size:1000)',
        'name_font': {'size': 15, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 12, 'bold': True, 'name':'Times New Roman'},
        'num_format': '#,##'
                })
#vmMapChart.set_title({'name': 'aaa', 'name_font': {'name': 'Times New Roman', 'size':80}})
vmMapSheet.insert_chart('E1', vmMapChart)


workbook.close()
