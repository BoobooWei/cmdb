#coding:utf8

__author__ = 'eric'

from flask import Blueprint
main = Blueprint('main',__name__)
from . import views, errors
print __name__

from ..models import Permission


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


@main.app_context_processor
def inject_menu():
    navbars = []
    navbars.append({
        'name' : u'首页',
        'url'  : '/index',
        })

    navbars.append({
        'name' : u'关于',
        'url'  : '/about',
        })

    navbars.append({
        'name' : u'博客',
        'url'  : '/blog',
        })

    navbars.append({
        'name' : u'开发',
        'url'  : '/devops',
        })

    navbars.append({
        'name' : u'git',
        'url'  : 'http://git.dev-ops.top',
        })


    return dict(navbars=navbars)