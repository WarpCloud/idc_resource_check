# -*- coding: utf-8 -*-
import json

import Config
from util.HttpClientUtil import HttpClientUtil
from Logger import Logger

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="PrometheusClient").getlog()


class PrometheusClient(object):

    def __init__(self, base_url):
        self.base_url = base_url + "/api/v1/"

    def query(self, query, time=""):

        ''' an instant query at a single point in time.

        :param query: Prometheus expression query string.
        :param time: time=<rfc3339 | unix_timestamp>: Evaluation timestamp. Optional.
        :return:
            result_status: query result status
            result_data_list: query result data list
        '''

        query_url = self.base_url + "query?query=" + query
        if time != "":
            query_url = str(query_url + "&time=" + time)

        result = HttpClientUtil.doGet(query_url, auth_token="")
        result_json = json.loads(result.text)

        result_data_list = []

        result_status = str(result_json['status'])
        if result_status == "success":
            for tmp in result_json['data']['result']:
                result_data_list.append(tmp)

        return result_status, result_data_list

    def query_range(self, query, start, end, step="15s"):
        """an instant query at a single point in time.

        Args:
            query: Prometheus expression query string.
            start=<rfc3339 | unix_timestamp>: Start timestamp
            end=<rfc3339 | unix_timestamp>: end timestamp
            step=<duration | float>: Query resolution step width in duration format or float number of seconds.

        Returns:
            result_status: query result status
            result_data_list: query result data list
        """

        query_url = self.base_url + "query_range?query=" + str(query) + "&start=" + str(start) + "&end=" + str(end) + "&step=" + str(step)

        result = HttpClientUtil.doGet(query_url, auth_token="")
        result_json = json.loads(result.text)

        result_data_list = []

        result_status = str(result_json['status'])
        if result_status == "success":
            for tmp in result_json['data']['result']:
                result_data_list.append(tmp)

        return result_status, result_data_list


if __name__ == '__main__':
    client = PrometheusClient("http://172.16.3.130:31601")
    status, data_list = client.query('rate(node_disk_io_time_seconds_total{device=~"sd.*"}[1m])')
    print status
    print data_list

    status, data_list = client.query_range("container_cpu_cfs_periods_total{pod_name='apacheds-master-xqqbt-0'}",
                                           start='1581670377.541', end='1581670577.541')
    print status
    print data_list
