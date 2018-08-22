# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2017/9/15 0015
import random
import json
import os
import platform
import xlrd
from pyExcelerator import *
import shutil
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'huohuo'

if __name__ == "__main__":
    pass


def write_data(data, file_name, **kwargs):
    file_type = file_name.split('.')[1]
    if file_type == 'csv':
        f1 = open(file_name, 'wb')
        f_csv = csv.DictWriter(f1, data[0].keys())
        f_csv.writeheader()
        f_csv.writerows(data)
        f1.close()
    elif file_type in ['xls', 'xlsx']:
        w = Workbook()  #创建一个工作簿
        datas = [{'data': data, 'sheet_name': 'Sheet1'}]
        if 'datas' in kwargs:
            datas = kwargs['datas']
        # print len(datas)
        for ss in range(len(datas)):
            s = datas[ss]
            sheet_name = 'Sheet%d' % (ss + 1) if 'sheet_name' not in s else s['sheet_name']
            data = s['data']
            ws = w.add_sheet(sheet_name)  # 创建一个工作表
            if len(data) > 0:
                if type(data[0]) in [str, list, unicode]:
                    for j in range(len(data)):
                        row = data[j] if type(data[j]) == str else data[j].split('\t')
                        for k in range(len(row)):
                            ws.write(j, k, row[k])
                else:
                    keys = data[0].keys()
                    thead = keys
                    if 'keys' in kwargs:
                        thead = kwargs['keys']
                    for i in range(len(thead)):
                        ws.write(0, i, thead[i])  #在1行1列写入bit
                    for j in range(len(data)):
                        for k in range(len(keys)):
                            v = '' if keys[k] not in data[j] else str(data[j][keys[k]])
                            if v is None:
                                v = ''
                            # if type(v) is unicode:
                            #     v = v[:30000]
                            # try:
                            unencoded_signs = [['‘‘', '"']]
                            for s in unencoded_signs:
                                v = v.replace(s[0], s[1])
                            try:
                                ws.write(j+1, k, v) #在2行1列写入xuan
                            except:
                                print j+1, k
                            #     print len(v), data[j]['gene'], keys[k], type(v)
        w.save(file_name)  #保存
    else:
        f = file(file_name, 'w')
        if file_type == 'json':
            f.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
        else:
            f.write(data)
        f.close()


def read_data(file_name, **kwargs):
    file_type = file_name.split('.')[1]
    if file_type in ['xls', 'xlsx']:
        data = []
        bk = xlrd.open_workbook(file_name, encoding_override='utf-8')
        sheet_name = 'Sheet1' if 'sheet_name' not in kwargs else kwargs['sheet_name']
        try:
            sh = bk.sheet_by_name(sheet_name)
        except:
            print "no sheet in %s named %s" % (file_name, sheet_name)
            return []
        nrows = sh.nrows
        ncols = sh.ncols
        if 'keys' in kwargs:
            keys = kwargs['keys']
        else:
            keys = []
            for i in range(ncols):
                keys.append(sh.cell_value(0, i))
        for ii in range(1, nrows):
            item = {}
            for j in range(ncols):
                item[keys[j]] = sh.cell_value(ii, j)
            if item not in data:
                data.append(item)
        return data
    f = open(file_name, 'r')
    text = f.read()
    f.close()
    if file_type == 'json':
        return json.loads(text)
    return text


def mkdir(path, is_remove=False):
    if path == '':
        return True
    if is_remove:
        remove_dir(path)
    path = path.strip()
    is_exists=os.path.exists(path)
    ss = platform.system()
    if ss == 'Linux':
        sign = '/'
    else:
        sign = '\\'
    # 判断结果
    path = path.rstrip(sign)
    if not is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print path + u' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + u' 目录已存在'
        return False 
    

def remove_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        
        
def write_result(data, result_file, **kwargs):
    write_data(data, result_file + '.json')
    excel_data = [{'data': data, 'sheet_name': 'sheet1'}]
    for k in kwargs.keys():
        if k.lower().startswith('sheet'):
            excel_data.append({'data': kwargs[k], 'sheet_name': k})
    write_data(data, result_file + '.xlsx', datas=excel_data)