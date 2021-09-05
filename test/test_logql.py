import datetime
from urllib.parse import urlencode

import requests

lok_base_url = "http://192.168.5.15:3100"

loki_service_query = {
    "job": {
        "logql": 'count_over_time({job="service_log"}|~"ERROR|Exception"!="nacos"!="slow sql"!="404"!="ErrorCodeException" [5m])',
        "is_must_at": True,  # other value is False
        "query_time_range": "rel: 5m-0m"
        # "query_time_range": "fix: h0-h24"
    }
    , "trigger": {
        "cron": "*/1 * * * *"
        # "cron": "0 10,14,18 * * *",
    }
    , "damage_time_point": {
        "total": 0,  # 总体
        "each": {}  # 详细 {"oss-api": 1630857600000}
    }
    , "alarm": {
        "template": "|{service_name}|{service_count}|{follow_of_users}",
        "is_at": True
    }
}


def query_loki(base_url, log_ql, query_time_start, query_time_end):
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


def convert_query_time_range(query_time_range):
    """
    转换查询时间范围
    :param query_time_range: 查询时间范围
    :return: 单位: 毫秒
    """
    # "rel: 5m-0m"
    # "fix: h0-h24"
    time_type_index = query_time_range.find(": ")
    time_type = query_time_range[:time_type_index]
    time_range = query_time_range[time_type_index + 2:]
    time_start_end_index = time_range.find("-")
    time_start = time_range[:time_start_end_index]
    time_end = time_range[time_start_end_index + 1:]

    # 统一转换成分钟单位
    def convert_rel_time_value_unit_2_minute(ori_time_value_unit):
        time_value = ori_time_value_unit[:-1]
        time_unit = ori_time_value_unit[-1:]
        if "m" == time_unit.lower():
            pass
        elif "h" == time_unit.lower():
            time_value = time_value * 60
        elif "d" == time_unit.lower():
            time_value = time_value * 60 * 24
        else:
            raise Exception("数据格式解析异常: %s" % time_unit)
        return int(time_value)

    def convert_fix_time_value_unit(ori_time_value_unit):
        time_unit = ori_time_value_unit[:1]
        time_value = int(ori_time_value_unit[1:])
        if "h" == time_unit:
            now_datetime = datetime.datetime.now()
            if time_value > 23:
                time_value = datetime.datetime(year=now_datetime.year, month=now_datetime.month, day=now_datetime.day,
                                               hour=0, minute=0, second=0)
                time_value = (time_value + datetime.timedelta(days=1)).timestamp()
            else:
                time_value = datetime.datetime(year=now_datetime.year, month=now_datetime.month, day=now_datetime.day,
                                               hour=time_value, minute=0, second=0).timestamp()
        else:
            raise Exception("数据格式解析异常: %s" % time_unit)
        return time_value

    if "rel" == time_type:
        start_query_time = (datetime.datetime.now() - datetime.timedelta(
            minutes=convert_rel_time_value_unit_2_minute(time_start))).timestamp()
        end_query_time = (datetime.datetime.now() - datetime.timedelta(
            minutes=convert_rel_time_value_unit_2_minute(time_end))).timestamp()
    elif "fix" == time_type:
        start_query_time = convert_fix_time_value_unit(time_start)
        end_query_time = convert_fix_time_value_unit(time_end)
    else:
        raise Exception("未知类型的查询时间, 请检查配置: job.query_time_range")

    return int(start_query_time * 1000), int(end_query_time * 1000)


def alarm_msg(ori_alarm_data):
    global loki_service_query
    ori_alarm_data_list = []
    for key in ori_alarm_data:
        value = ori_alarm_data[key]["total_count"]
        ori_alarm_data_list.append({"name": key, "count": value})
    ori_alarm_data_list.sort(key=lambda x: x["count"], reverse=True)
    print(ori_alarm_data_list)
    alarm_msg_text = ""
    # TODO 生成一键点击链接
    for item in ori_alarm_data_list:
        service_name = item["name"]
        service_count = item["count"]
        follow_of_users = ""
        alarm_msg_text += loki_service_query["alarm"]["template"].format(service_name=service_name,
                                                                         service_count=service_count,
                                                                         follow_of_users=follow_of_users) + "\n"
    print(alarm_msg_text)


def test():
    global loki_service_query
    # 查询数据
    loki_query_time_start, loki_query_time_end = convert_query_time_range(loki_service_query["job"]["query_time_range"])
    # print(loki_query_time_start, loki_query_time_end)
    resp_data = query_loki(lok_base_url, loki_service_query["job"]["logql"], loki_query_time_start * 1000000,
                           loki_query_time_end * 1000000)
    print(resp_data)
    # 解析数据并生成告警字符串
    # # 总体受损
    total_damage_time_range = ""  # 时间范围
    total_damage_service_count = 0  # 服务数量
    # total_damage_service_node_count = 0  # 服务节点数量
    total_damage_duration_time = 0  # 持续时间
    # # 服务受损
    service_damage = {}  # {"oss-api": {"wjh-prod": {"lmbrn": {"file_name_1":1}}}}
    query_result = resp_data["data"]["result"]
    if len(query_result) < 1:  # 当没有查询到异常日志项的时候
        if "damage_time_point" in loki_service_query:
            loki_service_query["damage_time_point"]["total"] = 0
            loki_service_query["damage_time_point"]["each"] = {}
        return
    # 遍历loki查询数据
    query_result = resp_data["data"]["result"]
    for item in query_result:
        # 解析值
        metric = item["metric"]
        service_name = metric["replicaset"]
        # service_env = metric["environment"]
        # service_node_name = metric["pod"] + "__" + metric["filename"]
        service_node_count = int(item["values"][len(item["values"]) - 1][1])
        # 加工数据
        # 切入到当前服务层级
        if service_name not in service_damage:
            service_damage[service_name] = {"total_count": 0}
            total_damage_service_count += 1
        service_damage[service_name]["total_count"] += service_node_count
        # cur_service_damage = service_damage[service_name]
        # # 切入到当前环境层级
        # if service_env not in cur_service_damage:
        #     cur_service_damage[service_env] = {}
        # cur_service_damage = cur_service_damage[service_env]
        # # 切入到当前节点层级
        # if service_node_name not in cur_service_damage:  # 切入到当前文件名称层级
        #     cur_service_damage[service_node_name] = {}
        # cur_service_damage[service_node_name] = service_node_count
    print(service_damage)
    alarm_msg(service_damage)


def test_alarm_msg():
    params = {'vendor-server': {'total_count': 4}, 'delivery-admin': {'total_count': 8}, 'oss-api': {'total_count': 1},
              'auth-server': {'total_count': 4}, 'wms-server': {'total_count': 1}}
    print(params)
    alarm_msg(params)


if __name__ == '__main__':
    # print(convert_query_time_range(service_query["job"]["query_time_range"]))
    # test()
    test_alarm_msg()
