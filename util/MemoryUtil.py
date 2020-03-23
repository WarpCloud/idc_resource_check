# -*- coding: utf-8 -*-
import time

import Config
from Logger import Logger
from client.PrometheusClient import PrometheusClient

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="MemoryUtil").getlog()
prom_client = PrometheusClient(Config.PROMETHEUS_URL)


class MemoryUtil(object):


    @staticmethod
    def get_node_memory_total(instance=""):
        '''
            node_memory_MemTotal_bytes
            node_memory_MemTotal_bytes{instance="172.26.0.51:9100"}
        '''

        if (str(instance) != ""):
            query_str = 'node_memory_MemTotal_bytes{instance="' + instance + '"}  / (1024 * 1024 * 1024)'
        else:
            query_str = 'node_memory_MemTotal_bytes / (1024 * 1024 * 1024)'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_node_memory_used(instance=""):
        '''
            (node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Cached_bytes) / (1024 * 1024 * 1024)
            (node_memory_MemTotal_bytes{instance="172.26.0.51:9100"} - node_memory_MemFree_bytes{instance="172.26.0.51:9100"} - node_memory_Cached_bytes{instance="172.26.0.51:9100"}) / (1024 * 1024 * 1024)
        '''

        if (str(instance) != ""):
            query_str = '(node_memory_MemTotal_bytes{instance="' + instance + '"} - node_memory_MemFree_bytes{instance="' + instance + '"} - node_memory_Cached_bytes{instance="' + instance + '"}) / (1024 * 1024 * 1024)'
        else:
            query_str = '(node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Cached_bytes) / (1024 * 1024 * 1024)'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_node_memory_used_range_time(instance="", start=str(time.time()), end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            (node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Cached_bytes) / (1024 * 1024 * 1024)
            (node_memory_MemTotal_bytes{instance="172.26.0.51:9100"} - node_memory_MemFree_bytes{instance="172.26.0.51:9100"} - node_memory_Cached_bytes{instance="172.26.0.51:9100"}) / (1024 * 1024 * 1024)
        '''

        if (str(instance) != ""):
            query_str = '(node_memory_MemTotal_bytes{instance="' + instance + '"} - node_memory_MemFree_bytes{instance="' + instance + '"} - node_memory_Cached_bytes{instance="' + instance + '"}) / (1024 * 1024 * 1024)'
        else:
            query_str = '(node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Cached_bytes) / (1024 * 1024 * 1024)'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list

    @staticmethod
    def get_namespace_memory_used(namespace):
        '''
            sum(container_memory_usage_bytes{job="kubelet", cluster="", namespace="kube-system", container_name!="POD", container_name!="",service="prometheus-operator-kubelet"} by (instance, pod_name)/(1024*1024*1024)
        '''

        query_str = 'sum(container_memory_usage_bytes{job="kubelet", cluster="", namespace="' + namespace + '",container_name!="POD",container_name!="",service="prometheus-operator-kubelet"}) by (instance, pod_name)/(1024*1024*1024)'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_namespace_memory_used_range_time(namespace, start=str(time.time()), end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            sum(container_memory_usage_bytes{job="kubelet", cluster="", namespace="kube-system",container_name!="POD", container_name!=""})  by (instance, pod_name)/(1024*1024*1024)
        '''

        query_str = 'sum(container_memory_usage_bytes{job="kubelet", cluster="", namespace="' + namespace + '",container_name!="POD", container_name!=""}) by (instance, pod_name)/(1024*1024*1024)'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list


    @staticmethod
    def get_node_pod_memory_max_used_range_time(instance, start=str(time.time()), end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            sum(container_memory_usage_bytes{job="kubelet", cluster="", namespace="kube-system",container_name!="POD", container_name!="", service="prometheus-operator-kubelet"})  by (pod_name)/(1024*1024*1024)
        '''

        query_str = 'sum(container_memory_usage_bytes{job="kubelet", cluster="", instance="' + instance + '",container_name!="POD", container_name!="", service="prometheus-operator-kubelet"}) by (pod_name)/(1024*1024*1024)'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list

    @staticmethod
    def get_namespace_pod_memory_request(namespace):
        '''
            sum(kube_pod_container_resource_requests_memory_bytes{namespace="shared-env"}) by (pod,namespace)/(1024*1024*1024)
        '''

        query_str = 'sum(kube_pod_container_resource_requests_memory_bytes{namespace="' + namespace + '"}) by (pod,namespace)/(1024*1024*1024)'

        status, data_list = prom_client.query(str(query_str))

        return status, data_list

    @staticmethod
    def get_namespace_pod_memory_limit(namespace):
        '''
            sum(kube_pod_container_resource_limits_memory_bytes{namespace="shared-env"}) by (pod,namespace)/(1024*1024*1024)
        '''

        query_str = 'sum(kube_pod_container_resource_limits_memory_bytes{namespace="' + namespace + '"}) by (pod,namespace)/(1024*1024*1024)'

        status, data_list = prom_client.query(str(query_str))

        return status, data_list


if __name__ == '__main__':

    # status, data_list = MemoryUtil.get_node_memory_used("")
    # print status
    # print data_list
    #
    # end_time = time.time()
    # start_time = end_time - 60 * 60
    # status, data_list = MemoryUtil.get_node_memory_used_range_time("", str(start_time), str(end_time), "60s")
    # print status
    # print data_list
    #
    # print "======================================================"
    #
    # status, data_list = MemoryUtil.get_node_memory_used("172.16.3.130:9100")
    # print status
    # print data_list
    #
    # end_time = time.time()
    # start_time = end_time - 60 * 60
    # status, data_list = MemoryUtil.get_node_memory_used_range_time("172.16.3.130:9100", str(start_time), str(end_time), "60s")
    # print status
    # print data_list
    #
    # print "======================================================"
    #
    # status, data_list = MemoryUtil.get_namespace_memory_max_used("kube-system")
    # print status
    # print data_list
    #
    # end_time = time.time()
    # start_time = end_time - 60 * 60
    # status, data_list = MemoryUtil.get_namespace_memory_max_used_range_time("kube-system", str(start_time), str(end_time), "60s")
    # print status
    # print data_list
    #
    # print "======================================================"
    #
    # status, data_list = MemoryUtil.get_namespace_memory_avg_used("kube-system")
    # print status
    # print data_list
    #
    # end_time = time.time()
    # start_time = end_time - 60 * 60
    # status, data_list = MemoryUtil.get_namespace_memory_avg_used_range_time("kube-system", str(start_time), str(end_time), "60s")
    # print status
    # print data_list
    #
    # print "======================================================"
    #
    # status, data_list = MemoryUtil.get_namespace_pod_memory_request("monitor")
    # print status
    # print data_list
    #
    # status, data_list = MemoryUtil.get_namespace_pod_memory_limit("monitor")
    # print status
    # print data_list

    print "======================================================"

    end_time = time.time()
    start_time = end_time - 60 * 60

    status, data_list = MemoryUtil.get_node_pod_memory_max_used_range_time("172.16.3.130:10250", str(start_time), str(end_time), "60s")
    print status
    print data_list


    status, data_list = MemoryUtil.get_node_memory_total()
    print status
    print data_list