flask-script的用法：

~~~
Flask-Script扩展提供向Flask插入外部脚本的功能。包括运行一个开发用的服务器，一个定制的 Python shell，设置数据库的脚本，cronjobs，以及其他的运行在web应用之外的命令行任务。

Flask-Script和Flask本身的工作方式类似。只需要定义和添加能从命令行中被Manager实例调用的 命令即可。

Flask-Script 的作用是可以通过命令行的方式来操作 Flask。例如通过命令跑一个开发版本的服务器、设置数据库、定时任务等。
~~~

flask项目中app在那个目录下定义，启动项目的时候，就会把那个目录作为base函数的目录
~~~
manage.py函数作为app和manage相连接的一个定义

项目中src下的init文件中作为创建app和db的初始化模块，main函数也是在这个模块定义的

config文件作为定义一些基础的配置类，如：mysql的url、redis配置等
