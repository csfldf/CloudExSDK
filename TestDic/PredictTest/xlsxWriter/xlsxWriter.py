#!/usr/bin/env python
# encoding: utf-8

import shelve
import re
import xlsxwriter

aindex = []
bindex = []
index = []
f = open('./testTxt.txt')
indexCount = 1
for line in f:
    sl = re.split(r'\s+', line)
    aindex.append(int(sl[0]))
    bindex.append(int(sl[1]))
    index.append(indexCount)
    indexCount += 1
f.close()
workbook = xlsxwriter.Workbook('../../DataFile/xlsxWriterTest.xlsx')

testSheet = workbook.add_worksheet('test')

#这个仅仅影响表格中的字体, 表格中字体format有关可以看文档第九章
bold = workbook.add_format({'bold': 1})

headings = ['index', 'a', 'b']

testSheet.write_row('A1', headings, bold)
testSheet.write_column('A2', index)
testSheet.write_column('B2', aindex)
testSheet.write_column('C2', bindex)




testChart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
testChart.add_series({
        'name': '=test!$B$1',
        'categories': '=test!$A$2:$A$' + str(1 + len(index)),
        'values': '=test!$B$2:$B$' + str(1 + len(index)),
        'fill':{'color': 'yellow'}
        })

testChart.add_series({
        'name': '=test!$C$1',
        'categories': '=test!$A$2:$A$' + str(1 + len(index)),
        'values': '=test!$C$2:$C$' + str(1 + len(index))})

#char 的 setXXX函数可以在文档第十章查，这里是设置图例的字体的方法，font是设置
#char Fonts 可参见16.15
testChart.set_legend({'font': {'size':8, 'name':'Times New Roman', 'bold':True}})


testChart.set_size({'width': 700, 'height': 400})

#设置X轴
testChart.set_x_axis({
        'name': 'xzhou',
        'name_font': {'size': 8, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 8, 'bold': True, 'name':'Times New Roman'},
        'num_format': '#,##',
        'interval_tick': 3
                })
#设置Y轴
testChart.set_y_axis({
        'name': 'yzhou',
        'name_font': {'size': 8, 'bold': True, 'name':'Times New Roman'},
        'num_font': {'size': 8, 'bold': True, 'name':'Times New Roman'},
        'num_format': '#,##'
                })
#testChart.set_title({'name': 'aaa', 'name_font': {'name': 'Times New Roman', 'size':80}})
testSheet.insert_chart('E1', testChart)


workbook.close()
