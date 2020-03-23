# -*- coding: utf-8 -*-
import time

import Config
from Logger import Logger
from util.WarpdriveUtil import WarpdriveUtil

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="WarpdriveClient").getlog()


class WarpdriveClient(object):

    def __init__(self):
        pass

    def get_volume_total_requests(self, namespace):

        status, data_list = WarpdriveUtil.get_volume_total_requests(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Warpdrive Volume Metircs")
            raise Exception("Cannot Get Warpdrive Volume Metircs")

        pod_value_dict = dict()

        if len(data_list) == 0:
            logger.warn("Get Warpdrive Volume Is Empty")
            return pod_value_dict

        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict

    def get_volume_used(self, namespace):

        status, data_list = WarpdriveUtil.get_volume_used(namespace)
        if str(status) != "success":
            logger.error("Cannot Get Warpdrive Volume Metircs")
            raise Exception("Cannot Get Warpdrive Volume Metircs")

        pod_value_dict = dict()
        if len(data_list) == 0:
            logger.warn("Get Warpdrive Volume Is Empty")
            return pod_value_dict

        for data in data_list:
            if dict(data['metric']).has_key("pod_name"):
                tmp_podname = str(data['metric']['pod_name'])
            else:
                tmp_podname = str(data['metric']['pod'])
            tmp_value = str(data['value'][1])
            pod_value_dict[tmp_podname] = tmp_value

        return pod_value_dict



if __name__ == '__main__':
    warpdriveClient = WarpdriveClient()
    pod_value_dict = warpdriveClient.get_volume_total_requests("shared-env")
    print pod_value_dict