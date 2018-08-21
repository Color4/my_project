# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2017/10/11 0011
import os
import shutil
from view.cbk_file import read_data, write_data, mkdir
from view.cbk_common import sort_list, get_time, format_record, base_url, get_soup,  get_table_datas, get_th
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
dict_name = ''
results_dir = 'results'
items_dir = 'items'
jsons_dir = 'jsons'
mkdir(results_dir)
mkdir(jsons_dir, is_remove=False)
mkdir(items_dir, is_remove=False)

__author__ = 'huohuo'

if __name__ == "__main__":
    pass


def get_items(page):

    json_path = 'jsons/page_%d.json' % page
    if os.path.exists(json_path):
        return read_data(json_path)
    url = 'https://www.snpedia.com/index.php?title=Special:Ask&offset=%d' % page
    url += '&limit=500&q=%5B%5BCategory%3AIs+a+genotype%5D%5D&p=mainlabel%3D%2Fformat%3Dtable&po=%3FMagnitude%0A%3FRepute%0A%3FSummary%0A&sort=magnitude&order=desc'
    'https://www.snpedia.com/index.php/Special:Ask/-5B-5BCategory:Is-20a-20snp-5D-5D/-3FMax-20Magnitude/-3FSummary/mainlabel%3D/limit%3D10/order%3Ddesc/sort%3DMax-20Magnitude/offset%3D10/format%3Dtable'
    items, data1, len_trs = get_table_datas(url, 0, base='')

    if len(items) > 0:
        write_data(items, 'items/page_%d.json' % page)
        # write_data(items, 'items/page_%d.xlsx' % page)
    return items


def uniq_list(items):
    items1 = []
    for item in items:
        if item not in items1:
            items1.append(item)
    return items1


n = 1
limit = 100000
total = n * limit / 500
items = []
items2 = []
for i in range(total):
    items1 = get_items(i * 500)
    if items1 not in items:
        items.append(items1)
        items2 += items1
    else:
        msg = format_record('record%d' % (i * 500), i + 1, total)
        print msg, get_time(), items.index(items1)
print len(items2)
write_data(items2, 'results/snpedia.csv')
write_data(items2, 'results/snpedia.json')
