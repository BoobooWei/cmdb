#coding:utf8

__author__ = 'eric'

from flask import Blueprint
main = Blueprint('main',__name__)
from . import views, errors
from ..import db
from ..models import *
from ..models import Permission


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


@main.app_context_processor
def db_query():
    return dict(db=db)

@main.app_context_processor
def models():
    return dict(Asset=Asset, Device=Device, Rack=Rack, Idc=Idc,
                VirtMachine=VirtMachine, DevicePools=DevicePools,
                ClassType=ClassType, DeviceNetwork=DeviceNetwork,
                DevicePower=DevicePower, DevicePorts=DevicePorts,
                DeviceModel=DeviceModel, User=User)


@main.app_context_processor
def choice():
    choices = {
        'onstatus'     : {1: u'已用', 2: u'空闲', 3: u'下线', 4: u'待下线'},
        'powerstatus'  : {1: u'开机', 2: u'关机'},
        'nettype'      : {1: u'单电信', 2: u'单联通', 3: u'双BGP', 4: u'联通电信双线'},
        'adnature'     : {1: u'租用', 2: u'自建', 3: u'合作', 4: u'其他'},
        'powertype'    : {1: u'交流', 2: u'直流'}
    }
    return dict(choices=choices)


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
