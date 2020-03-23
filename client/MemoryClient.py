# -*- coding: utf-8 -*-
import time

import Config
from Logger import Logger
from util.MemoryUtil import MemoryUtil

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="MemoryClient").getlog()


def compare_max_values(pod_value):
    return float(pod_value.values()[0]['max_value'])


class MemoryClient(object):

    def __init__(self):
        pass

    def get_all_node_memory_total(self):

        status, data_list = MemoryUtil.get_node_memory_total("")
        if str(status) != "success":
            logger.error("Cannot Get Node Memory Metircs")
            raise Exception("Cannot Get Node Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Memory Metircs Is Empty")
            raise Exception("Get Node Memory Metircs Is Empty")

        ip_value_dict = dict()
        for data in data_list:
            tmp_ip = str(data['metric']['instance']).split(":")[0]
            tmp_value = str(data['value'][1])
            ip_value_dict[tmp_ip] = tmp_value

        return ip_value_dict

    def get_all_node_now_memory_used(self):

        status, data_list = MemoryUtil.get_node_memory_used("")
        if str(status) != "success":
            logger.error("Cannot Get Node Memory Metircs")
            raise Exception("Cannot Get Node Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Memory Metircs Is Empty")
            raise Exception("Get Node Memory Metircs Is Empty")

        ip_value_dict = dict()
        for data in data_list:
            tmp_ip = str(data['metric']['instance']).split(":")[0]
            tmp_value = str(data['value'][1])
            ip_value_dict[tmp_ip] = tmp_value

        return ip_value_dict

    def get_one_node_now_memory_used(self, instance):

        if not str(instance).__contains__(":9100"):
            instance = str(instance).strip(" ") + ":9100"

        status, data_list = MemoryUtil.get_node_memory_used(instance)
        if str(status) != "success":
            logger.error("Get One Node Memory Metircs Is Empty")
            raise Exception("Cannot Get One Node Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get One Node Memory Metircs Is Empty")
            raise Exception("Get One Node Memory Metircs Is Empty")

        data = data_list[0]
        tmp_ip = str(data['metric']['instance']).split(":")[0]
        tmp_value = str(data['value'][1])

        return {tmp_ip : tmp_value}

    def get_all_node_memory_used_range_time(self, start_time, end_time, step="30s"):

        status, data_list = MemoryUtil.get_node_memory_used_range_time("", start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get Node Memory Metircs")
            raise Exception("Cannot Get Node Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Memory Metircs Is Empty")
            raise Exception("Get Node Memory Metircs Is Empty")

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

    def get_one_node_memory_used_range_time(self, instance, start_time, end_time, step="30s"):

        if not str(instance).__contains__(":9100"):
            instance = str(instance).strip(" ") + ":9100"

        status, data_list = MemoryUtil.get_node_memory_used_range_time(instance, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get One Node Memory Metircs")
            raise Exception("Cannot Get One Node Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Memory Metircs Is Empty")
            raise Exception("Get Node Memory Metircs Is Empty")

        data = data_list[0]
        max_used_value = total_used_value = avg_used_value = 0
        tmp_ip = str(data['metric']['instance']).split(":")[0]
        for value in data['values']:
            tmp_value = float(str(value[1]))
            max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
            total_used_value = float(total_used_value) + tmp_value

        return {tmp_ip: {"max_value": str(max_used_value), "avg_value": str(total_used_value / len(data['values']))}}

    def get_namespace_pod_memory_used(self, namespace):

        status, data_list = MemoryUtil.get_namespace_memory_used(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Namespace Memory Metircs Is Empty")
            raise Exception("Get Namespace Memory Metircs Is Empty")

        pod_value_dict = dict()
        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict

    def get_namespace_pod_memory_used_range_time(self, namespace, start_time, end_time, step="30s"):

        status, data_list = MemoryUtil.get_namespace_memory_used_range_time(namespace, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.error("Get Namespace Memory Metircs Is Empty")
            return pod_value_dict

        for data in data_list:
            max_used_value = total_used_value = avg_used_value = 0
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_instance = str(data['metric']['instance']).split(":")[0]
            for value in data['values']:
                tmp_value = float(str(value[1]))
                max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
                total_used_value = float(total_used_value) + tmp_value
            pod_value_dict[tmp_podname] = {"host_ip": tmp_instance, "max_value": str(max_used_value), "avg_value": str(total_used_value / len(data['values']))}

        return pod_value_dict

    def get_namespace_specify_pod_memory_used_range_time(self, namespace, pod_name_prefix, start_time, end_time, step="30s"):

        status, data_list = MemoryUtil.get_namespace_memory_used_range_time(namespace, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Namespace Memory Metircs Is Empty")
            raise Exception("Get Namespace Memory Metircs Is Empty")

        pod_value_dict = dict()
        for data in data_list:
            max_used_value = total_used_value = 0
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            if not tmp_podname.startswith(str(pod_name_prefix)):
                continue
            tmp_instance = str(data['metric']['instance']).split(":")[0]
            for value in data['values']:
                tmp_value = float(str(value[1]))
                max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
                total_used_value = float(total_used_value) + tmp_value

            pod_value_dict[tmp_podname] = {"host_ip": tmp_instance, "max_value": str(max_used_value), "avg_value": str(total_used_value / len(data['values']))}

        return pod_value_dict

    def get_namespace_pod_memory_used_top_n(self, namespace, start_time, end_time, step="30s", top_n=1):

        status, data_list = MemoryUtil.get_namespace_memory_used_range_time(namespace, start_time, end_time, step)
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
            tmp_instance = str(data['metric']['instance']).split(":")[0]

            for value in data['values']:
                tmp_value = float(str(value[1]))
                max_used_value = tmp_value if tmp_value > float(max_used_value) else float(max_used_value)
                total_used_value = float(total_used_value) + tmp_value
            pod_value_list.append({tmp_podname: {"host_ip": tmp_instance, "max_value": str(max_used_value),
                                                 "avg_value": str(total_used_value / len(data['values']))}})

            pod_value_list.sort(key=compare_max_values, reverse=True)

        pod_value_dict = dict()
        for i in range(0, int(top_n)):
            pod_value_dict.update(pod_value_list[i])

        return pod_value_dict


    def get_one_node_pod_memory_used_top_n(self, instance, start_time, end_time, step="30s", top_n=1):

        if not str(instance).__contains__(":10250"):
            instance = str(instance).strip(" ") + ":10250"

        status, data_list = MemoryUtil.get_node_pod_memory_max_used_range_time(instance, start_time, end_time, step)
        if str(status) != "success":
            logger.error("Cannot Get One Node Memory Metircs")
            raise Exception("Cannot Get One Node Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Node Memory Metircs Is Empty")
            raise Exception("Get Node Memory Metircs Is Empty")

        pod_value_list = []
        for data in data_list:
            max_used_value = total_used_value = 0
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                try:
                    tmp_podname = str(data['metric']['pod'])
                except:
                    logger.warn("------------------------------------------")
                    logger.warn("Cannot Found Lable 'pod/pod_name', Skip this metric")
                    logger.warn(str(data['metric']))
                    logger.warn("------------------------------------------")
                    continue

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

    def get_namespace_pod_memory_limit(self, namespace):

        status, data_list = MemoryUtil.get_namespace_pod_memory_limit(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.warn("Get Namespace Memory Metircs Is Empty")
            return pod_value_dict

        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict

    def get_namespace_pod_memory_request(self, namespace):

        status, data_list = MemoryUtil.get_namespace_pod_memory_request(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.error("Get Namespace Memory Metircs Is Empty")
            return pod_value_dict

        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict


    def get_namespace_specify_pod_memory_limit(self, namespace, pod_name_prefix):

        status, data_list = MemoryUtil.get_namespace_pod_memory_limit(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Namespace Memory Metircs")
            raise Exception("Cannot Get Namespace Memory Metircs")

        if len(data_list) == 0:
            logger.error("Get Namespace Memory Metircs Is Empty")
            raise Exception("Get Namespace Memory Metircs Is Empty")

        pod_value_dict = dict()
        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            if not tmp_podname.startswith(str(pod_name_prefix)):
                continue
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict


if __name__ == '__main__':

    memoryClient = MemoryClient()
    ip_value_list = memoryClient.get_all_node_now_memory_used()
    print ip_value_list

    ip_value_dict = memoryClient.get_one_node_now_memory_used("172.26.0.51")
    print ip_value_dict
    #
    end_time = time.time()
    start_time = end_time - 30 * 60
    ip_value_list = memoryClient.get_all_node_memory_used_range_time(start_time, end_time)
    print ip_value_list

    ip_value_dict = memoryClient.get_one_node_memory_used_range_time("172.26.0.51", start_time, end_time)
    print ip_value_dict

    pod_value_list = memoryClient.get_namespace_pod_memory_used("shared-env")
    print pod_value_list
    #

    pod_value_list = memoryClient.get_namespace_pod_memory_limit("shared-env")
    print pod_value_list

    pod_value_list = memoryClient.get_namespace_specify_pod_memory_used_range_time("shared-env", "hdfsdatanode", start_time, end_time)
    print pod_value_list

    pod_value_list = memoryClient.get_namespace_pod_memory_used_range_time("shared-env", start_time, end_time)
    print pod_value_list
    #
    pod_value_list = memoryClient.get_namespace_pod_memory_used_top_n("shared-env", start_time, end_time, top_n=5)
    print pod_value_list

    pod_value_list = memoryClient.get_one_node_pod_memory_used_top_n("172.26.0.51", start_time, end_time, top_n=3)
    print pod_value_list




