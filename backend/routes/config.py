class Config:
    """应用配置类
    
    包含Flask应用的所有配置项，如数据库连接、安全设置等
    """
    # 数据库连接URI，使用MySQL数据库，通过PyMySQL驱动连接
    # 格式：mysql+pymysql://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/zhaopin'
    
    # 是否追踪数据库修改，设为False可减少内存使用
    SQLALCHEMY_TRACK_MODIFICATIONS = False