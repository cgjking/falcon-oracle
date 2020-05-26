# gjbeyond@hotmai.com CaoGuangjie
import requests
import cx_Oracle
import time
import copy
import json
import config

endpoint = config.endpoint
push_url = config.push_url
userName = config.userName
password = config.password
host = config.host
interval=config.interval
payload = []




def add_data(metric,value,conterType,tags,ts):
    
    # counterType :GAUGE 孤立点。COUNTER 连续点，连续点会计算两个数值之差，然后除以时间间隔
    data = {"endpoint":endpoint,"metric":metric,"timestamp":ts,"step":interval,"value":value,"counterType":conterType,"tags":tags}
    payload.append(copy.copy(data))

with cx_Oracle.connect(userName, password,host,) as connection:
    cursor = connection.cursor()
    while True:
        ts= int(time.time())
        # 获取session数量
        activeSession = 0
        inactiveSession = 0
        stopSession = 0
        cursor.execute("select status,count(status) from v$session where username != 'null'  GROUP by status")
        for raw in cursor:
            if raw[0]=="ACTIVE":
                activeSession = raw[1]
            elif raw[0] == "INACTIVE":
                inactiveSession = raw[1]
            else:
                stopSession=raw[1]
        add_data("session.activeSession",activeSession,"GAUGE","",ts)
        add_data("session.inactiveSession",inactiveSession,"GAUGE","",ts)
        add_data("session.stopSession",stopSession,"GAUGE","",ts)
    
       
        # 获取表空间 情况 单位为MB
        cursor.execute("""
            SELECT a.tablespace_name, 
            a.bytes/1024/1024 total, 
            b.bytes/1024/1024 used, 
            c.bytes/1024/1024 free, 
            (b.bytes * 100) / a.bytes "USED ", 
            (c.bytes * 100) / a.bytes "FREE " 
            FROM sys.sm$ts_avail a, sys.sm$ts_used b, sys.sm$ts_free c 
            WHERE a.tablespace_name = b.tablespace_name 
            AND a.tablespace_name = c.tablespace_name
        """)
    
        for raw in cursor:
            add_data("tableSpace."+raw[0]+".totalMB",raw[1],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".freeMB",raw[2],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".usedMB",raw[3],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".usePercent",raw[4],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".freePercent",raw[5],"GAUGE","",ts)
        
       
        # 获取ASN磁盘信息
        cursor.execute("select * from V$ASM_DISKGROUP")
        for raw in cursor:
            
            add_data("asmdf."+raw[1],100*(raw[7]-raw[8])/raw[7],"GAUGE","",ts)
    
    
    
    
    
        # 获取session数量
        activeSession = 0
        inactiveSession = 0
        stopSession = 0
        cursor.execute("select status,count(status) from v$session where username != 'null'  GROUP by status")
        for raw in cursor:
            if raw[0]=="ACTIVE":
                activeSession = raw[1]
            elif raw[0] == "INACTIVE":
                inactiveSession = raw[1]
            else:
                stopSession=raw[1]
        add_data("session.activeSession",activeSession,"GAUGE","",ts)
        add_data("session.inactiveSession",inactiveSession,"GAUGE","",ts)
        add_data("session.stopSession",stopSession,"GAUGE","",ts)
    
       
        # 获取表空间 情况 单位为MB
        cursor.execute("""
            SELECT a.tablespace_name, 
            a.bytes/1024/1024 total, 
            b.bytes/1024/1024 used, 
            c.bytes/1024/1024 free, 
            (b.bytes * 100) / a.bytes "USED ", 
            (c.bytes * 100) / a.bytes "FREE " 
            FROM sys.sm$ts_avail a, sys.sm$ts_used b, sys.sm$ts_free c 
            WHERE a.tablespace_name = b.tablespace_name 
            AND a.tablespace_name = c.tablespace_name
        """)
    
        for raw in cursor:
            add_data("tableSpace."+raw[0]+".totalMB",raw[1],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".freeMB",raw[2],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".usedMB",raw[3],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".usePercent",raw[4],"GAUGE","",ts)
            add_data("tableSpace."+raw[0]+".freePercent",raw[5],"GAUGE","",ts)
        
       
        # 获取ASN磁盘信息
        cursor.execute("select * from V$ASM_DISKGROUP")
        for raw in cursor:
            
            add_data("asmdf."+raw[1],100*(raw[7]-raw[8])/raw[7],"GAUGE","",ts)
    # 获取等待时间
        cursor.execute("select wait_class, sum(time_waited) from v$session_event group by wait_class")
        for raw in cursor:
            add_data("wait_class."+raw[0],raw[1]*10,"COUNTER","",ts)


        # 获取磁盘IO等数据
        cursor.execute("""
                        select name , value from v$sysstat where name = 'physical read total bytes' or name = 'physical write total IO requests'
                        or name='physical read total IO requests' or name = 'physical write total bytes'
        """)

        for raw in cursor:
            add_data("physicalIO."+raw[0],raw[1],"COUNTER","",ts)
  
    
        # 将数据上传
        print(payload)
        r = requests.post(push_url, data=json.dumps(payload))
        payload = []
        # 脚本执行所用时间
        timeend = int(time.time())-ts
        time.sleep(config.interval-timeend)

        
    
    
