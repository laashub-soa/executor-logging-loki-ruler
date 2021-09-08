import json
import logging
import time
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
    logger.debug("params: base_url: %s\n, log_ql: %s\n, query_time_start: %s\n, query_time_end: %s\n" % (
        base_url, log_ql, query_time_start, query_time_end))
    execute_time_start = time.time()
    query_result = requests.get(base_url + "/loki/api/v1/query_range",
                                params=urlencode(
                                    {"query": log_ql, "start": query_time_start, "end": query_time_end}))
    query_result_text = query_result.text
    logger.debug(
        "query_time_cost: %s秒 \n,query_result: %s" % (int(time.time() - execute_time_start), query_result_text))
    if query_result.status_code != 200:
        raise Exception(query_result_text)
    return json.loads(query_result_text)
