# -*- coding:utf-8 -*-

__author__ = 'eric'

import hashlib
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import current_app, request, url_for, flash
from . import db
from . import login_manager
from app.exceptions import ValidationError


class Permission(object):
    ADMINISTER = 0x001

    DEVICE_LOOK = 0x002
    DEVICE_EDIT = 0x004
    DEVICE_DEL = 0x008

    RACK_LOOK = 0x010
    RACK_EDIT = 0x020
    RACK_DEL = 0x040

    IDC_LOOK = 0x080
    IDC_EDIT = 0x100
    IDC_DEL = 0x200

    VIRTMACHINE_LOOK = 0x400
    VIRTMACHINE_EDIT = 0x800
    VIRTMACHINE_DEL = 0x1000

    NETWORKDEVICE_LOOK = 0x2000
    NETWORKDEVICE_EDIT = 0x4000
    NETWORKDEVICE_DEL = 0x8000

    DATABASE_LOOK = 0x10000
    DATABASE_EDIT = 0x20000
    DATABASE_DEL = 0x40000

    SOFTWARE_LOOK = 0x80000
    SOFTWARE_EDIT = 0x100000
    SOFTWARE_DEL = 0x200000

    DEVICEPERMISSION_LOOK = 0x400000
    DEVICEPERMISSION_EDIT = 0x800000
    DEVICEPERMISSION_DEL = 0x1000000

    ASSET_LOOK = 0x2000000
    ASSET_EDIT = 0x4000000
    ASSET_DEL = 0x8000000

    USER_LOOK = 0x10000000
    USER_EDIT = 0x20000000
    USER_DEL = 0x40000000

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, index=True, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def to_json(self):
        json_role = {
            'url' : self.id,
            'name' : self.name,
            'default' : self.default,
            'permissions' : self.permissions,
            'users' : self.users,
        }

        return json_role

    @staticmethod
    def insert_roles():
        roles = {

            'User': (
                     Permission.DEVICEPERMISSION_LOOK |
                     Permission.SOFTWARE_LOOK |
                     Permission.VIRTMACHINE_LOOK |
                     Permission.NETWORKDEVICE_LOOK |
                     Permission.DATABASE_LOOK |
                     Permission.SOFTWARE_LOOK |
                     Permission.ASSET_LOOK |
                     Permission.DEVICE_LOOK |
                     Permission.RACK_LOOK |
                     Permission.IDC_LOOK|
                     Permission.USER_LOOK, True),

            'manager': (

                Permission.DEVICEPERMISSION_LOOK |
                Permission.SOFTWARE_LOOK |
                Permission.VIRTMACHINE_LOOK |
                Permission.NETWORKDEVICE_LOOK |
                Permission.DATABASE_LOOK |
                Permission.SOFTWARE_LOOK |
                Permission.ASSET_LOOK |
                Permission.DEVICE_LOOK |
                Permission.RACK_LOOK |
                Permission.IDC_LOOK  |
                Permission.USER_LOOK |

                Permission.DEVICEPERMISSION_EDIT |
                Permission.SOFTWARE_EDIT |
                Permission.VIRTMACHINE_EDIT |
                Permission.NETWORKDEVICE_EDIT |
                Permission.DATABASE_EDIT |
                Permission.SOFTWARE_EDIT |
                Permission.ASSET_EDIT |
                Permission.DEVICE_EDIT |
                Permission.RACK_EDIT |
                Permission.IDC_EDIT |

                Permission.DEVICEPERMISSION_DEL |
                Permission.SOFTWARE_DEL |
                Permission.VIRTMACHINE_DEL |
                Permission.NETWORKDEVICE_DEL |
                Permission.DATABASE_DEL |
                Permission.SOFTWARE_DEL |
                Permission.ASSET_DEL |
                Permission.DEVICE_DEL |
                Permission.RACK_DEL |
                Permission.IDC_DEL |

                Permission.ASSET_EDIT, False ),

            'Administrator': (

                Permission.DEVICEPERMISSION_LOOK |
                Permission.SOFTWARE_LOOK |
                Permission.VIRTMACHINE_LOOK |
                Permission.NETWORKDEVICE_LOOK |
                Permission.DATABASE_LOOK |
                Permission.SOFTWARE_LOOK |
                Permission.ASSET_LOOK |
                Permission.DEVICE_LOOK |
                Permission.IDC_LOOK |
                Permission.RACK_LOOK |
                Permission.USER_LOOK |

                Permission.DEVICEPERMISSION_EDIT |
                Permission.SOFTWARE_EDIT |
                Permission.VIRTMACHINE_EDIT |
                Permission.NETWORKDEVICE_EDIT |
                Permission.DATABASE_EDIT |
                Permission.SOFTWARE_EDIT |
                Permission.ASSET_EDIT |
                Permission.DEVICE_EDIT |
                Permission.IDC_EDIT  |
                Permission.RACK_EDIT |
                Permission.USER_EDIT |

                Permission.DEVICEPERMISSION_DEL |
                Permission.SOFTWARE_DEL |
                Permission.VIRTMACHINE_DEL |
                Permission.NETWORKDEVICE_DEL |
                Permission.DATABASE_DEL |
                Permission.SOFTWARE_DEL |
                Permission.ASSET_DEL |
                Permission.DEVICE_DEL |
                Permission.IDC_DEL  |
                Permission.RACK_DEL |
                Permission.USER_EDIT |
                Permission.USER_DEL |
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
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)  # Email Address
    username = db.Column(db.String(64), unique=True, index=True)  # Username
    password_hash = db.Column(db.String(128))  # password Md5 Hash
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Role 鍏宠仈 Role table
    name = db.Column(db.String(64))  # 鐪熷疄濮撳悕
    location = db.Column(db.String(64))  # 鍦板潃
    position = db.Column(db.String(64))  # 职位
    about_me = db.Column(db.Text())  # 鍏充簬鎴�
    phone = db.Column(db.String(11))  # 手机号码
    qq = db.Column(db.String(13))  # QQ号码
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)  # 娉ㄥ唽鏃堕棿
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)  # 鏈�鍚庣櫥褰曟椂闂�
    confirmed = db.Column(db.Boolean, default=False)  # 璐︽埛鐘舵��
    avatar_hash = db.Column(db.String(32))  # 澶村儚
    logs = db.relationship('Logger', backref='user', lazy='dynamic')


    def to_json(self):
        json_user = {
            'url' : self.id,
            'email' : self.email,
            'username' : self.username,
            'password_hash' : self.password_hash,
            'role' : self.role,
            'name' : self.name,
            'location' : self.location,
            'position' : self.position,
            'about_me' : self.about_me,
            'phone' : self.phone,
            'qq' : self.qq,
            'member_sine' : self.member_since,
            'last_seen' : self.last_seen,
        }

        return json_user

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if self.role is None:
            if self.email == current_app.config.get('FLASK_ADMIN', None):
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('UTF-8')).hexdigest()


    @staticmethod
    def insert_admin_user():

        r = Role()
        r.insert_roles()
        adminRole = Role.query.all()[-1]

        u = User.query.filter_by(username='administrator').first()
        if u is None:
            u = User()
        u.name = 'Admin'
        u.email = 'kefatong@qq.com'
        u.username = 'administrator'
        u.password = '123456'
        u.confirmed = True
        u.role = adminRole

        db.session.add(u)
        db.session.commit()


    @staticmethod
    def generate_fake(count=1000):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     position=forgery_py.lorem_ipsum.sentence(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
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
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default,
                                                                     rating=rating)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
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

        if data.get('confirm', None) != self.id:
            return False

        self.confirmed = True
        print self.confirmed
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('reset', None) != self.id:
            return False

        self.password = new_password
        db.session.add(self)
        return True

    def generate_change_email_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('change_email') != self.id:
            return False

        new_email = data.get('new_email', None)

        if new_email is None:
            return False

        if self.query.filter_by(email=new_email).first() is not None:
            return False

        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('UTF-8')).hexdigest()
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username



class ClassType(db.Model):
    __tablename__ = 'classType'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)  # 璧勪骇绫诲悕
    type = db.Column(db.Integer)      # 网络设备, 存储设备,  服务器,  资产
    remarks = db.Column(db.Text)  # 璧勪骇绫昏鏄�
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def to_json(self):
        json_classType = {
            'id' : self.id,
            'url': self.id,
            'name' : self.name,
            'type' : self.type,
            'remarks' : self.remarks,
            'isdelete': self.isdelete,
        }

        return json_classType

    def __repr__(self):
        return '<DeviceType %r>' % self.name


class DeviceDisks(db.Model):
    __tablename__ = 'deviceDisks'
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer)
    sn = db.Column(db.String(64))
    size = db.Column(db.String(32))
    type = db.Column(db.Integer)
    raid = db.Column(db.Integer)
    revolutions = db.Column(db.Integer)
    status = db.Column(db.Integer)
    physics_error = db.Column(db.Integer)
    logic_error = db.Column(db.Integer)
    device_id = db.Column(db.ForeignKey('devices.id'))
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def to_json(self):
        json_deviceDisk = {
            'id' : self.id,
            'url' : url_for('api.deviceDisk', id=self.id, _external=True),
            'slot_id' : self.slot_id,
            'sn' : self.sn,
            'size': self.size,
            'type': self.type,
            'raid': self.raid,
            'revolutions': self.revolutions,
            'status' : self.status,
            'physics_error': self.physics_error,
            'logic_error': self.logic_error,
            'device_id' : self.device_id,
            'isdelete': self.isdelete,
            'remarks': self.remarks
        }

        return json_deviceDisk

    def __repr__(self):
        return '<Disk %r>' % self.sn


class DevicePortMap(db.Model):
    __tablename__ = 'devicePortMap'
    source_id = db.Column(db.Integer, db.ForeignKey('devicePorts.id'), primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('devicePorts.id'), primary_key=True)
    use = db.Column(db.String(64))
    isbond = db.Column(db.Boolean)
    remarks = db.Column(db.Text)
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def __repr__(self):
        return '<DevicePortMap %r connect %r>' % (self.source, self.target)


class DevicePorts(db.Model):
    __tablename__ = 'devicePorts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))            # 接口名称 (eth0)
    ip = db.Column(db.String(32), unique=True, index=True)
    netmask = db.Column(db.String(32))             #子网掩码
    gateway = db.Column(db.String(32))          #网关
    mac = db.Column(db.String(64), unique=True, index=True)
    type = db.Column(db.Integer)     #（公网，内网， 上联接口）
    mode = db.Column(db.Integer)        # 接口类型(电口, 光口)
    rate = db.Column(db.Integer)        #速率
    vlanid = db.Column(db.Integer, default=0)      #交换机vlanid
    source = db.relationship('DevicePortMap', foreign_keys=[DevicePortMap.target_id], backref=db.backref('target', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    target = db.relationship('DevicePortMap', foreign_keys=[DevicePortMap.source_id], backref=db.backref('source', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    model_id = db.Column(db.ForeignKey('deviceModel.id'))
    display = db.Column(db.Boolean, default=False)      #是否显示在管理资产条目显示端口信息
    remarks = db.Column(db.Text)  # 澶囨敞
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def to_json(self):
        json_devicePort = {
            'id' : self.id,
            'url': url_for('api.get_devicePort', id=self.id, _external=True),
            'name': self.name,
            'ip'  : self.ip,
            'mask': self.netmask,
            'gateway' : self.gateway,
            'mac' : self.mac,
            'type': self.type,
            'mode': self.mode,
            'rate': self.rate,
            'vlanid': self.vlanid,
            'model' : url_for('api.get_deviceModel', id=self.model_id, _external=True),
            'model_id' : self.model_id,
            'display': self.display,
            'remarks': self.remarks,
            'isdelete': self.isdelete,
        }

        return json_devicePort

    def map(self, target):
        if not self.is_map(target):
            devicePortMap = DevicePortMap()
            devicePortMap.source = self
            devicePortMap.target = target
            db.session.add(devicePortMap)
            db.session.commit()

    def unmap(self, target):
        devicePortMap = self.target.filter_by(target_id=target.id).first()
        if devicePortMap:
            db.session.delete(devicePortMap)

    def is_map(self, target):
        return self.target.filter_by(target_id=target.id).first() is not None

    def is_map_by(self, source):
        return self.source.filter_by(source_id=source.id).first() is not None

    @staticmethod
    def auto_update_ipaddr(target, value, oldvalue, initiator):
        db.session.add(target)
        db.session.commit()
        from IPy import IP

        prefix = value.split('.')[:-1]
        prefix.append('0')
        prefix = '.'.join(prefix)
        ipRange = str(IP("{0}/{1}".format(prefix, target.netmask)))


        ipPool = IpResourcePools.query.filter(IpResourcePools.range == ipRange).first()
        ipAddr = IpResourceManage.query.filter(IpResourceManage.ip == value).first()
        if ipPool and ipAddr:
            ipAddr.status = 1
            ipAddr.devicePort_id = target.id
            flash(u'IP地址:{0}在IP地址段已经设置为已用.')
            db.session.add(ipAddr)
            db.session.commit()

        else:
            ipPool = IpResourcePools()
            ipPool.netmask = target.netmask
            ipPool.gateway = target.gateway
            ipPool.range = ipRange

            iptype = 1
            if IP(ipRange).iptype() == 'PUBLIC':
                iptype = 2

            ipPool.type = iptype

            db.session.add(ipPool)
            db.session.commit()

            flash(u'成功创建IP地址段: {0}'.format(ipRange))

            ipAddr = IpResourceManage.query.filter(IpResourceManage.ip == value).first()
            if ipAddr:
                ipAddr.status = 1
                ipAddr.devicePort_id = target.id

                db.session.add(ipAddr)
                db.session.commit()

                flash(u'IP地址:{0}在IP地址段已经设置为已用。')


    def __repr__(self):
        return '<DevicePort %r>' % self.id

db.event.listen(DevicePorts.ip, 'set', DevicePorts.auto_update_ipaddr)



class DeviceMemorys(db.Model):
    __tablename__ = 'deviceMemorys'
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer)
    sn = db.Column(db.String(64))
    size = db.Column(db.Integer)
    device_id = db.Column(db.ForeignKey('devices.id'))
    remarks = db.Column(db.Text)  # 澶囨敞
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def to_json(self):
        json_deviceMemory = {
            'id' : self.id,
            'url': url_for('api.get_deviceMemorys', id=self.id, _external=True),
            'solt_id' : self.slot_id,
            'sn' : self.sn,
            'size' : self.size,
            'device_id' : self.device_id,
            'device' : url_for('api.get_device', id=self.device_id, _external=True),
            'remarks' : self.remarks,
            'isdelete' : self.isdelete,
        }

        return json_deviceMemory

    def __repr__(self):
        return '<DeviceMemory %r>' % self.id

class DevicePools(db.Model):
    __tablename__ = 'devicePools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer)
    usedept = db.Column(db.String(64))
    devices = db.relationship('VirtMachine', backref='pool', lazy='dynamic')
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def __repr__(self):
        return '<DevicePools %r>' % self.id


class DevicePower(db.Model):
    __tablename__ = 'devicePowers'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=False)
    ip = db.Column(db.String(64))  # 杩滄帶鍗P鍦板潃
    user = db.Column(db.String(64))
    password_hash = db.Column(db.String(256))
    powerid = db.Column(db.String(256))
    device_id = db.Column(db.ForeignKey('devices.id'), primary_key=True)
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿


    def generate_password_token(self, password):
        from itsdangerous import JSONWebSignatureSerializer as Serializer
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': password})

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = self.generate_password_token(password)


    def to_json(self):
        json_power = {
            'url': url_for('api.get_devicePower', id=self.id, _external=True),
            'id' : self.id,
            'device_id' : self.device_id,
            'device' : url_for('api.get_device', id=self.device_id, _external=True),
            'type' : self.type,
            'enabled' : self.enabled,
            'ip' : self.ip,
            'user' : self.user,
            'password': self.password_hash,
            'powerid': self.powerid,
        }

        return json_power

    def __repr__(self):
        return '<DevicePower %r>' %self.id



class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    classType_id = db.Column(db.ForeignKey('classType.id'))  # 璧勪骇绫诲埆   鍏宠仈AssetType table
    an = db.Column(db.String(64), unique=True, index=True)  # AN 浼佷笟璧勪骇缂栧彿
    sn = db.Column(db.String(64), unique=True, index=True)  # SN 璁惧搴忓垪鍙�
    onstatus = db.Column(db.Integer)  # 浣跨敤鐘舵��
    dateofmanufacture = db.Column(db.DateTime)  # 鐢熶骇鏃堕棿
    manufacturer = db.Column(db.String(64))  # 鐢熶骇鍟�
    brand = db.Column(db.String(64))  # 鍝佺墝
    model = db.Column(db.String(64))  # 鍨嬪彿
    usedept = db.Column(db.String(64))  # 浣跨敤閮ㄩ棬
    usestaff = db.Column(db.String(64))  # 閮ㄩ棬浣跨敤浜�
    mainuses = db.Column(db.String(128))  # 涓昏鐢ㄩ��
    managedept = db.Column(db.String(64))  # 绠＄悊閮ㄩ棬
    managestaff = db.Column(db.String(64))  # 绠＄悊浜�
    koriyasustarttime = db.Column(db.DateTime)  # 缁翠繚寮�濮嬫椂闂�
    koriyasuendtime = db.Column(db.DateTime)  # 缁翠繚缁撴潫鏃堕棿
    equipprice = db.Column(db.Integer)  # 璁惧浠锋牸
    auto_discover = db.Column(db.Boolean)           #自动发现 True , False
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿


    def to_json(self):

        json_asset = {
            'url': url_for('api.get_asset', id=self.id, _external=True),
            #'classType': url_for('api.get_deviceType', id=self.id, _external=True),
            'id' : self.id,
            'an': self.an,
            'sn': self.sn,
            'onstatus': self.onstatus,
            'dateofmanufacture': self.dateofmanufacture,
            'manufacturer': self.manufacturer,
            'brand': self.brand,
            'model': self.model,
            'usedept': self.usedept,
            'usestaff': self.usestaff,
            'mainuses': self.mainuses,
            'managedept': self.managedept,
            'managestaff': self.managestaff,
            'equipprice': self.equipprice,
            'koriyasustarttime': self.koriyasustarttime,
            'koriyasuendtime': self.koriyasuendtime,
            }
        return json_asset

    @staticmethod
    def from_json(json_asset):

        sn = json_asset.get('sn', None)
        if sn is None and sn == '':
            raise ValidationError(u'设备SN不能为空.')

        asset = db.session.query(Asset).filter(sn=json_asset.get('sn')).first()
        if not asset:
            asset = Asset()

        asset.sn = sn
        asset.dateofmanufacture = json_asset.get('dateofmanufacture')
        asset.manufacturer = json_asset.get('manufacturer')
        asset.brand = json_asset.get('brand')
        asset.model = json_asset.get('model')
        asset.auto_discover = True

        return asset


    def __repr__(self):
        return '<Asset %r>' %self.id



class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE', onupdate='CASCADE'))
    rack_id = db.Column(db.ForeignKey('racks.id'))  # 鍏宠仈Rack table id
    classType_id = db.Column(db.ForeignKey('classType.id'))
    hostname = db.Column(db.String(64))  # Hostname
    is_virtualization = db.Column(db.Boolean)  # 鏄惁璺戣櫄鎷熷寲  锛堝 OpenStack Compute锛�
    os = db.Column(db.String(64))  # os绫诲瀷
    cpumodel = db.Column(db.String(64))  # CPU 鍨嬪彿
    cpucount = db.Column(db.Integer)  # CPU 鏍告暟
    memsize = db.Column(db.Integer)  # 鍐呭瓨瀹归噺
    disks = db.relationship('DeviceDisks', backref='device', lazy='dynamic')  # 鍏宠仈 Asset table
    disksize = db.Column(db.String(64))
    memorys = db.relationship('DeviceMemorys', backref='device', lazy='dynamic')
    useracksize = db.Column(db.Integer)
    use = db.Column(db.String(64))     #用途
    business = db.Column(db.Integer)    #所属业务
    powerstatus = db.Column(db.Integer)  #电源状态
    uuid = db.Column(db.String(64))     # Device UUID
    auto_discover = db.Column(db.Boolean)           #自动发现 True , False
    isdelete = db.Column(db.Integer)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿


    def to_json(self):
        deviceAsset = db.session.query(Asset).filter(Asset.id == self.asset_id).first()
        deviceModel = db.session.query(DeviceModel).filter(DeviceModel.device_id == self.id).first()
        devicePorts = db.session.query(DevicePorts).filter(DevicePorts.model_id == deviceModel.id).all()

        ip = None
        for devicePort in devicePorts:
            if devicePort.display:
                ip = devicePort.ip
                print devicePort.ip
        json_device = {
                'url': url_for('api.get_device', id=self.id, _external=True),
                'id' : self.id,
                'asset': url_for('api.get_asset', id=self.id, _external=True),
                'asset_id' : self.asset_id,
                'rack' : url_for('api.get_rack', id=self.id, _external=True),
                'classType' : self.classType_id,
                'an' : deviceAsset.an,
                'sn' : deviceAsset.sn,
                'hostname': self.hostname,
                'ip' : ip,
                'onstatus' : deviceAsset.onstatus,
                'brand' : deviceAsset.brand,
                'model' : deviceAsset.model,
                'usedept' : deviceAsset.usedept,
                'usestaff' : deviceAsset.usestaff,
                'mainuses' : deviceAsset.mainuses,
                'managedept' : deviceAsset.managedept,
                'managestaff' : deviceAsset.managestaff,
                'is_virtualization': self.is_virtualization,
                'os': self.os,
                'cpumodel': self.cpumodel,
                'cpucount': self.cpucount,
                'memsize': self.memsize,
                'disksize': self.disksize,
                'use': self.use,
                'business': self.business,
                'powerstatus': self.powerstatus,
                'uuid' : self.uuid,
                'instaff' : self.instaff,
                'remarks': self.remarks,
        }
        return json_device


    @staticmethod
    def from_json(json_device):

        uuid = json_device.get('uuid', None)
        if uuid is None and uuid == '':
            raise ValidationError(u'UUID不能为空.')

        device = db.session.query(Device).filter(Device.uuid == json_device.get('uuid')).first()
        if not device:
            device = Device()

        device.hostname = json_device.get('hostname')
        device.os = json_device.get('os')
        device.cpumodel = json_device.get('cpumodel')
        device.cpucount = json_device.get('cpucount')
        device.memsize = json_device.get('memsize')
        device.disksize = json_device.get('disksize')
        device.powerstatus = json_device.get('powerstatus')
        device.auto_discover  = True
        device.uuid = uuid

        return device


    @staticmethod
    def auto_update_racksize(target, value, oldvalue, initiator):
        deviceRack = db.session.query(Rack).filter(Rack.id == target.rack_id).first()
        if deviceRack:
            deviceRack.usesize += value
            deviceRack.remainsize -= value
            db.session.add(deviceRack)
            db.session.commit()

    def __repr__(self):
        return '<Device %r>' % self.hostname

db.event.listen(Device.useracksize, 'set', Device.auto_update_racksize)


class VirtMachine(db.Model):
    __tablename__ = 'virtMachine'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.ForeignKey('devices.id'))
    deviceType = db.Column(db.String(64))
    virtType = db.Column(db.Integer)     #虚拟化平台类型 (VMware, KVM)
    pool_id = db.Column(db.Integer, db.ForeignKey('devicePools.id'))    #所属资源池
    hostname = db.Column(db.String(64))  # Hostname
    os = db.Column(db.String(64))  # os绫诲瀷
    cpumodel = db.Column(db.String(64))  # CPU 鍨嬪彿
    cpucount = db.Column(db.Integer)  # CPU 鏍告暟
    memsize = db.Column(db.Integer)  # 鍐呭瓨瀹归噺
    disksize = db.Column(db.String(64))
    business = db.Column(db.Integer)    #所属业务
    powerstatus = db.Column(db.Integer)  #电源状态
    onstatus = db.Column(db.Integer)  # 浣跨敤鐘舵��
    usedept = db.Column(db.String(64))  # 浣跨敤閮ㄩ棬
    usestaff = db.Column(db.String(64))  # 閮ㄩ棬浣跨敤浜�
    mainuses = db.Column(db.String(128))  # 涓昏鐢ㄩ��
    managedept = db.Column(db.String(64))  # 绠＄悊閮ㄩ棬
    managestaff = db.Column(db.String(64))  # 绠＄悊浜�
    uuid = db.Column(db.String(64))
    isdelete = db.Column(db.Boolean)
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿
    remarks = db.Column(db.Text)  # 澶囨敞

    def to_json(self):
        json_virtMachine = {
            'url' : self.id,
            'device_id' : self.device_id,
            'device' : url_for('api.get_device', id=self.device_id, _external=True),
            'deviceType': self.deviceType,
            'virtType': self.virtType,
            'pool_id' : self.pool_id,
            'hostname' : self.hostname,
            'os' : self.os,
            'cpumodel' : self.cpumodel,
            'cpucount' : self.cpucount,
            'memsize' : self.memsize,
            'disksize' : self.disksize,
            'business' : self.business,
            'powerstatus' : self.powerstatus,
            'onstatus' : self.onstatus,
            'usedept' : self.usedept,
            'usestaff' : self.usestaff,
            'mainues' : self.mainuses,
            'managedept' : self.managestaff,
            'managestaff' : self.managestaff,
            'uuid' : self.uuid,
            'remarks' : self.remarks,
            'isdelete' : self.isdelete,
        }
        return json_virtMachine


    def __repr__(self):
        return '<VirtMachine %r>' % self.hostname


class DeviceModel(db.Model):
    __tablename__ = 'deviceModel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer)    #模块类型
    portcount = db.Column(db.Integer)       #端口数量
    slot_id = db.Column(db.Integer)
    sn = db.Column(db.String(64))
    device_id = db.Column(db.ForeignKey('devices.id'))
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def to_json(self):
        deviceModel = {
            'id' : self.id,
            'url' : url_for('api.get_deviceModel', id=self.id, _external=True),
            'name' : self.name,
            'type' : self.type,
            'portcount' : self.portcount,
            'slot_id' : self.slot_id,
            'sn' : self.sn,
            'device_id' : self.device_id,
            'device' : url_for('api.get_device', id=self.device_id, _external=True),
            'isdelete' : self.isdelete,
            'remarks' : self.remarks,
        }

        return deviceModel

    def __repr__(self):
        return '<Model %r>' % self.name


class DeviceNetwork(db.Model):
    __tablename__ = 'deviceNetwork'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))     #主机名
    classType_id = db.Column(db.Integer, db.ForeignKey('classType.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    rack_id = db.Column(db.Integer, db.ForeignKey('racks.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('deviceModel.id'))
    firmversion = db.Column(db.String(64))     #固件版本
    enginecount = db.Column(db.Integer)      #引擎数量
    powercount = db.Column(db.Integer)          #电源数量
    powertype = db.Column(db.Integer)           #电源类型 (直流, 交流)
    fancount = db.Column(db.Integer)            #风扇数量
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿
    remarks = db.Column(db.Text)  # 澶囨敞

    def to_json(self):
        deviceNetwork = {
            'id' : self.id,
            'url' : self.id,
            'hostname' : self.hostname,
            'classType' : self.classType_id,
            'asset' : self.asset_id,
            'rack' : self.rack_id,
            'model' : self.model_id,
            'firmversion' : self.firmversion,
            'enginecount' : self.enginecount,
            'powercount' : self.powercount,
            'powertype' : self.powertype,
            'fancount' : self.fancount,
            'remarks' : self.remarks,
            'isdelete' : self.isdelete,
        }

        return deviceNetwork

    def __repr__(self):
        return '<Switch %r>' % self.id


class IpResourcePools(db.Model):
    __tablename__ = 'ipResourcePools'
    id = db.Column(db.Integer, primary_key=True)
    idc_id = db.Column(db.ForeignKey('idcs.id'))   #锁在机房
    ips = db.relationship('IpResourceManage', backref='ipPool', lazy='dynamic')
    netmask = db.Column(db.String(32))
    gateway = db.Column(db.String(32))             #网关
    range = db.Column(db.String(64))               #ip范围
    type = db.Column(db.Integer)                   #ip类型 (内网,公网)
    vlan = db.Column(db.String(10))                #所在vlan
    remarks = db.Column(db.Text)  # 澶囨敞


    def __repr__(self):
        return '<IpPool %r>' % self.range


    @staticmethod
    def auto_insert_ipaddr(target, value, oldvalue, initiator):
        from IPy import IP

        ipRange = IP(value)
        if not IpResourcePools.query.filter(IpResourcePools.range == str(ipRange)).all():

            for ipaddr in ipRange[1:-1]:
                status = 0
                port_id = None
                devicePort = DevicePorts.query.filter(DevicePorts.ip==ipaddr).first()
                if devicePort:
                    status = 1
                    port_id = devicePort.id
                ip = IpResourceManage()
                ip.ipPool = target
                ip.ip = ipaddr
                ip.status = status
                ip.devicePort_id = port_id
                db.session.add(ip)
                db.session.commit()


db.event.listen(IpResourcePools.range, 'set', IpResourcePools.auto_insert_ipaddr)


class IpResourceManage(db.Model):
    __tablename__ = 'ipResourceManage'
    id = db.Column(db.Integer, primary_key=True)
    ipPool_id = db.Column(db.Integer, db.ForeignKey('ipResourcePools.id'))
    ip = db.Column(db.String(20))
    status = db.Column(db.Integer)              # 可用, 已用, 主机地址, 广播地址
    devicePort_id = db.Column(db.Integer, db.ForeignKey('devicePorts.id'))

    def __repr__(self):
        return '<ipManage %r:%r>' % (self.ip, self.status)



class Idc(db.Model):
    __tablename__ = 'idcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ispid = db.Column(db.String(64))  # 杩愯惀鍟嗗悕绉�
    racks = db.relationship('Rack', backref='idc', lazy='dynamic')  # 鍏宠仈Rack
    contactname = db.Column(db.String(64))
    contactphone = db.Column(db.String(64))  # 鑱旂郴浜�
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    nettype = db.Column(db.Integer)  # 缃戠粶绫诲瀷
    netout = db.Column(db.String(64))  # 鍑哄彛甯﹀
    address = db.Column(db.String(128))  # 鏈烘埧鍦板潃
    city = db.Column(db.String(64))  # 鍩庡競
    adnature = db.Column(db.Integer)  # 鏈烘埧鎬ц川
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿
    remarks = db.Column(db.Text)  # 澶囨敞

    def to_json(self):
        json_idc = {
            'id' : self.id,
            'url' : url_for('api.get_idc', id=self.id, _external=True),
            'name' : self.name,
            'ispid' : self.ispid,
            'contactname' : self.contactname,
            'contactphone' : self.contactphone,
            'nettype' : self.nettype,
            'netout' : self.netout,
            'address' : self.address,
            'city' : self.city,
            'adnature' : self.adnature,
            'remarks' : self.remarks,
            'isdelete' : self.isdelete,
        }

        return json_idc

    def __repr__(self):
        return '<Idc %r>' % self.name


class Rack(db.Model):
    __tablename__ = 'racks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    staff = db.Column(db.String(64))  # 鏈烘煖璐熻矗浜�
    idc_id = db.Column(db.ForeignKey('idcs.id'))  # 鍏宠仈IDC table id
    site = db.Column(db.String(64))  # 鏈烘煖浣嶇疆
    racktype = db.Column(db.String(64))  # 鏈烘煖绫诲瀷
    usesize = db.Column(db.Integer)  # 宸茬敤绌洪棿锛坲锛�
    remainsize = db.Column(db.Integer)  # 鍓╀綑绌洪棿锛圲锛�
    electrictype = db.Column(db.String(32))  # 鐢靛姏绫诲瀷
    electricno = db.Column(db.String(32))  # 鐢靛姏璺暟
    electriccapacity = db.Column(db.Integer)  # 鐢靛姏瀹归噺
    leftelectric = db.Column(db.Integer)  # 鍓╀綑鐢靛姏
    renttime = db.Column(db.DateTime, default=datetime.now)  # 绉熺敤鏃堕棿
    expiretime = db.Column(db.DateTime, default=datetime.now)  # 杩囨湡鏃堕棿
    nextpaytime = db.Column(db.DateTime, default=datetime.now)  # 涓嬫鏀粯鏃堕棿
    money = db.Column(db.Integer)  # 鏀粯閲戦
    isdelete = db.Column(db.Boolean, default=False)  # 鏄惁鍒犻櫎
    remarks = db.Column(db.Text)  # 澶囨敞
    instaff = db.Column(db.String(64))  # 褰曞叆浜�
    inputtime = db.Column(db.DateTime, default=datetime.now)  # 褰曞叆鏃堕棿

    def to_json(self):
        json_rack = {
            'id' : self.id,
            'url' : self.id,
            'name' : self.name,
            'staff' : self.staff,
            'idc' : url_for('api.get_idc', id=self.idc_id, _external=True),
            'idc_id' : self.idc_id,
            'site' : self.site,
            'racktype' : self.racktype,
            'usesize' : self.usesize,
            'remainsize' : self.remainsize,
            'electrictype' : self.electrictype,
            'electricno' : self.electricno,
            'electriccapacity' : self.electriccapacity,
            'leftelectric' : self.leftelectric,
            'renttime' : self.renttime,
            'expiretime' : self.expiretime,
            'nextpaytime' : self.nextpaytime,
            'money' : self.money,
            'remarks' : self.remarks,
            'isdelete' : self.isdelete,
        }

        return json_rack

    def __repr__(self):
        return '<Rack %r>' % self.idcname



class Logger(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    logtime = db.Column(db.DateTime, default=datetime.now())
    content = db.Column(db.String(256))
    # action  [ 1: add , 2: edit, 3: del ]
    action = db.Column(db.String(32))
    logobjtype = db.Column(db.String(64))
    logobj_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Logs %r>' % self.user_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

