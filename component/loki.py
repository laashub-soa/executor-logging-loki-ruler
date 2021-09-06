from urllib.parse import urlencode

import requests


def query(base_url, log_ql, query_time_start, query_time_end):
    """
    查询loki
    :param base_url:
    :param log_ql:
    :param query_time_start:
    :param query_time_end:
    :return:
    """
    # 1630675964718000000
    # 1600251903664616300
    return requests.get(base_url + "/loki/api/v1/query_range",
                        params=urlencode({"query": log_ql, "start": query_time_start, "end": query_time_end})).json()
