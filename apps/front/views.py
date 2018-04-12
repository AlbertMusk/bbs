# encoding: utf-8
# author = 'Albert_Musk'


from flask import (
    Blueprint,
    views,
    render_template,
    make_response
)
from exts import alidayu
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint('front',__name__)

@bp.route('/')
def index():
    return 'front index'

@bp.route('/sms_captcha/')
def sms_captcha():
    result = alidayu.send_sms('17806284379',code='abcd')
    if result:
        return '发送成功'
    else:
        return '发送失败'

@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text,image = Captcha.gene_graph_captcha()
    # BytesIO 字节流
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    response = make_response(out.read())
    response.content_type = 'image/png'
    return response



class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front-signup.html')

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))