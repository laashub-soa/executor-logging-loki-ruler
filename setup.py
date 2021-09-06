import logging
import os

from __init__ import init
from __init__ import project_temp_path
from config import app_conf
from service.loki_ruler import LokiRuler

init()
logger = logging.getLogger('setup')
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # 根据tasks创建调度任务
    # 调度频率为trigger中cron的值
    # 或者自定义解析
    for item in app_conf["tasks"]:
        logger.debug("task(%s) is start" % item)
        task_persistent_path = os.path.join(project_temp_path, item)
        if not os.path.exists(task_persistent_path):
            os.mkdir(task_persistent_path)
        task_data = app_conf["tasks"][item]
        task_data["common"] = {
            "dingding_webhook_access_token": app_conf["dingding_webhook_access_token"],
            "loki_base_uri": app_conf["loki_base_uri"],
            "user_info": app_conf["user_info"],
            "user_follow_service": app_conf["user_follow_service"],
        }
        LokiRuler(task_persistent_path, task_data).start()
