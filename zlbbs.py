# coding:utf-8
from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
import config
from exts import db,mail,alidayu
from flask_wtf import CSRFProtect

# 初始化app
app = Flask(__name__)
# 导入配置文件
app.config.from_object(config)
# 初始化
db.init_app(app)
mail.init_app(app)
alidayu.init_app(app)
# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)
# 绑定CSRF保护
CSRFProtect(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
