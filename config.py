# gjbeyond@hotmai.com CaoGuangjie

#coding=utf-8 
# falcon配置
endpoint = "" # 上报给 open-falcon 的 endpoint
push_url = "http://127.0.0.1:1988/v1/push" # 上报的 http api 接口
interval = 120 # 上报的 step 间隔 建议不要小于60秒，时间太短可能造成单次获取数据未完成

# oracle 的配置项：
host = "" # oracle 的地址链接地址
userName = "" # oracle 的用户名
password = "" # oracle 的密码

