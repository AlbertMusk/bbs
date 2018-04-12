# encoding: utf-8
# author = 'Albert_Musk'

from .views import bp
from flask import session,g
from .models import CMSUser,CMSPermission
import config

@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session[config.CMS_USER_ID]
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


@bp.context_processor
def cms_context_processor():
    return {'CMSPermission':CMSPermission}