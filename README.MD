#目的
>1、规范代码结构及风格
2、提供配置文件，优先级：脚本传参>环境变量>默认配置
3、格式化日志输出打印，使得日志可接入运维监控
4、提供一些公共工具/方法

#结构说明
>|--hdcloud #公共模块  
|----base #基础模块，主要为配置文件解析和日志  
|----dbutil #数据库操作工具  
|----utis #其他公共工具  
|----datasource.py #初始化数据库池连接配置  
|--service #业务代码模块 (可以参考demo模块使用)  
|--config.yaml #配置文件  
|--main.py #主执行程序

#使用注意
>1、若想使用脚本传参改变默认配置，需在主程序代码块前加入：Configs.register()
2、使用数据库连接池需在datasource.py 创建连接池关闭方法并在程序执行完成调用该方法

#建议
>1、公共方法或工具不建议使用类
2、方法或变量建议使用小写字母和下划线命名，常量使用大写和下划线命名

### 新增（2019-09-12）
>1、支持多环境配置文件配置，参考config.yaml中profile.active属性
2、支持动态配置日志输出级别及日志文件目录和前缀，参考config.yaml中logger.level\logger.prefix\logger.parent
    动态脚本传参如：`python main.py -logger.prefix=test` 
    或者 `Logger.reset_parent_prefix(prefix="test",parent="")` 会生成test-2019-09-12.log的日志文件。
    主要目的区分不同的进程执行文件的日志输出