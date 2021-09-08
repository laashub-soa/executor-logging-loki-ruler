import logging
from urllib.parse import urlencode

import requests

logger = logging.getLogger('loki')
logger.setLevel(logging.DEBUG)


def query(base_url, log_ql, query_time_start, query_time_end):
    """
    查询loki
    :param base_url:
    :param log_ql:
    :param query_time_start:
    :param query_time_end:
    :return:
    """
    logger.debug("base_url: %s\n, log_ql: %s\n, query_time_start: %s\n, query_time_end: %s\n" % (
        base_url, log_ql, query_time_start, query_time_end))
    query_result = requests.get(base_url + "/loki/api/v1/query_range",
                                params=urlencode(
                                    {"query": log_ql, "start": query_time_start, "end": query_time_end}))
    logger.debug("query_result: %s" % query_result.text)
    if query_result.status_code != 200:
        raise Exception("请求失败")
    return query_result.json()
