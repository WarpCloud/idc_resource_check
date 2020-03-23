# -*- coding: utf-8 -*-
import time

import Config
from Logger import Logger
from client.PrometheusClient import PrometheusClient

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="CpuUtil").getlog()
prom_client = PrometheusClient(Config.PROMETHEUS_URL)


class CpuUtil(object):

    @staticmethod
    def get_node_cpu_used(instance=""):
        '''
            sum by(instance) (rate(node_cpu_seconds_total{mode!="idle"}[2m])) * 100
            sum by(instance) (rate(node_cpu_seconds_total{mode!="idle",instance="172.16.1.51:9100"}[2m])) * 100
        '''

        if (str(instance) != ""):
            query_str = 'sum by(instance) (rate(node_cpu_seconds_total{mode!="idle",instance="' + instance + '"}[2m])) * 100'
        else:
            query_str = 'sum by(instance) (rate(node_cpu_seconds_total{mode!="idle"}[2m])) * 100'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_node_cpu_used_range_time(instance="", start=str(time.time()), end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            sum by(instance) (rate(node_cpu_seconds_total{mode!="idle"}[2m])) * 100
            sum by(instance) (rate(node_cpu_seconds_total{mode!="idle",instance="172.16.1.51:9100"}[2m])) * 100
        '''

        if (str(instance) != ""):
            query_str = 'sum by(instance) (rate(node_cpu_seconds_total{mode!="idle",instance="' + instance + '"}[2m])) * 100'
        else:

            query_str = 'sum by(instance) (rate(node_cpu_seconds_total{mode!="idle"}[2m])) * 100'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list

    @staticmethod
    def get_namespace_cpu_used(namespace):
        '''
            sum(namespace_pod_name_container_name:container_cpu_usage_seconds_total:sum_rate{container_name !="POD", namespace="integ1-multies"}) by (container_name,  pod_name, namespace)
        '''

        query_str = 'sum(namespace_pod_name_container_name:container_cpu_usage_seconds_total:sum_rate{container_name !="POD", namespace="' + namespace + '"}) by (container_name,  pod_name, namespace)'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_namespace_cpu_used_range_time(namespace, start=str(time.time()), end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            sum by(namespace, pod_name) (rate(container_cpu_usage_seconds_total{container_name!="", container_name!="POD",image!="",job="kubelet",namespace="1ofnuao"}[5m]))
        '''

        query_str = 'sum by(namespace, pod_name) (rate(container_cpu_usage_seconds_total{container_name!="", container_name!="POD",image!="",job="kubelet",namespace="' + namespace + '"}[5m]))'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list

    @staticmethod
    def get_namespace_pod_cpu_request(namespace):
        '''
            sum(kube_pod_container_resource_requests_cpu_cores{namespace="shared-env"}) by (pod, namespace)
        '''

        query_str = 'sum(kube_pod_container_resource_requests_cpu_cores{namespace="' + namespace + '"}) by (pod,namespace)'

        status, data_list = prom_client.query(str(query_str))

        return status, data_list

    @staticmethod
    def get_namespace_pod_cpu_limit(namespace):
        '''
            sum(kube_pod_container_resource_limits_cpu_cores{namespace="shared-env"}) by (pod, namespace)
        '''

        query_str = 'sum(kube_pod_container_resource_limits_cpu_cores{namespace="' + namespace + '"}) by (pod,namespace)'

        status, data_list = prom_client.query(str(query_str))

        return status, data_list


if __name__ == '__main__':
    status, data_list = CpuUtil.get_node_cpu_used()
    print status
    print data_list

    status, data_list = CpuUtil.get_node_cpu_used("172.16.3.130:9100")
    print status
    print data_list

    print "********************************************"

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = CpuUtil.get_node_cpu_used_range_time("", str(start_time), str(end_time), "60s")
    print status
    print data_list

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = CpuUtil.get_node_cpu_used_range_time("172.16.3.130:9100", str(start_time), str(end_time), "60s")
    print status
    print data_list

    print "======================================================"

    status, data_list = CpuUtil.get_namespace_cpu_used("monitor")
    print status
    print data_list

    print "********************************************"

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = CpuUtil.get_namespace_cpu_used_range_time("monitor", str(start_time), str(end_time), "60s")
    print status
    print data_list

    print "======================================================"

    status, data_list = CpuUtil.get_namespace_pod_cpu_request("monitor")
    print status
    print data_list

    status, data_list = CpuUtil.get_namespace_pod_cpu_limit("monitor")
    print status
    print data_list