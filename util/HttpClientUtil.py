# -*- coding: utf-8 -*-
import json
import requests

import Config
from Logger import Logger

logger = Logger(logname=Config.LOGGER_LOC, loglevel=1, logger="HttpClientUtil").getlog()


class HttpClientUtil(object):
    @staticmethod
    def doPost(url, data, auth_token=""):

        if auth_token != "":
            headers = {'content-type': 'application/json',
                       'x-auth-token': auth_token}
        else:
            headers = {'content-type': 'application/json'}

        logger.debug("HEADERS: " + str(headers))
        logger.debug("POST:  " + url + " --data " + data)

        try:

            result = requests.post(url=url, data=data, headers=headers)
            logger.debug("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            logger.error(str(result.text))
            raise e

        return result

    @staticmethod
    def doGet(url, auth_token, **kwargs):

        if auth_token != "":
            headers = {'content-type': 'application/json',
                       'x-auth-token': auth_token}
        else:
            headers = {'content-type': 'application/json'}

        logger.debug("HEADERS: " + str(headers))
        logger.debug("GET:  " + url + " --data " + str(kwargs))

        try:

            result = requests.get(url=url, headers=headers, **kwargs)
            logger.debug("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            logger.error(str(result.text))
            raise e

        return result

    @staticmethod
    def doPut(url, auth_token, data, **kwargs):

        if auth_token != "":
            headers = {'content-type': 'application/json',
                       'x-auth-token': auth_token}
        else:
            headers = {'content-type': 'application/json'}

        logger.debug("HEADERS: " + str(headers))
        logger.debug("GET:  " + url + " --data " + str(kwargs))

        try:

            result = requests.put(url=url, headers=headers, data=data, **kwargs)
            logger.debug("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            logger.error(str(result.text))
            raise e

        return result

    @staticmethod
    def doDelete(url, auth_token, **kwargs):

        if auth_token != "":
            headers = {'content-type': 'application/json',
                       'x-auth-token': auth_token}
        else:
            headers = {'content-type': 'application/json'}

        logger.debug("HEADERS: " + str(headers))
        logger.debug("DELETE:  " + url + " --data " + str(kwargs))

        try:

            result = requests.delete(url=url, headers=headers, **kwargs)
            logger.debug("RESPONSE CODE: " + str(result.status_code))

            result.raise_for_status()

        except requests.RequestException as e:
            logger.error(e)
            logger.error(str(result.text))
            raise e

        return result


if __name__ == '__main__':
    url = "http://172.16.130.78:5000/v2.0/tokens"
    data = {
        "auth": {
            "tenantName": "admin",
            "passwordCredentials": {
                "username": "admin",
                "password": "admin"
            }
        }
    }

    result = HttpClientUtil.doPost(url, json.dumps(data))
    print json.loads(result.text)['access']['token']['id']
