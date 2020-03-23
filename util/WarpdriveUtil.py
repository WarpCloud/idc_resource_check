# -*- coding: utf-8 -*-
import time

import Config
from Logger import Logger
from client.PrometheusClient import PrometheusClient

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="WarpdriveUtil").getlog()
prom_client = PrometheusClient(Config.PROMETHEUS_URL)


class WarpdriveUtil(object):

    @staticmethod
    def get_volume_total_requests(namespace):
        '''
            warpdrive_volume_total_space_bytes{exported_namespace="shared-env"}/(1024 * 1024 * 1024)
        '''

        query_str = 'sum(warpdrive_volume_total_space_bytes{exported_namespace="' + namespace + '"}) by (exported_namespace, pod)/(1024 * 1024 * 1024)'

        status, data_list = prom_client.query(query_str)

        return status, data_list

    @staticmethod
    def get_volume_used(namespace):
        '''
            warpdrive_volume_used_space_bytes{exported_namespace="shared-env"}/(1024 * 1024 * 1024)
        '''

        query_str = 'sum(warpdrive_volume_used_space_bytes{exported_namespace="' + namespace + '"}) by(exported_namespace, pod)/(1024 * 1024 * 1024)'

        status, data_list = prom_client.query(query_str)

        return status, data_list


if __name__ == '__main__':

    status, data_list = WarpdriveUtil.get_volume_total_requests("shared-env")
    print status
    print data_list

    status, data_list = WarpdriveUtil.get_volume_used("shared-env")
    print status
    print data_list


    print "======================================================"
