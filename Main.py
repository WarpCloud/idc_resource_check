# -*- coding: utf-8 -*-

import os
import time
from copy import copy

import xlrd
import xlwt
from xlutils.copy import copy

import Config
from Logger import Logger
from client.CpuClient import CpuClient
from client.MemoryClient import MemoryClient
from client.WarpdriveClient import WarpdriveClient

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="Main").getlog()


def init_excel(path):

    wb = xlwt.Workbook()
    sheet = wb.add_sheet("idc_resource")
    value = [["Namespace", "Pod Name", "Cpu Request", "Cpu Limit", "Cpu 24Hour Max Used", "Cpu 24Hour Avg Used", "Memory Request", "Memory Limit", "Memory 24Hour Max Used",
              "Memory 24Hour Avg Used", "Volume Total Request(G)", "Volume Used(G)"]]

    style = xlwt.XFStyle()  # 格式信息
    font = xlwt.Font()  # 字体基本设置
    font.name = u'微软雅黑'
    font.color = 'black'
    font.height = 220  # 字体大小，220就是11号字体，大概就是11*20得来的吧
    style.font = font
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    style.alignment = alignment
    border = xlwt.Borders()  # 给单元格加框线
    border.left = xlwt.Borders.THIN  # 左
    border.top = xlwt.Borders.THIN  # 上
    border.right = xlwt.Borders.THIN  # 右
    border.bottom = xlwt.Borders.THIN  # 下
    border.left_colour = 0x40  # 设置框线颜色，0x40是黑色，颜色真的巨多，都晕了
    border.right_colour = 0x40
    border.top_colour = 0x40
    border.bottom_colour = 0x40
    style.borders = border

    for j in range(0, len(value[0])):
        sheet.write(0, j, value[0][j], style=style)
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


def init_client():

    memoryClient = MemoryClient()
    cpuClient = CpuClient()
    warpClient = WarpdriveClient()

    return memoryClient, cpuClient, warpClient


def get_pod_cpu_metrics(cpuClient, namespace):

    end_time = time.time()
    start_time = end_time - 3600 * 24

    pod_cpu_request = cpuClient.get_namespace_pod_cpu_request(namespace)
    pod_cpu_limit = cpuClient.get_namespace_pod_cpu_limit(namespace)
    pod_cpu_used = cpuClient.get_namespace_pod_cpu_used_range_time(namespace=namespace, start_time=start_time, end_time=end_time, step="150s")

    return pod_cpu_request, pod_cpu_limit, pod_cpu_used


def get_pod_memory_metrics(memoryClient, namespace):

    end_time = time.time()
    start_time = end_time - 3600 * 24

    pod_memory_request = memoryClient.get_namespace_pod_memory_request(namespace)
    pod_memory_limit = memoryClient.get_namespace_pod_memory_limit(namespace)
    pod_memory_used = memoryClient.get_namespace_pod_memory_used_range_time(namespace=namespace, start_time=start_time, end_time=end_time, step="150s")

    return pod_memory_request, pod_memory_limit, pod_memory_used


def get_all_namespaces():

    namespaces_list = Config.NAMESPACE.split(",")
    namespaces_black_list = Config.NAMESPACE_BLACK_LIST.split(",")
    for i in namespaces_black_list:
        if namespaces_list.__contains__(i):
            namespaces_list.remove(i)

    return namespaces_list


def get_pod_volume_metrics(warpClient, namespace):

    pod_volume_total_request = warpClient.get_volume_total_requests(namespace)
    pod_volume_used = warpClient.get_volume_used(namespace)

    return pod_volume_total_request, pod_volume_used


def get_namespace_resources_dict(namespaces_list, memoryClient, cpuClient, warpClient):

    namespace_pod_dict = dict()
    for namespace in namespaces_list:

        pod_cpu_mem_disk_dict = dict()

        pod_cpu_request, pod_cpu_limit, pod_cpu_used = get_pod_cpu_metrics(cpuClient, namespace)

        pod_memory_request, pod_memory_limit, pod_memory_used = get_pod_memory_metrics(memoryClient, namespace)

        pod_volume_total_request, pod_volume_used = get_pod_volume_metrics(warpClient, namespace)

        for name, values in pod_cpu_used.items():
            cpu_request_value = str(pod_cpu_request[str(name)]) if pod_cpu_request.has_key(str(name)) else "NULL"
            cpu_limit_value = str(pod_cpu_limit[str(name)]) if pod_cpu_limit.has_key(str(name)) else "NULL"
            cpu_hour24_max_value = str(values['max_value'])
            cpu_hour24_avg_value = str(values['avg_value'])

            mem_request_value = str(pod_memory_request[str(name)]) if pod_memory_request.has_key(str(name)) else "NULL"
            mem_limit_value = str(pod_memory_limit[str(name)]) if pod_memory_limit.has_key(str(name)) else "NULL"
            mem_hour24_max_value = str(pod_memory_used[str(name)]['max_value']) if pod_memory_used.has_key(
                str(name)) else "NULL"
            mem_hour24_avg_value = str(pod_memory_used[str(name)]['avg_value']) if pod_memory_used.has_key(
                str(name)) else "NULL"

            volume_total_value = str(pod_volume_total_request[str(name)]) if pod_volume_total_request.has_key(
                str(name)) else "NULL"
            volume_used_value = str(pod_volume_used[str(name)]) if pod_volume_used.has_key(str(name)) else "NULL"

            if cpu_request_value == cpu_limit_value == mem_request_value == mem_limit_value == volume_total_value == volume_used_value == "NULL":
                continue

            pod_cpu_mem_disk_dict[str(name)] = {'cpu_request_value': cpu_request_value,
                                                'cpu_limit_value': cpu_limit_value,
                                                'cpu_hour24_max_value': cpu_hour24_max_value,
                                                'cpu_hour24_avg_value': cpu_hour24_avg_value,
                                                'mem_request_value': mem_request_value,
                                                'mem_limit_value': mem_limit_value,
                                                'mem_hour24_max_value': mem_hour24_max_value,
                                                'mem_hour24_avg_value': mem_hour24_avg_value,
                                                'volume_total_request': volume_total_value,
                                                'volume_used': volume_used_value
                                                }

        namespace_pod_dict[namespace] = pod_cpu_mem_disk_dict

    return namespace_pod_dict


if __name__ == '__main__':

    logger.info("****************************************************")

    logger.info("Begin Check Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n")
    logger.info("Namespace: %s " % (str(Config.NAMESPACE)))
    logger.info("Namespace Black List: %s " % (str(Config.NAMESPACE_BLACK_LIST)))
    logger.info("Promethues Url: %s \n" % (str(Config.PROMETHEUS_URL)))

    memoryClient, cpuClient, warpClient = init_client()

    namespace_pod_dict = get_namespace_resources_dict(get_all_namespaces(), memoryClient, cpuClient, warpClient)

    excel_path = os.path.join(Config.EXPORT_EXCEL_PATH_NAME)

    init_excel(excel_path)

    for namespace, pod_cpu_mem_disk_dict in namespace_pod_dict.items():

        values = []
        for pod_name, pod_values_dict in pod_cpu_mem_disk_dict.items():

            cpu_request_value = str(pod_values_dict['cpu_request_value'])
            cpu_limit_value = str(pod_values_dict['cpu_limit_value'])
            cpu_hour24_max_value = str(pod_values_dict['cpu_hour24_max_value'])
            cpu_hour24_avg_value = str(pod_values_dict['cpu_hour24_avg_value'])

            mem_request_value = str(pod_values_dict['mem_request_value'])
            mem_limit_value = str(pod_values_dict['mem_limit_value'])
            mem_hour24_max_value = str(pod_values_dict['mem_hour24_max_value'])
            mem_hour24_avg_value = str(pod_values_dict['mem_hour24_avg_value'])

            volume_total_request = str(pod_values_dict['volume_total_request'])
            volume_used = str(pod_values_dict['volume_used'])

            values.append([
                str(namespace),
                str(pod_name),
                cpu_request_value, cpu_limit_value, cpu_hour24_max_value, cpu_hour24_avg_value,
                mem_request_value, mem_limit_value, mem_hour24_max_value, mem_hour24_avg_value,
                volume_total_request, volume_used
            ])

        write_excel_xls_append(excel_path, values)

    logger.info("****************************************************\n")
