from urllib.parse import unquote

if __name__ == '__main__':
    test_str = """
    http://grafana-loki.wangjiahuan.com/explore?orgId=1&left=%5B%221631068980000%22,%221631069280000%22,%22loki-tristan%22,%7B%22expr%22:%22%7Bjob%3D%5C%22service_log%5C%22%7D%7C~%5C%22ERROR%7CException%5C%22!%3D%5C%22nacos%5C%22!%3D%5C%22slow%20sql%5C%22!%3D%5C%22404%5C%22!%3D%5C%22ErrorCodeException%5C%22!%3D%5C%22Target%20object%20must%20not%20be%20null%5C%22!%3D%5C%22Your%20request%20params%20is%20invalid%5C%22!%3D%5C%22%E6%A0%B8%E7%AE%97%E6%89%A9%E5%B1%95%E8%AE%A1%E7%AE%97%5C%22!%3D%5C%22%E6%A0%B8%E7%AE%97%E9%87%91%E9%A2%9D%5C%22!%3D%5C%22%E5%8F%82%E6%95%B0%E7%BC%BA%E5%A4%B1%5C%22!%3D%5C%22%E8%A7%A3%E6%9E%90%E6%97%A5%E5%BF%97%E5%8F%82%E6%95%B0%E5%BC%82%E5%B8%B8%5C%22%22%7D%5D
    """
    # 1631 0689 8000 0
    # 1631 0692 8000 0
    # 1631 0713 5530 8 096 000
    # 1631 1168 0000 0

    print(unquote(test_str))
    # /explore?orgId=1&left=["now-5m","now","Loki",{"expr":"{job=\"service_log\",service=\"{SERVICE_NAME}\"}|~\"ERROR|Exception\"!=\"nacos\"!=\"slow sql\"!=\"404\"!=\"ErrorCodeException\""}]

