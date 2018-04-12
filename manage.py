# encoding: utf-8
# author = 'Albert_Musk'

from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from zlbbs import app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser = front_models.FrontUser

manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.command
def create_role():
    # 1.创建访问者
    visitor = CMSRole(name='访问者',desc='只能访问相关数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    # 2.运营人员(可以管理帖子、评论)
    operator = CMSRole(name='运营',desc='可以管理帖子，评论')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FORNTUSER

    # 3.管理员
    admin = CMSRole(name='管理员',desc='拥有一切权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.BOARDER|CMSPermission.FORNTUSER|CMSPermission.CMSUSER

    # 4.开发者
    developer = CMSRole(name='开发者',desc='至高无上的权限')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('有访问者权限')
    else:
        print('没有访问者权限')


@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功')
        else:
            print('没有这个角色')
    else:
        print('没有这个用户')


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')


@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--usernmae',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()