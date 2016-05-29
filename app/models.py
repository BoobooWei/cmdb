# -*- coding:utf-8 -*-

__author__ = 'eric'

import hashlib
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import current_app, request
from . import db
from . import login_manager




class Permission:
    USER_EDIT = 0x001

    DEVICE_LOOK = 0x002
    DEVICE_EDIT = 0x004

    RACK_LOOK = 0x008
    RACK_EDIT = 0x010

    IDC_LOOK = 0x020
    IDC_EDIT = 0x040

    ADMINISTER = 0x80



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, index=True, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.DEVICE_LOOK |
                     Permission.RACK_LOOK |
                     Permission.IDC_LOOK, True),

            'Administrator': (Permission.USER_EDIT |
                              Permission.DEVICE_LOOK |
                              Permission.DEVICE_EDIT |
                              Permission.RACK_LOOK |
                              Permission.RACK_EDIT |
                              Permission.IDC_LOOK  |
                              Permission.IDC_EDIT  |
                              Permission.ADMINISTER, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


    def __repr__(self):
        return '<Role %r>' %self.name




class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)             # Email Address
    username = db.Column(db.String(64),unique=True,index=True)          # Username
    password_hash = db.Column(db.String(128))                           # password Md5 Hash
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))           # Role 关联 Role table
    name = db.Column(db.String(64))                                     # 真实姓名
    location = db.Column(db.String(64))                                 # 地址
    about_me = db.Column(db.Text())                                     # 关于我
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)    # 注册时间
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)       # 最后登录时间
    confirmed = db.Column(db.Boolean, default=False)                    # 账户状态
    avatar_hash = db.Column(db.String(32))                              # 头像




    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)

        if self.role is None:
            if self.email == current_app.config.get('FLASK_ADMIN',None):
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('UTF-8')).hexdigest()


    @staticmethod
    def generate_fake(count=1000):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email = forgery_py.internet.email_address(),
                     username = forgery_py.internet.user_name(True),
                     password = forgery_py.lorem_ipsum.word(),
                     confirmed = True,
                     name = forgery_py.name.full_name(),
                     location = forgery_py.address.city(),
                     about_me = forgery_py.lorem_ipsum.sentence(),
                     member_since = forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                print "db commit email : {0} Error".format(u.email)
                db.session.rollback()



    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://secure.gravatar.com/avatar'

        hash = self.avatar_hash or hashlib.md5(self.email.encode('UTF-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,hash=hash,size=size,default=default,rating=rating)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)



    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
           data = s.loads(token)
        except:
            return False

        if data.get('confirm',None) != self.id:
            return False

        self.confirmed = True
        print self.confirmed
        db.session.add(self)
        return True


    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset':self.id})


    def reset_password(self,token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('reset',None) != self.id:
            return False

        self.password = new_password
        db.session.add(self)
        return True


    def generate_change_email_token(self,new_email,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'change_email':self.id, 'new_email': new_email})


    def change_email(self,token):
        s = Serializer(current_app.config ['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('change_email') != self.id:
            return False

        new_email = data.get('new_email',None)

        if new_email is None:
            return False

        if self.query.filter_by(email=new_email).first() is not None:
            return False

        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('UTF-8')).hexdigest()
        db.session.add(self)
        return True



    def __repr__(self):
        return '<User %r>' %self.username



class AssetType(db.Model):
    __tablename__ = 'assettype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True,index=True)             # 资产类名
    remarks = db.Column(db.Text)                                 # 资产类说明
    assets = db.relationship('Asset',backref='asset',lazy='dynamic')    # 关联 Asset table

    def __repr__(self):
        return '<AssetType %r>' %self.name






class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    assetclass_id = db.Column(db.ForeignKey('assettype.id'))   # 资产类别   关联AssetType table
    an = db.Column(db.String(64), unique=True,index=True)   # AN 企业资产编号
    sn = db.Column(db.String(64), unique=True,index=True)                           # SN 设备序列号
    onstatus = db.Column(db.Integer)                        # 使用状态
    flowstatus = db.Column(db.Integer)                      # 流程状态
    dateofmanufacture = db.Column(db.DateTime)              # 生产时间
    manufacturer = db.Column(db.String(64))                 # 生产商
    brand = db.Column(db.String(64))                        # 品牌
    model = db.Column(db.String(64))                        # 型号
    site = db.Column(db.String(64))                         # 位置
    devices = db.relationship('Device',backref='asset',lazy='dynamic')    # 关联设备表  Device Table
    usedept = db.Column(db.String(64))                      # 使用部门
    usestaff = db.Column(db.String(64))                     # 部门使用人
    usestarttime = db.Column(db.DateTime)                   # 使用开始时间
    useendtime = db.Column(db.DateTime)                     # 使用结束时间
    mainuses = db.Column(db.String(128))                    # 主要用途
    managedept = db.Column(db.String(64))                   # 管理部门
    managestaff = db.Column(db.String(64))                  # 管理人
    instaff = db.Column(db.String(64))                      # 录入人
    intime = db.Column(db.DateTime, default=datetime.now)   # 录入时间
    koriyasustarttime = db.Column(db.DateTime)              # 维保开始时间
    koriyasuendtime = db.Column(db.DateTime)                # 维保结束时间
    equipprice = db.Column(db.Integer)                      # 设备价格
    remarks = db.Column(db.Text)                            # 备注


    def __repr__(self):
        return '<Asset %r>' %self.id


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))                     # Hostname
    private_ip = db.Column(db.String(15))                   # 内外IP地址
    private_mac = db.Column(db.String(20))
    public_ip = db.Column(db.String(15))                    # 公网IP地址
    public_mac = db.Column(db.String(20))
    other_ip = db.Column(db.String(64))                     # 其他IP地址， 用“，”分隔多个
    #idcname = db.Column(db.ForeignKey('idcs.id'))   # 关联IDC table id
    rack_id = db.Column(db.ForeignKey('racks.id'))                         # 关联Rack table id
    idc = db.Column(db.String(64))                          # 关联IDC table id
    is_virtualization = db.Column(db.Boolean)               # 是否跑虚拟化  （如 OpenStack Compute）
    asset_id = db.Column(db.ForeignKey('assets.id'))           # 关联Asset 主表 id
    cpumodel = db.Column(db.String(64))                     # CPU 型号
    cpucount = db.Column(db.Integer)                        # CPU 核数
    memsize = db.Column(db.Integer)                      # 内存容量
    singlemem = db.Column(db.Integer)                       # 单根内存大小
    raidmodel = db.Column(db.String(64))                    # RAID 级别
    disksize = db.Column(db.Integer)                        # 磁盘容量
    remotecardip = db.Column(db.String(64))                 # 远控卡IP地址
    networkportcount = db.Column(db.Integer)                # 网卡端口数量
    os = db.Column(db.String(64))                           # os类型
    isdelete = db.Column(db.Boolean, default=False)                        # 是否删除
    remarks = db.Column(db.Text)                            # 备注
    instaff = db.Column(db.String(64))                      # 录入人
    inputtime = db.Column(db.DateTime, default=datetime.now)    # 录入时间
    remarks = db.Column(db.Text)                            # 备注

    def __repr__(self):
        return '<Device %r>' %self.hostname


class Idc(db.Model):
    __tablename__ = 'idcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ispid = db.Column(db.String(64))                        # 运营商名称
    racks = db.relationship('Rack',backref='idcname',lazy='dynamic')     # 关联Rack
    contactid = db.Column(db.String(64))                    # 联系人
    isdelete = db.Column(db.Boolean, default=False)                        # 是否删除
    nettype = db.Column(db.String(64))                      # 网络类型
    netout = db.Column(db.String(64))                       # 出口带宽
    address = db.Column(db.String(128))                     # 机房地址
    city = db.Column(db.String(64))                         # 城市
    adnature = db.Column(db.String(64))                     # 机房性质
    instaff = db.Column(db.String(64))                      # 录入人
    inputtime = db.Column(db.DateTime, default=datetime.now)    # 录入时间
    remarks = db.Column(db.Text)                            # 备注

    def __repr__(self):
        return '<Idc %r>' %self.idcname


class Rack(db.Model):
    __tablename__ = 'racks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    staff = db.Column(db.String(64))                        # 机柜负责人
    idcname_id = db.Column(db.ForeignKey('idcs.id'))   # 关联IDC table id
    devices = db.relationship('Device',backref='rack',lazy='dynamic')
    site = db.Column(db.String(64))                         # 机柜位置
    racktype = db.Column(db.String(64))                     # 机柜类型
    usesize = db.Column(db.Integer)                      # 已用空间（u）
    remainsize = db.Column(db.Integer)                   # 剩余空间（U）
    electrictype = db.Column(db.String(32))                 # 电力类型
    electricno = db.Column(db.String(32))                   # 电力路数
    electriccapacity = db.Column(db.Integer)             # 电力容量
    leftelectric = db.Column(db.Integer)                 # 剩余电力
    renttime = db.Column(db.DateTime)                       # 租用时间
    expiretime = db.Column(db.DateTime)                     # 过期时间
    nextpaytime = db.Column(db.DateTime)                    # 下次支付时间
    money = db.Column(db.Integer)                        # 支付金额
    isdelete = db.Column(db.Boolean, default=False)                        # 是否删除
    remarks = db.Column(db.Text)                            # 备注
    instaff = db.Column(db.String(64))                      # 录入人
    inputtime = db.Column(db.DateTime, default=datetime.now)    # 录入时间

    def __repr__(self):
        return '<Rack %r>' %self.idcname




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
