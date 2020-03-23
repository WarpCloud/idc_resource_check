# -*- coding: utf-8 -*-


'''
    %util：一秒中有百分之多少的时间用于I/O操作，即被IO消耗的CPU百分比，一般地，如果该参数是100%表示设备已经接近满负荷运行了
    await：平均每次设备I/O操作的等待时间 (毫秒)，一般地，系统I/O响应时间应该低于2ms，如果大于 10ms就比较大了
    rkB/s：每秒读K字节数
    wkB/s:每秒写K字节数
'''

import time

import Config
from Logger import Logger
from client.PrometheusClient import PrometheusClient

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="IoUtil").getlog()
prom_client = PrometheusClient(Config.PROMETHEUS_URL)


class IoUtil(object):

    @staticmethod
    def get_node_io_util(device_prefix="sd", instance=""):
        '''
            rate(node_disk_io_time_seconds_total{device=~"sd.*"}[1m])
            rate(node_disk_io_time_seconds_total{device=~"sd.*", instance="172.16.3.130:9100"}[1m])
        '''

        if (str(instance) != ""):
            query_str = 'rate(node_disk_io_time_seconds_total{device=~"' + device_prefix + '.*", instance="' + str(
                instance) + '"}[1m])'
        else:
            query_str = 'rate(node_disk_io_time_seconds_total{device=~"' + device_prefix + '.*"}[1m])'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_node_io_util_range_time(device_prefix="sd", instance="", start=str(time.time()),
                                    end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            rate(node_disk_io_time_seconds_total{device=~"sd.*"}[1m])
            rate(node_disk_io_time_seconds_total{device=~"sd.*", instance="172.16.3.130:9100"}[1m])
        '''

        if (str(instance) != ""):
            query_str = 'rate(node_disk_io_time_seconds_total{device=~"' + device_prefix + '.*", instance="' + str(
                instance) + '"}[1m])'
        else:
            query_str = 'rate(node_disk_io_time_seconds_total{device=~"' + device_prefix + '.*"}[1m])'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list

    @staticmethod
    def get_node_io_await(device_prefix="sd", instance=""):
        '''
            rate(node_disk_read_time_seconds_total{device=~"sd.*"}[1m]) / rate(node_disk_reads_completed_total{device=~"sd.*"}[1m])
            rate(node_disk_read_time_seconds_total{device=~"dm.*",instance="172.16.1.51:9100"}[1m]) / rate(node_disk_reads_completed_total{device=~"dm.*",instance="172.16.1.51:9100"}[1m])
        '''

        if (str(instance) != ""):
            query_str = 'rate(node_disk_read_time_seconds_total{device=~"' + device_prefix + '.*", instance="' + instance + '"}[1m]) / rate(node_disk_reads_completed_total{device=~"' + device_prefix + '.*",instance="' + instance + '"}[1m])'
        else:
            query_str = 'rate(node_disk_read_time_seconds_total{device=~"' + device_prefix + '.*"}[1m]) / rate(node_disk_reads_completed_total{device=~"' + device_prefix + '.*"}[1m])'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_node_io_await_range_time(device_prefix="sd", instance="", start=str(time.time()),
                                     end=str(time.time() - 60 * 5), step=str("30s")):
        '''
            rate(node_disk_read_time_seconds_total{device=~"sd.*"}[1m]) / rate(node_disk_reads_completed_total{device=~"sd.*"}[1m])
            rate(node_disk_read_time_seconds_total{device=~"sd.*",instance="172.16.1.51:9100"}[1m]) / rate(node_disk_reads_completed_total{device=~"sd.*",instance="172.16.1.51:9100"}[1m])
        '''

        if (str(instance) != ""):
            query_str = 'rate(node_disk_read_time_seconds_total{device=~"' + device_prefix + '.*", instance="' + instance + '"}[1m]) / rate(node_disk_reads_completed_total{device=~"' + device_prefix + '.*",instance="' + instance + '"}[1m])'
        else:
            query_str = 'rate(node_disk_read_time_seconds_total{device=~"' + device_prefix + '.*"}[1m]) / rate(node_disk_reads_completed_total{device=~"' + device_prefix + '.*"}[1m])'

        status, data_list = prom_client.query_range(str(query_str), str(start), str(end), str(step))

        return status, data_list


if __name__ == '__main__':
    status, data_list = IoUtil.get_node_io_util("sd")
    print status
    print data_list

    status, data_list = IoUtil.get_node_io_util("sd", "172.16.3.130:9100")
    print status
    print data_list

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = IoUtil.get_node_io_util_range_time("sd", "", str(start_time), str(end_time), "60s")
    print status
    print data_list

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = IoUtil.get_node_io_util_range_time("sd", "172.16.3.130:9100", str(start_time), str(end_time),
                                                           "60s")
    print status
    print data_list

    print "=================================="

    status, data_list = IoUtil.get_node_io_await("sd")
    print status
    print data_list

    status, data_list = IoUtil.get_node_io_await("sd", "172.16.3.130:9100")
    print status
    print data_list

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = IoUtil.get_node_io_await_range_time("sd", "", str(start_time), str(end_time), "60s")
    print status
    print data_list

    end_time = time.time()
    start_time = end_time - 60 * 60
    status, data_list = IoUtil.get_node_io_await_range_time("sd", "172.16.3.130:9100", str(start_time), str(end_time),
                                                            "60s")
    print status
    print data_list
