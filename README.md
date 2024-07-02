# MCommandes

## 关于此程序

1. 数据来源：[此处](https://docs.google.com/spreadsheets/d/1SJTOn0FNIzy76FH8OeSz1Ul55lJkL-ZkmWAUaa5tFGo/edit?usp=sharing)（共300个工作表，其中第1张仅仅是格式而已）

2. 使用前，首先解压mcommandes_service.zip中的JSON文件（内含机密），因为GitHub代码仓库中禁止包含机密信息。

3. 启动redis伺服器：
    ```bash
    sudo service redis-server start
    ```
    然后启动celery消息收信端（worker）：
    ```bash
    celery -A celery_app worker --loglevel=INFO
    ```
    然后另外打开一个命令提示窗，运行带定时执行功能的celery发信端：
    ```bash
    celery -A celery_app beat --loglevel=INFO
    ```

4. 本程序一天中每15分运行一次，按日期生成订单记录，并统计每日毛利润

5. 若有紧急退出，使用以下命令强制性删除所有未执行的任务：
    ```bash
    celery -A appli_celery purge
    ```

## 做此程序学习到的经验

1. 使用gspread库读取电子表无需使用celery异步处理
    - 使用异步处理容易陷入大量429错误循环，从而浪费编程时间
    - 异步读取工作表几乎不会节省运行时间，反而会浪费系统资源

2. 查错（try-except）
    - 使用python封装库时，阅读其文档，观察可能发生的错误，并针对这些错误添加相应的try-except查错代码
    - 数据分析中最常见的错误：值缺失、格式（例如日期）不规范
    - 可写一个专门的函数查错：以一个函数f为参数，如果那个函数f成功运行则正常返回值，不然根据不同错误返回特殊值（例如None）
    
3. 电子表数据分析步骤
    1. 打开电子表（gspread）
    2. API获取所有工作表，并根据需要过滤部分工作表（例如空工作表）；注意考虑429错误————此时需要暂停API请求一段时间
    3. 从工作表中提取（全部或部分）列名
    4. 从工作表中逐行读取值（留意值缺失或不规范的情况，添加查错代码，并决定是否忽略及如何统计）
    5. 根据需要将工作表中保留下来的每行整理成一条对象（例如dictionary）；一个工作表就是一个对象列表

4. 尽量使用面向对象编程

5. 注意[代码规范](https://peps.python.org/pep-0008/)
