from urllib.parse import unquote

if __name__ == '__main__':
    test_str = """http://grafana-loki.wangjiahuan.com/explore?orgId=1&left=%5B%22now-5m%22,%22now%22,%22Loki%22,%7B%22expr%22:%22%7Bjob%3D%5C%22service_log%5C%22,service%3D%5C%22auth-server%5C%22%7D%7C~%5C%22ERROR%7CException%5C%22!%3D%5C%22nacos%5C%22!%3D%5C%22slow%20sql%5C%22!%3D%5C%22404%5C%22!%3D%5C%22ErrorCodeException%5C%22%22%7D%5D"""
    print(unquote(test_str))
# /explore?orgId=1&left=["now-5m","now","Loki",{"expr":"{job=\"service_log\",service=\"{SERVICE_NAME}\"}|~\"ERROR|Exception\"!=\"nacos\"!=\"slow sql\"!=\"404\"!=\"ErrorCodeException\""}]
