# encoding: utf-8
# author = 'Albert_Musk'

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPermission(object):
    # 255 0b11111111
    # 权限设置
    # 拥有所有权限
    ALL_PERMISSION = 0b11111111
    # 访问者权限
    VISITOR =        0b00000001
    # 管理帖子权限
    POSTER =         0b00000010
    # 管理评论权限
    COMMENTER =      0b00000100
    # 管理板块权限
    BOARDER =        0b00001000
    # 管理前台用户的权限
    FORNTUSER =      0b00010000
    # 管理后台用户的权限
    CMSUSER =        0b00100000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    # 描述信息
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.VISITOR)

    users = db.relationship("CMSUser",backref="roles",secondary=cms_role_user)


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)


    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email


    # 密码加密
    # 初始化函数接收到password后会作为password中的raw_password参数
    # 然后经过加密后赋值给模型中的_password
    # 当需要访问_password时直接用CMSUser.password可以直接拿到

    # property装饰器可以使函数直接作为属性来访问
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

    # 拿到用户所有的权限
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permission = role.permissions
            all_permissions |= permission
        return all_permissions

    def has_permission(self,permission):
        return self.permissions & permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)