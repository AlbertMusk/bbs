# encoding: utf-8
# author = 'Albert_Musk'

from flask import g
from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo,ValidationError
from ..forms import BaseForm
from utils import cache

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码'),InputRequired()])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码'),InputRequired()])
    newpwd2 = StringField(validators=[Length(6,20,message='请输入正确格式的新密码'),InputRequired()])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码'), InputRequired(),EqualTo('newpwd2')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(6,6,message='请输入正确长度的验证码')])


    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email).decode()

        if not cache_captcha or captcha.lower() != cache_captcha.lower():
            raise ValidationError('验证码不正确!')

    def validate_email(self,field):
        email = field.data
        old_email = g.cms_user.email

        if email == old_email:
            raise ValidationError('相同邮箱不能修改!')