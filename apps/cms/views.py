# encoding: utf-8
# author = 'Albert_Musk'

from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginForm,ResetpwdForm,ResetEmailForm
from .models import CMSUser,CMSPermission
from .decorators import login_required,permission_required
import config
from exts import db
from utils import restful,cache
from exts import mail
from flask_mail import Message
import random,string

bp = Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')

@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FORNTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')

@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error(message='请传递邮箱')
    else:
        # string.ascii_letters 可以拿到一个a-zA-Z的字符串
        # list()可以将字符串中的每一个字符作为列表的一项
        source = list(string.ascii_letters)
        # map(func= , 可迭代对象)
        # map方法可以将可迭代对象中的每一项执行func方法
        source.extend(map(lambda x:str(x),range(0,10)))
        # random.sample(列表，个数)方法可以在列表中随机拿多少个
        # ''.join() 可以将列表中的每一项组成一个字符串
        captcha = ''.join(random.sample(source,6))

        message = Message('Python论坛邮箱验证码',recipients=[email],body='您的邮箱验证码是：%s'%captcha)
        try:
            mail.send(message)
        except:
            return restful.params_error()
        cache.set(email,captcha,ex=120)
        print(cache.get(email))
        return restful.success()

@bp.route('/signout/')
@login_required
def signout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True

                return redirect(url_for('cms.index'))
            else:
                return self.get(message='密码验证错误')

        else:
            return form.get_error()

class ResetPwdView(views.MethodView):

    decorators = [login_required]
    def get(self,message=None):
        return render_template('cms/cms_resetpwd.html',message=message)

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data

            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='旧密码错误')
        else:
            return restful.params_error(form.get_error())

class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))