from flask import Flask
from flask_cors import CORS
from config import Config
from models import db

# 创建Flask应用实例
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 启用跨域资源共享，允许前端访问API
CORS(app)
# 从Config对象加载配置
app.config.from_object(Config)
# 初始化数据库
db.init_app(app)

# 注册蓝图，用于组织路由
from analysis import bp as analysis_bp  # 数据分析相关路由
from data_management import bp as data_management_bp  # 数据管理相关路由

app.register_blueprint(analysis_bp)
app.register_blueprint(data_management_bp)

if __name__ == '__main__':
    # 以调试模式运行应用
    app.run(debug=True)