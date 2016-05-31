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
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))           # Role 鍏宠仈 Role table
    name = db.Column(db.String(64))                                     # 鐪熷疄濮撳悕
    location = db.Column(db.String(64))                                 # 鍦板潃
    position = db.Column(db.String(64))                                 # 职位
    about_me = db.Column(db.Text())                                     # 鍏充簬鎴�
    phone = db.Column(db.String(11))                                       # 手机号码
    qq = db.Column(db.String(13))                                          # QQ号码
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)    # 娉ㄥ唽鏃堕棿
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)       # 鏈�鍚庣櫥褰曟椂闂�
    confirmed = db.Column(db.Boolean, default=False)                    # 璐︽埛鐘舵��
    avatar_hash = db.Column(db.String(32))                              # 澶村儚


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
                     position = forgery_py.lorem_ipsum.sentence(),
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
    name = db.Column(db.String(64), unique=True,index=True)             # 璧勪骇绫诲悕
    remarks = db.Column(db.Text)                                 # 璧勪骇绫昏鏄�
    assets = db.relationship('Asset',backref='asset',lazy='dynamic')    # 鍏宠仈 Asset table

    def __repr__(self):
        return '<AssetType %r>' %self.name






class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    assetclass_id = db.Column(db.ForeignKey('assettype.id'))   # 璧勪骇绫诲埆   鍏宠仈AssetType table
    an = db.Column(db.String(64), unique=True,index=True)   # AN 浼佷笟璧勪骇缂栧彿
    sn = db.Column(db.String(64), unique=True,index=True)                           # SN 璁惧搴忓垪鍙�
    onstatus = db.Column(db.Integer)                        # 浣跨敤鐘舵��
    flowstatus = db.Column(db.Integer)                      # 娴佺▼鐘舵��
    dateofmanufacture = db.Column(db.DateTime)              # 鐢熶骇鏃堕棿
    manufacturer = db.Column(db.String(64))                 # 鐢熶骇鍟�
    brand = db.Column(db.String(64))                        # 鍝佺墝
    model = db.Column(db.String(64))                        # 鍨嬪彿
    site = db.Column(db.String(64))                         # 浣嶇疆
    devices = db.relationship('Device',backref='asset',lazy='dynamic')    # 鍏宠仈璁惧琛�  Device Table
    usedept = db.Column(db.String(64))                      # 浣跨敤閮ㄩ棬
    usestaff = db.Column(db.String(64))                     # 閮ㄩ棬浣跨敤浜�
    usestarttime = db.Column(db.DateTime)                   # 浣跨敤寮�濮嬫椂闂�
    useendtime = db.Column(db.DateTime)                     # 浣跨敤缁撴潫鏃堕棿
    mainuses = db.Column(db.String(128))                    # 涓昏鐢ㄩ��
    managedept = db.Column(db.String(64))                   # 绠＄悊閮ㄩ棬
    managestaff = db.Column(db.String(64))                  # 绠＄悊浜�
    instaff = db.Column(db.String(64))                      # 褰曞叆浜�
    intime = db.Column(db.DateTime, default=datetime.now)   # 褰曞叆鏃堕棿
    koriyasustarttime = db.Column(db.DateTime)              # 缁翠繚寮�濮嬫椂闂�
    koriyasuendtime = db.Column(db.DateTime)                # 缁翠繚缁撴潫鏃堕棿
    equipprice = db.Column(db.Integer)                      # 璁惧浠锋牸
    remarks = db.Column(db.Text)                            # 澶囨敞


    def __repr__(self):
        return '<Asset %r>' %self.id


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))                     # Hostname
    private_ip = db.Column(db.String(15))                   # 鍐呭IP鍦板潃
    private_mac = db.Column(db.String(20))
    public_ip = db.Column(db.String(15))                    # 鍏綉IP鍦板潃
    public_mac = db.Column(db.String(20))
    other_ip = db.Column(db.String(64))                     # 鍏朵粬IP鍦板潃锛� 鐢ㄢ�滐紝鈥濆垎闅斿涓�
    #idcname = db.Column(db.ForeignKey('idcs.id'))   # 鍏宠仈IDC table id
    rack_id = db.Column(db.ForeignKey('racks.id'))                         # 鍏宠仈Rack table id
    idc = db.Column(db.String(64))                          # 鍏宠仈IDC table id
    is_virtualization = db.Column(db.Boolean)               # 鏄惁璺戣櫄鎷熷寲  锛堝 OpenStack Compute锛�
    asset_id = db.Column(db.ForeignKey('assets.id'))           # 鍏宠仈Asset 涓昏〃 id
    cpumodel = db.Column(db.String(64))                     # CPU 鍨嬪彿
    cpucount = db.Column(db.Integer)                        # CPU 鏍告暟
    memsize = db.Column(db.Integer)                      # 鍐呭瓨瀹归噺
    singlemem = db.Column(db.Integer)                       # 鍗曟牴鍐呭瓨澶у皬
    raidmodel = db.Column(db.String(64))                    # RAID 绾у埆
    disksize = db.Column(db.Integer)                        # 纾佺洏瀹归噺
    remotecardip = db.Column(db.String(64))                 # 杩滄帶鍗P鍦板潃
    networkportcount = db.Column(db.Integer)                # 缃戝崱绔彛鏁伴噺
    os = db.Column(db.String(64))                           # os绫诲瀷
    isdelete = db.Column(db.Boolean, default=False)                        # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)                            # 澶囨敞
    instaff = db.Column(db.String(64))                      # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)    # 褰曞叆鏃堕棿
    remarks = db.Column(db.Text)                            # 澶囨敞

    def __repr__(self):
        return '<Device %r>' %self.hostname


class Idc(db.Model):
    __tablename__ = 'idcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ispid = db.Column(db.String(64))                        # 杩愯惀鍟嗗悕绉�
    racks = db.relationship('Rack',backref='idcname',lazy='dynamic')     # 鍏宠仈Rack
    contactid = db.Column(db.String(64))                    # 鑱旂郴浜�
    isdelete = db.Column(db.Boolean, default=False)                        # 鏄惁鍒犻櫎
    nettype = db.Column(db.String(64))                      # 缃戠粶绫诲瀷
    netout = db.Column(db.String(64))                       # 鍑哄彛甯﹀
    address = db.Column(db.String(128))                     # 鏈烘埧鍦板潃
    city = db.Column(db.String(64))                         # 鍩庡競
    adnature = db.Column(db.String(64))                     # 鏈烘埧鎬ц川
    instaff = db.Column(db.String(64))                      # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)    # 褰曞叆鏃堕棿
    remarks = db.Column(db.Text)                            # 澶囨敞

    def __repr__(self):
        return '<Idc %r>' %self.idcname


class Rack(db.Model):
    __tablename__ = 'racks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    staff = db.Column(db.String(64))                        # 鏈烘煖璐熻矗浜�
    idcname_id = db.Column(db.ForeignKey('idcs.id'))   # 鍏宠仈IDC table id
    devices = db.relationship('Device',backref='rack',lazy='dynamic')
    site = db.Column(db.String(64))                         # 鏈烘煖浣嶇疆
    racktype = db.Column(db.String(64))                     # 鏈烘煖绫诲瀷
    usesize = db.Column(db.Integer)                      # 宸茬敤绌洪棿锛坲锛�
    remainsize = db.Column(db.Integer)                   # 鍓╀綑绌洪棿锛圲锛�
    electrictype = db.Column(db.String(32))                 # 鐢靛姏绫诲瀷
    electricno = db.Column(db.String(32))                   # 鐢靛姏璺暟
    electriccapacity = db.Column(db.Integer)             # 鐢靛姏瀹归噺
    leftelectric = db.Column(db.Integer)                 # 鍓╀綑鐢靛姏
    renttime = db.Column(db.DateTime)                       # 绉熺敤鏃堕棿
    expiretime = db.Column(db.DateTime)                     # 杩囨湡鏃堕棿
    nextpaytime = db.Column(db.DateTime)                    # 涓嬫鏀粯鏃堕棿
    money = db.Column(db.Integer)                        # 鏀粯閲戦
    isdelete = db.Column(db.Boolean, default=False)                        # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)                            # 澶囨敞
    instaff = db.Column(db.String(64))                      # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)    # 褰曞叆鏃堕棿

    def __repr__(self):
        return '<Rack %r>' %self.idcname




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
