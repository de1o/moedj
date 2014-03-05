准备工作:
----
0.  安装pip（if not），`wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py`后`sudo python get-pip.py`即可。

1.  `sudo apt-get install python-dev` && `sudo apt-get install libsqlite3-dev` for pysqlite

4.  安装supervisor：`pip install supervisor` 或者 `apt-get install supervisor`

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

    __注意，每次修改app key和密钥，都必须重启server（中断重新启动即可）,否则会导致微博授权失败。__
7.  点击左侧授权微博
8.  显示授权成功后在第三步中的终端里`ctrl C`中断管理服务器的运行

启动定时任务
----
1.  进入`/usr/local/etc`，执行`sudo wget https://raw.github.com/deloeating/moedj/master/supervisord.conf`和`sudo wget https://raw.github.com/deloeating/moedj/master/celeryd.conf`下载supervisor的配置文件。在mp虚拟环境的状态下执行`which celery`得到celery命令所在路径，修改`celeryd.conf`中的celery命令路径。
2.  执行`supervisord`启动supervisor，此时用于定时发送的celery应该也已经启动。使用supervisorctl status celery可以观察到celery的状态。如`celery    RUNNING    pid 24016, uptime 0:25:57`
3.  如celery未启动，执行`supervisorctl start celery`。
4.  注：celery定时任务采用的是UTC时区，应当与本机时区设置无关。


更多使用
----
1.  当完成了账号授权后，可以执行`mpupdate mins`来获取最近mins分钟内的更新条目。默认不加参数是20分钟。
2.  执行`mpsend`可以手动触发词条的推送。
3.  在`mpserver run`后可以在浏览器的管理界面进行屏蔽词条的增删查。
4.  使用`mplog`查看条目最近的更新和发送日志。
5.  使用`deactivate`可退出mp虚拟环境。

一些说明
----
如无特别说明，在安装virtualenv之后，对上面命令的操作都在`workon mp`之后执行。

此版本的moepad使用mediawiki的api而不是feed来获取最新条目。对关键词的屏蔽也同时考察词条的名称和词条的分类。例如Ahe颜的分类里有R18，那么将R18加入屏蔽列表将阻止Ahe颜被推送。

新创建词条会缓存24小时后发出，目前放行词条的功能还未实现。

如果bug欢迎反馈。:blush:

[1]:  http://redis.io/download
