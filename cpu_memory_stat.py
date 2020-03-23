# -*- coding: utf-8 -*-
import argparse
import os

import xlrd
import xlwt
from xlutils.copy import copy


def parse_argument():
    global args
    parse = argparse.ArgumentParser()
    parse.add_argument("-c", "--sc_file_dir", help="sc_file_dir", required=True, dest='sc_file_dir')
    parse.add_argument("-d", "--dest_file_dir", help="dest_file_dir", default="/tmp/", dest='dest_file_dir')

    parse.set_defaults(user_define=False)

    args = parse.parse_args()
    return args


def init_excel(path):

    wb = xlwt.Workbook()
    sheet = wb.add_sheet("cpu_memory")
    value = [["Namespace", "Component", "Cpu_Request", "Cpu_Limits", "Memory_Request", "Memory_Limits"]]

    style = xlwt.XFStyle()
    border = xlwt.Borders()  # 给单元格加框线
    border.left = xlwt.Borders.THIN  # 左
    border.top = xlwt.Borders.THIN  # 上
    border.right = xlwt.Borders.THIN  # 右
    border.bottom = xlwt.Borders.THIN  # 下
    border.left_colour = 0x40  # 设置框线颜色，0x40是黑色，颜色真的巨多，都晕了
    border.right_colour = 0x40
    border.top_colour = 0x40
    border.bottom_colour = 0x40

    for j in range(0, len(value[0])):
        sheet.write(0, j, value[0][j], style)
    wb.save(path)
    print("write data success")


def write_excel_xls_append(path, value):
    index = len(value)
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheets[0])
    rows_old = worksheet.nrows
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(0)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])
    new_workbook.save(path)
    print("append  data success")


if __name__ == '__main__':

    global sc_file_dir, dest_file_dir

    parse_argument()

    sc_file_dir = str(args.sc_file_dir)
    dest_file_dir = str(args.dest_file_dir)

    excel_path = os.path.join(dest_file_dir, "idc_resource_cpu_memory.xls")

    init_excel(excel_path)

    list = os.listdir(sc_file_dir)
    for i in range(0, len(list)):

        values = []
        path = os.path.join(sc_file_dir, list[i])
        if os.path.isfile(path):
            with open(path, 'r') as f:
                for line in f:
                    ns = str(list[i]).split("_")[1].split(".")[0]
                    content = line.strip('\n').split(",")
                    comp_name = content[0].split("/")[1]
                    cpu_request = content[1]
                    cpu_limits = content[2]
                    memory_request = content[3]
                    memory_limits = content[4]
                    values.append([ns, comp_name, cpu_request, cpu_limits, memory_request, memory_limits])

            write_excel_xls_append(excel_path, values)
            values = []