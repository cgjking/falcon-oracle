# falcon-oracle
适用于open-falcon的oracle监控脚本。
## 使用

* 新建一个主机用于链接oracle实例并监控。将open-falcon的[agent](https://book.open-falcon.org/zh_0_2/distributed_install/agent.html)部署到此主机上。

* 安装[oracleclient](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)和[cx_oracle](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#quick-start-cx-oracle-installation)
* 在你要监控的oracle实例上新建一个用于监控的只读用户。
```
create user test
identified by test
account unlock;
grant connect to test;
grant select any dictionary to test;
```
* 配置config.py
```
后台执行脚本：
nohup python3 -u falconOracle.py > out.log &
```
