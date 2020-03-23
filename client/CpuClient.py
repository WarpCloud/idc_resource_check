# -*- coding: utf-8 -*-
import time

import Config
from Logger import Logger
from util.CpuUtil import CpuUtil

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="CpuClient").getlog()


def compare_max_values(pod_value):
    return float(pod_value.values()[0]['max_value'])


class CpuClient(object):

    def __init__(self):
        pass

    def get_all_node_now_cpu_used(self):

        status, data_list = CpuUtil.get_node_cpu_used("")
        if str(status) != "success":
            logger.error("Cannot Get Node Cpu Metircs")
            raise Exception("Cannot Get Node Cpu Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Cpu Metircs Is Empty")
            raise Exception("Get Node Memory Cpu Is Empty")

        ip_value_dict = dict()
        for data in data_list:
            tmp_ip = str(data['metric']['instance']).split(":")[0]
            tmp_value = str(data['value'][1])
            ip_value_dict[tmp_ip] = tmp_value

        return ip_value_dict

    def get_one_node_now_cpu_used(self, instance):

        if not str(instance).__contains__(":9100"):
            instance = str(instance).strip(" ") + ":9100"

        status, data_list = CpuUtil.get_node_cpu_used(instance)
        if str(status) != "success":
            logger.error("Get One Node Cpu Metircs Is Empty")
            raise Exception("Cannot Get One Node Cpu Metircs")

        if len(data_list) == 0:
            logger.error("Get One Node Cpu Metircs Is Empty")
            raise Exception("Get One Node Cpu Metircs Is Empty")

        data = data_list[0]
        tmp_ip = str(data['metric']['instance']).split(":")[0]
        tmp_value = str(data['value'][1])

        return {tmp_ip : tmp_value}

    def get_all_node_cpu_used_range_time(self, start_time, end_time, step="30s"):

        status, data_list = CpuUtil.get_node_cpu_used_range_time("", start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get Node Cpu Metircs")
            raise Exception("Cannot Get Node Cpu Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Cpu Metircs Is Empty")
            raise Exception("Get Node Cpu Metircs Is Empty")

        ip_value_dict = dict()
        for data in data_list:
            max_used_value = total_used_value = avg_used_value = 0
            tmp_ip = str(data['metric']['instance']).split(":")[0]
            for value in data['values']:
                tmp_value = float(str(value[1]))
                max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
                total_used_value = float(total_used_value) + tmp_value
            ip_value_dict[tmp_ip] = {"max_value": str(max_used_value), "avg_value": str(total_used_value / len(data['values']))}

        return ip_value_dict

    def get_one_node_cpu_used_range_time(self, instance, start_time, end_time, step="30s"):

        if not str(instance).__contains__(":9100"):
            instance = str(instance).strip(" ") + ":9100"

        status, data_list = CpuUtil.get_node_cpu_used_range_time(instance, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get One Node Cpu Metircs")
            raise Exception("Cannot Get One Node Cpu Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Cpu Metircs Is Empty")
            raise Exception("Get Node Cpu Metircs Is Empty")

        data = data_list[0]
        max_used_value = total_used_value = avg_used_value = 0
        tmp_ip = str(data['metric']['instance']).split(":")[0]
        for value in data['values']:
            tmp_value = float(str(value[1]))
            max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
            total_used_value = float(total_used_value) + tmp_value

        return {tmp_ip: {"max_value": str(max_used_value), "avg_value": str(total_used_value / len(data['values']))}}

    def get_namespace_pod_cpu_used(self, namespace):

        status, data_list = CpuUtil.get_namespace_cpu_used(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Cpu Metircs")
            raise Exception("Cannot Get Namespace Cpu Metircs")

        if len(data_list) == 0:
            logger.error("Get Namespace Cpu Metircs Is Empty")
            raise Exception("Get Namespace Cpu Metircs Is Empty")

        pod_value_dict = dict()
        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict

    def get_namespace_pod_cpu_used_range_time(self, namespace, start_time, end_time, step="30s"):

        status, data_list = CpuUtil.get_namespace_cpu_used_range_time(namespace, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Cpu Metircs")
            raise Exception("Cannot Get Namespace Cpu Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.warn("Get Namespace Cpu Metircs Is Empty")
            return pod_value_dict

        for data in data_list:
            max_used_value = total_used_value = avg_used_value = 0
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            for value in data['values']:
                tmp_value = float(str(value[1]))
                max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
                total_used_value = float(total_used_value) + tmp_value
            pod_value_dict[tmp_podname] = {"max_value": str(max_used_value), "avg_value": str(total_used_value / len(data['values']))}

        return pod_value_dict

    def get_namespace_pod_cpu_used_top_n(self, namespace, start_time, end_time, step="30s", top_n=1):

        status, data_list = CpuUtil.get_namespace_cpu_used_range_time(namespace, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Namespace Memory Metircs Is Empty")
            raise Exception("Get Namespace Memory Metircs Is Empty")

        pod_value_list = []
        for data in data_list:
            max_used_value = total_used_value = avg_used_value = 0
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])

            for value in data['values']:
                tmp_value = float(str(value[1]))
                max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
                total_used_value = float(total_used_value) + tmp_value
            pod_value_list.append({tmp_podname: {"max_value": str(max_used_value),
                                                 "avg_value": str(total_used_value / len(data['values']))}})

        pod_value_list.sort(key=compare_max_values, reverse=True)

        pod_value_dict = dict()
        for i in range(0, int(top_n)):
            pod_value_dict.update(pod_value_list[i])

        return pod_value_dict

    def get_namespace_pod_cpu_limit(self, namespace):

        status, data_list = CpuUtil.get_namespace_pod_cpu_limit(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Cpu Metircs")
            raise Exception("Cannot Get Namespace Cpu Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.warn("Get Namespace Cpu Metircs Is Empty")
            return pod_value_dict

        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict

    def get_namespace_pod_cpu_request(self, namespace):

        status, data_list = CpuUtil.get_namespace_pod_cpu_request(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Cpu Metircs")
            raise Exception("Cannot Get Namespace Cpu Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.warn("Get Namespace Cpu Metircs Is Empty")
            return pod_value_dict

        pod_value_dict = dict()
        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict
