# executor-logging-loki-ruler
executor-logging-loki-ruler

# 分析

服务

​	异常日志查询

​		什么时候(固定时间/循环时间): crontab

​		查多久: 最近5分钟/今天

​		服务定位: `{replicaset="auth-server"}`

​		过滤规则: `|="ERROR"!="Nacos"`



用户组

​	用户

用户关注服务

​	<服务> <容忍度>



人的联系方式

告警配置

展示

​	查询时间范围: 总体异常服务数量

​	服务-次数-人-容忍度-持续时间

​	异常日志指纹化(指纹ID)



配置文件变动时自动创建/关闭任务以及调整对应的告警(暂时不做)
