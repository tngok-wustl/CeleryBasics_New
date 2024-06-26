# MCommandes

## 关于此程序

1. 数据来源：[此处](https://docs.google.com/spreadsheets/d/1SJTOn0FNIzy76FH8OeSz1Ul55lJkL-ZkmWAUaa5tFGo/edit?usp=sharing)（共300个工作表，其中第1张仅仅是格式而已）

2. 使用前，首先解压mcommandes_service.zip中的JSON文件（内含机密），因为GitHub代码仓库中禁止包含机密信息。

3. 运行前，启动redis伺服器：
    ```bash
    sudo service redis-server start
    ```
    然后celery消息中介：
    ```bash
    celery -A appli_celery worker --loglevel=INFO
    ```

4. 使用以下命令强制性删除所有未执行的任务：
    ```bash
    celery -A appli_celery purge
    ```

## 编程中发现的问题及对策

1. celery只能处理（JSON化）某些数据类型（例如dictionary）；所以所创建的订单对象必须基于dictionary。

2. Google API限制每分钟发出API请求60次，而celery只能针对每个worker限定任务执行间隔（无法设定运行所有任务的间隔）。所以，为防止429（过多请求）错误，我必须限定每个worker读取工作表的任务最多每秒执行1次，并设定一个worker如果抓到429错误就等1分钟后再重试（二者缺一不可）。一次试运行中，4个worker异步读取299张工作表耗时10分半（单个worker读取一张工作表耗时4-7秒）。
