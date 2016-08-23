#coding:utf8

_author__ = 'eric'


from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, DateTimeField, SelectMultipleField, DateField
from wtforms.validators import Email, Length, Regexp, EqualTo, InputRequired, IPAddress, HostnameValidation, MacAddress, NumberRange
from ..models import *
from .. import db
from wtforms import ValidationError


class EditProfileForm(Form):
    username = StringField(u'用户姓名', validators=[InputRequired(), Length(0,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    name = StringField(u'真实姓名', validators=[InputRequired(), Length(0,64)])
    position = StringField(u'工作职位', validators=[InputRequired(), Length(0,64)])
    phone = StringField(u'手机号码')
    location = StringField(u'位置', validators=[Length(0,64)])
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField(u'Email',validators=[InputRequired(), Length(1,64), Email()])
    username = StringField(u'用户名', validators=[InputRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    password = PasswordField(u'密码', validators=[InputRequired()])
    confirmed = BooleanField(u'启用')
    name = StringField(u'真实姓名', validators=[Length(0,64)])
    role = SelectField(u'权限', coerce=int)
    position = StringField(u'工作职位')
    phone = StringField(u'手机号码')
    location = StringField(u'位置', validators=[Length(0,64)])
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if self.user:
            if field.data != self.user.email and User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered')
        else:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered')

    def validate_username(self, field):
        if self.user:
            if field.data != self.user.username and User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')
        else:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')



class EditClassTypeForm(Form):
    name = StringField(u'类名', validators=[InputRequired() ,Length(1,64)])             # 类名
    type = SelectField(u'类型', coerce=int)
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, classType, *args, **kwargs):
        super(EditClassTypeForm, self).__init__(*args, **kwargs)
        self.classType = classType

        self.type.choices = [(1, u'服务器'), (2, u'网络设备'), (3, u'存储设备'), (4, u'资产')]

    def validate_name(self,field):
        if not self.classType:
            if ClassType.query.filter_by(name=field.data).first():
                raise ValidationError(u'类名称已经被使用了')
        else:
            if field.data != self.classType.name and ClassType.query.filter_by(name=field.data).first():
                raise ValidationError(u'类名称已经被使用了')



class EditIdcForm(Form):
    name = StringField(u'Idc名称', validators=[InputRequired() ,Length(1,64)])
    ispid = StringField(u'运营商名称', validators=[InputRequired() ,Length(1,64)])                        # 运营商名称
    city = StringField(u'城市', validators=[InputRequired() ,Length(1,64)])                         # 城市
    address = StringField(u'机房地址', validators=[InputRequired() ,Length(1,64)])                     # 机房地址
    contactname = StringField(u'联系人姓名', validators=[InputRequired() ,Length(1,64)])
    contactphone = StringField(u'联系人电话', validators=[InputRequired() ,Length(1,64)])
    nettype = SelectField(u'网络类型', coerce=int)                      # 网络类型
    netout = StringField(u'出口带宽', validators=[InputRequired() ,Length(1,64)])                       # 出口带宽
    adnature = SelectField(u'机房类型', coerce=int)                     # 机房性质
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, idc, *args, **kwargs):
        super(EditIdcForm, self).__init__(*args, **kwargs)

        self.nettype.choices = [(1, u'单电信'), (2, u'单联通'), (3, u'双BGP'), (4, u'联通电信双线')]

        self.adnature.choices = [(1, u'租用'), (2, u'自建'), (3, u'合作'), (4, u'其他')]

        self.idc = idc

    def validate_name(self,field):
        if not self.idc:
            if Idc.query.filter_by(name=field.data).first():
                raise ValidationError(u'机房名称已经被使用了')
        else:
            if field.data != self.idc.name and Idc.query.filter_by(name=field.data).first():
                raise ValidationError(u'机房名称已经被使用了')


class EditAssetForm(Form):
    classType_id = SelectField(u'设备类型', coerce=int)   # 资产类别   关联ClassType table
    an = StringField(u'AN号', validators=[InputRequired() ,Length(1,64)])   # AN 企业资产编号
    sn = StringField(u'SN号', validators=[InputRequired() ,Length(1,64)])                           # SN 设备序列号
    onstatus = SelectField(u'使用状态', coerce=int)                        # 使用状态
    dateofmanufacture = DateField(u'生产时间')              # 生产时间
    manufacturer = StringField(u'生产商', validators=[Length(1,64)])                 # 生产商
    brand = StringField(u'品牌', validators=[Length(0,64)])                        # 品牌
    model = StringField(u'型号', validators=[Length(0,64)])                        # 型号
    usedept = StringField(u'使用部门', validators=[Length(0,64)])                       # 使用部门
    usestaff = StringField(u'部门使用人', validators=[Length(0,64)])                     # 部门使用人
    mainuses = StringField(u'主要用途', validators=[Length(0,128)])                    # 主要用途
    managedept = StringField(u'管理部门', validators=[Length(0,64)])                   # 管理部门
    managestaff = StringField(u'管理人', validators=[Length(0,64)])                  # 管理人
    koriyasustarttime = DateField(u'维保开始时间')              # 维保开始时间
    koriyasuendtime = DateField(u'维保结束时间')                # 维保结束时间
    equipprice = IntegerField(u'设备价格')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, deviceAsset, *args, **kwargs):
        super(EditAssetForm, self).__init__(*args, **kwargs)

        self.classType_id.choices = [(classType.id, classType.name)
                             for classType in ClassType.query.order_by(ClassType.name).all()]

        self.onstatus.choices = [(1, u'已用'), (2, u'空闲'), (3, u'下线'), (3, u'待回收')]

        self.deviceAsset = deviceAsset


    def validate_an(self,field):
        if not self.deviceAsset:
            if Asset.query.filter_by(an=field.data).first():
                raise ValidationError(u'AN已经被使用了')
        else:
            if field.data != self.deviceAsset.an and Asset.query.filter_by(an=field.data).first():
                raise ValidationError(u'AN已经被使用了')

    def validate_sn(self,field):
        if not self.deviceAsset:
            if Asset.query.filter_by(sn=field.data).first():
                raise ValidationError(u'SN已经被使用了')
        else:
            if field.data != self.deviceAsset.sn and Asset.query.filter_by(sn=field.data).first():
                raise ValidationError(u'SN已经被使用了')


class EditDeviceForm(Form):
    asset_id = SelectField(u'资产号', coerce=int)
    classType_id = SelectField(u'设备类型', coerce=int)
    rack_id = SelectField(u'机柜', coerce=int)            # 关联Rack table id
    hostname = StringField(u'主机名', validators=[HostnameValidation, Length(0,64)])
    is_virtualization = BooleanField(u'虚拟化')               # 是否跑虚拟化  （如 OpenStack Compute）
    os = StringField(u'操作系统')
    cpumodel = StringField(u'CPU型号', validators=[Length(0,64)])                     # CPU 型号
    cpucount = IntegerField(u'CPU内核(个)')                        # CPU 核数
    memsize = IntegerField(u'内存大小(GB)')                      # 内存容量
    disksize = IntegerField(u'磁盘大小(GB)')                        # 磁盘容量
    rackusesize = IntegerField(u'使用机柜容量')
    use = StringField(u'用途')
    business = SelectField(u'所属业务', coerce=int)
    powerstatus = SelectField(u'电源状态', coerce=int)
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDeviceForm, self).__init__(*args, **kwargs)

        # self.asset_id.choices = [(asset.id, u'{0}:{1}:{2}:{3}:{4}:{5}'.format(asset.an, asset.sn, asset.brand, asset.model, asset.usedept, asset.usestaff))
        #                          for asset in Asset.query.order_by(Asset.inputtime.desc()).filter(Asset.classType_id == 1).filter(
        #                             Asset.id.notin_(db.session.query(Device.asset_id))
        #                           ).all()]

        self.asset_id.choices = [(asset.id, u'{0}:{1}:{2}:{3}:{4}:{5}'.format(asset.an, asset.sn, asset.brand, asset.model, asset.usedept, asset.usestaff))
                                 for asset in db.session.query(Asset).filter(Asset.classType_id.in_(db.session.query(ClassType.id).filter(ClassType.type == 1))).all()]


        self.classType_id.choices = [(classType.id, classType.name)
                                   for classType in ClassType.query.filter_by(type = 1).order_by(ClassType.name).all()]

        self.rack_id.choices = [(rack.id, rack.name)
                             for rack in Rack.query.order_by(Rack.name).all()]

        self.business.choices = [(1, u'云计算',),(2, u'网站')]

        self.powerstatus.choices = [(1, u'开机'), (2, u'关机')]



class EditVritMachineForm(Form):
    deviceType = SelectField(u'设备类型', coerce=int)   # 资产类别   关联ClassType table
    onstatus = SelectField(u'使用状态', coerce=int)                        # 使用状态
    usedept = StringField(u'使用部门', validators=[Length(1,64)])                       # 使用部门
    usestaff = StringField(u'部门使用人', validators=[Length(1,64)])                     # 部门使用人
    mainuses = StringField(u'主要用途', validators=[Length(1,128)])                    # 主要用途
    managedept = StringField(u'管理部门', validators=[Length(1,64)])                   # 管理部门
    managestaff = StringField(u'管理人', validators=[Length(1,64)])                  # 管理人
    device_id = SelectField(u'运行主机', coerce=int)
    pool = SelectField(u'资源池', coerce=int)
    hostname = StringField(u'主机名', validators=[HostnameValidation, Length(0,64)])
    os = StringField(u'操作系统')
    cpumodel = StringField(u'CPU型号', validators=[Length(0,64)])                     # CPU 型号
    cpucount = IntegerField(u'CPU内核(个)')                        # CPU 核数
    memsize = IntegerField(u'内存大小(GB)')                      # 内存容量
    disksize = IntegerField(u'磁盘大小(GB)')                        # 磁盘容量
    business = SelectField(u'所属业务', coerce=int)
    powerstatus = SelectField(u'电源状态', coerce=int)
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditVritMachineForm, self).__init__(*args, **kwargs)

        self.deviceType.choices = [(1, u'OpenStack'), (2, u'VMware')]

        self.onstatus.choices = [(1, u'已用'), (2, u'空闲'), (3, u'下线'), (3, u'待回收')]

        self.device_id.choices = [(device.id, device.hostname)
                             for device in Device.query.order_by(Device.hostname).filter(Device.is_virtualization == True).all()]

        self.pool.choices = [(pool.id, pool.name)
                             for pool in DevicePools.query.order_by(DevicePools.name).all()]

        self.business.choices = [(1, u'云计算',),(2, u'大数据')]

        self.powerstatus.choices = [(1, u'开机'), (2, u'关机')]






class EditDeviceNetworkForm(Form):
    hostname = StringField(u'主机名', validators=[HostnameValidation, Length(0,64)])
    classType_id = SelectField(u'设备类型', coerce=int)
    asset_id = SelectField(u'资产号', coerce=int)
    rack_id = SelectField(u'机柜', coerce=int)                  # 关联Rack table id
    firmversion = StringField(u'固件版本')
    enginecount = IntegerField(u'引擎数量')      #引擎数量
    powercount = IntegerField(u'电源数量')          #电源数量
    powertype = SelectField(u'电源类型', coerce=int)           #电源类型 (直流, 交流)
    fancount = IntegerField(u'风扇数量')            #风扇数量
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, deviceNetwork, *args, **kwargs):
        super(EditDeviceNetworkForm, self).__init__(*args, **kwargs)

        self.asset_id.choices = [(asset.id, '{0}-{1}-{2}'.format(asset.an, asset.sn, asset.id))
                                 for asset in Asset.query.order_by(Asset.inputtime.desc()).filter(Asset.classType_id == 2).all()]

        self.classType_id.choices = [(classType.id, classType.name)
                                 for classType in ClassType.query.filter(ClassType.type==2).order_by(ClassType.name).all()]

        self.rack_id.choices = [(rack.id, rack.name)
                                for rack in Rack.query.order_by(Rack.name).all()]

        self.powertype.choices = [(1, u'交流'), (2, u'直流')]
        self.deviceNetwork = deviceNetwork


    def validate_hostname(self, field):
        if not self.deviceNetwork:
            if DeviceNetwork.query.filter_by(hostname=field.data).first():
                raise ValidationError(u'Hostname已经被使用了')
        else:
            if field.data != self.deviceNetwork.hostname and DeviceNetwork.query.filter_by(hostname=field.data).first():
                raise ValidationError(u'Hostname已经被使用了')



class EditDevicePortForm(Form):
    name = StringField(u'接口名称', validators=[InputRequired(), Length(1,64)])
    ip = StringField(u'IP地址', validators=[InputRequired()])
    netmask = StringField(u'子网掩码', validators=[InputRequired()])
    gateway = StringField(u'网关')
    mac = StringField(u'Mac地址')
    type = SelectField(u'接口类型', coerce=int)
    mode = SelectField(u'端口类型', coerce=int)
    rate = SelectField(u'速率', coerce=int)
    vlanid = IntegerField(u'VlanID')
    model_id = SelectField(u'模块', coerce=int)
    display = BooleanField(u'显示查询页面')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')


    def __init__(self, devicePorts, *args, **kwargs):
        super(EditDevicePortForm, self).__init__(*args, **kwargs)

        self.type.choices = [(1, u'内网'), (2, u'公网')]

        self.mode.choices = [(1, u'电口'), (2, u'光口')]

        self.rate.choices = [(2, u'1GB'), (1, u'100MB'), (3, u'10GB'), (4, u'100GB')]

        self.model_id.choices = [(model.id, u'{0}.{1}'.format(Device.query.filter(Device.id==model.device_id).first().hostname, model.name ))
                                 for model in DeviceModel.query.all()]

        self.devicePorts = devicePorts

    def validate_mac(self, field):
        if not self.devicePorts:
            if DevicePorts.query.filter_by(mac=field.data).first():
                raise ValidationError(u'mac地址已经被使用了')
        else:
            if field.data != self.devicePorts.mac and DevicePorts.query.filter(DevicePorts.mac==field.data).first():
                raise ValidationError(u'mac地址已经被使用了')

    def validate_ip(self, field):
        if not self.devicePorts:
            if DevicePorts.query.filter(DevicePorts.ip==field.data).first():
                raise ValidationError(u'ip地址已经被使用了')
        else:
            if field.data != self.devicePorts.ip and DevicePorts.query.filter(DevicePorts.ip == field.data).first():
                raise ValidationError(u'ip地址已经被使用了')

class EditDeviceMemoryForm(Form):
    slot_id = IntegerField(u'插槽', validators=[InputRequired(), Length(1,64)])
    sn = StringField(u'序列号')
    size = IntegerField(u'内存大小')
    device = SelectField(u'设备', coerce=int)
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDeviceMemoryForm, self).__init__(*args, **kwargs)

        self.device.choices = [(device.id, device.hostname)
                             for device in Device.query.order_by(Device.hostname).all()]


class EditDeviceDiskForm(Form):
    slot_id = IntegerField(u'插槽', validators=[InputRequired(), Length(1,64)])
    sn = StringField(u'序列号')
    size = IntegerField(u'磁盘大小(GB)')
    type = SelectField(u'磁盘类型', coerce=int)
    raid = SelectField(u'RAID级别', coerce=int)
    revolutions = SelectField(u'磁盘转速', coerce=int)
    status = SelectField(u'健康状态', coerce=int)
    physics_error = IntegerField(u'物理坏道')
    logic_error = IntegerField(u'逻辑坏道')
    device = SelectField(u'连接设备', coerce=int)
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDeviceDiskForm, self).__init__(*args, **kwargs)

        self.type.choices = [(1, u'SAS'),(2, u'STAT'), (3, u'HDD'), (4, u'SSD')]

        self.raid.choices = [(1, u'RAID0'), (2, u'RAID1'), (3, u'RAID5'), (4, u'RAID10')]

        self.revolutions.choices = [(1, u'7200'),(2, u'10000'),(3, u'15000'),(4, u'SSD')]

        self.status.choices = [(1, u'在线'),(2, u'下线')]

        self.device.choices = [(device.id, device.hostname)
                           for device in Device.query.order_by(Device.hostname).all()]


class EditDevicePowerForm(Form):
    device_id = SelectField(u'关联服务器', coerce=int)
    type = SelectField(u'电源模块类型', coerce=int)   # 网络类型
    enabled = BooleanField(u'启用电源管理')
    ip = StringField(u'IP地址', validators=[Length(0,15)])                 # 远控卡IP地址
    user = StringField(u'用户', validators=[Length(0,64)])
    password = PasswordField(u'密码', validators=[InputRequired(), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField(u'确认密码', validators=[InputRequired()])
    powerid = StringField(u'设备ID', validators=[Length(0,64)])          # 缃戝崱绔彛鏁伴噺
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDevicePowerForm, self).__init__(*args, **kwargs)

        self.device_id.choices = [(device.id, device.hostname)
                                  for device in Device.query.all()]

        self.type.choices = [(1, u'IPMI'), (1, u'iLO')]


#    def validate_powermanage_ip(self, field):
#        if DevicePowerManage.query.filter_by(powermanage_ip=field.data).first():
#            raise ValidationError(u'远控卡IP: {0}已经用了'.format(field.data))



class EditDevicePoolsForm(Form):
    type = SelectField(u'资源池类型', coerce=int)
    name = StringField(u'资源池名称', validators=[InputRequired(), Length(1,64)])
    usedept = StringField(u'使用部门')
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDevicePoolsForm, self).__init__(*args, **kwargs)

        self.type.choices = [(1, u'普通'), (2, u'高性能')]


class EditDeviceModelForm(Form):
    name = StringField(u'模块名称', validators=[InputRequired(), Length(1,64)])
    type = SelectField(u'模块类型', coerce=int)
    portcount = IntegerField(u'端口数量')
    slot_id = IntegerField(u'插槽ID', validators=[InputRequired()])
    sn = StringField(u'序列号')
    device_id = SelectField(u'设备', coerce=int)
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')


    def __init__(self, *args, **kwargs):
        super(EditDeviceModelForm, self).__init__(*args, **kwargs)
        self.type.choices = [(1, u'服务器网卡'), (2, u'网络设备模块')]

        device = Device.query.all()
        deviceNetwork = DeviceNetwork.query.all()

        deviceChoices = []
        deviceChoices.extend(device)
        deviceChoices.extend(deviceNetwork)

        self.device_id.choices = [ (device.id, device.hostname)
                                   for device in deviceChoices]


class EditDevicePortMapForm(Form):
    source_id = SelectField(u'设备源端口', coerce=int)
    target_id = SelectField(u'设备目的端口', coerce=int)
    use = StringField(u'用途')
    isbond = BooleanField(u'isbond')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDevicePortMapForm, self).__init__(*args, **kwargs)

        self.source_id.choices = [( port.id, port.name)
                                  for port in DevicePorts.query.all()]

        #self.source_id.choices.append((network.id, network.name)
                                      #for network in DeviceNetwork.query.all())


        self.target_id.choices = [(port.id, port.hostname)
                                  for port in DevicePorts.query.all()]

        #self.target_id.choices.append((network.id, network.name)
                              #for network in DeviceNetwork.query.all())


class EditIpResourcePoolsForm(Form):
    idc_id = SelectField(u'所在机房', coerce=int)
    range = StringField(u'IP范围')
    netmask = StringField(u'子网掩码')
    gateway = StringField(u'网关')
    type = SelectField(u'类型', coerce=int)
    vlan = StringField(u'VlanID')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')


    def __init__(self, *args, **kwargs):
        super(EditIpResourcePoolsForm, self).__init__(*args, **kwargs)

        self.idc_id.choices = [(idc.id, idc.name)
                               for idc in Idc.query.all()]

        self.type.choices = [(1, u'内网'), (2, u'公网')]


class EditIpResourceManageForm(Form):
    ipPool_id = SelectField(u'IP资源池', coerce=int)
    ip = StringField(u'IP地址')
    status = StringField(u'状态')
    devicePort_id = SelectField(u'设备端口')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')


    def __init__(self, *args, **kwargs):
        super(EditIpResourceManageForm, self).__init__(*args, **kwargs)

        self.ipPool_id.choices = [(ipPool.id, ipPool.name)
                                for ipPool in IpResourcePools.query.all()]

        self.devicePort_id.choices = [(devicePort.id, devicePort.name)
                                      for devicePort in DevicePorts.query.all()]



class EditRackForm(Form):
    name = StringField(u'机柜名称', validators=[InputRequired(), Length(1,64)])
    staff = StringField(u'管理人', validators=[Length(0,64)])                        # 机柜负责人
    idc = SelectField(u'机房', coerce=int)
    site = StringField(u'机柜位置', validators=[Length(1,64)])                         # 机柜位置
    racktype = SelectField(u'机柜类型', coerce=int)                     # 机柜类型
    usesize = IntegerField(u'已用(u)')                      # 已用空间（u）
    remainsize = IntegerField(u'可用(u)')                   # 剩余空间（U）
    electrictype = SelectField(u'电力类型', coerce=int)                 # 电力类型
    electricno = SelectField(u'电力路数', coerce=int)                   # 电力路数
    electriccapacity = IntegerField(u'电力容量(A)')             # 电力容量
    leftelectric = IntegerField(u'剩余容量(A)')                 # 剩余电力
    renttime = DateField(u'租用时间')                   # 租用时间
    expiretime = DateField(u'过期时间')                     # 过期时间
    nextpaytime = DateField(u'下次支付时间')                    # 下次支付时间
    money = IntegerField(u'支付金额')                        # 支付金额
    remarks = TextAreaField(u'备注')                            # 备注
    submit = SubmitField(u'提交')

    def __init__(self, rack,*args, **kwargs):
        super(EditRackForm, self).__init__(*args, **kwargs)

        self.idc.choices = [(idc.id, idc.name)
                             for idc in Idc.query.order_by(Idc.name).all()]

        self.racktype.choices = [(1, u'服务器'), (2, u'网络设备')]

        self.electrictype.choices = [(1, u'交流'), (1, u'直流')]

        self.electricno.choices = [(1, u'双路'), (1, u'单路')]

        self.rack = rack

    def validate_name(self, field):
        if not self.rack:
            if Rack.query.filter_by(name=field.data).first():
                raise ValidationError(u'机柜名已经创建了')
        else:
            if field.data != self.rack.name and Rack.query.filter_by(name=field.data).first():
                raise ValidationError(u'机柜名已经创建了')



class EditSearchAssetForm(Form):
    ip = StringField(u'目标IP地址段')
    remote_user = StringField(u'远程用户')
    remote_pass = StringField(u'远程密码')
    sudo_user = StringField(u'sudo用户')
    sudo_pass = StringField(u'sudo密码')