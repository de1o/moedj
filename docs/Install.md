准备工作:
----
0.  安装pip（if not），`wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py`后`sudo python get-pip.py`即可。

1.  `sudo apt-get install python-dev` && `sudo apt-get install libsqlite3-dev` for pysqlite

2.  安装virtualenv和virtualenv-wrapper:
    ```
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    ```
执行
    ```
    export WORKON_HOME=~/venvs
    mkdir $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv --no-site-packages mp
    ```
创建了虚拟环境mp

    执行`workon mp`切换到虚拟环境mp下

    为了让virtualenv配置持续生效，将
    ```
    export WORKON_HOME=~/venvs
    source /usr/local/bin/virtualenvwrapper.sh
    ```
    两行加入`~/.bashrc`.
4.  安装supervisor：`pip install supervisor` 或者 `apt-get install supervisor`
3.  安装配置redis

redis配置：
----
1.  [下载][1]redis编译安装。
2.  修改redis.conf(可能在：`/usr/local/redis/redis.conf`或`/etc/redis/redis.conf`)，加入或开启以下配置项

    ```
    appendonly yes  # 开启aof持久化
    appendfilename appendonly.aof   # 数据保存在.aof文件里，文件存在redis.conf里dir指定的路径下
    appendfsync no  #  由操作系统完成文件的sync，默认30s一次，对我们来说够了
    ```
3.  执行redis-server /path/to/your/config/redis.conf 启动redis服务器
4.  注：moepad默认使用db number＝1的数据库，如果需要特别配置请修改`MoePad/mputils.py`里的参数

配置微博参数
----

1.  执行`pip install moedj`
3.  执行`mpsyncdb`创建数据库，按提示输入管理员密码，管理员名称默认是moepad
4.  执行`mpserver run`运行管理站，默认运行在8090端口。
5.  访问`http://gengxinweibo.moegirl.org:8090/`，用第二步中设置的密码登录
6.  设置微博app key和密钥，域名（`gengxinweibo.moegirl.org:8090/`)，相同条目发送间隔时间（单位小时）后提交
7.  点击左侧授权微博
8.  显示授权成功后在第四步中的终端里`ctrl C`中断管理服务器的运行
10. 执行`deactivate`退出mp虚拟环境

启动定时任务
----
1.  将`supervisord.conf`与`celeryd.conf`放入`/usr/local/etc/`路径下，并修改`celeryd.conf`中的celery命令路径。（在mp虚拟环境中执行`which celery`即可得到）。
2.  执行`supervisorctl start celery`即可。

查看日志
----
使用`mplog`查看条目的更新和发送日志。

备注
----
如无特别说明，在安装virtualenv之后，对上面命令的操作都在`workon mp`之后执行，以免出问题。

配置完毕后可使用`deactivate`退出mp虚拟环境。



[1]:  http://redis.io/download