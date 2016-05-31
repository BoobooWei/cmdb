#coding:utf8

_author__ = 'eric'


from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Email, Length, Regexp, EqualTo, InputRequired, IPAddress, HostnameValidation, MacAddress, NumberRange
from ..models import Role, Rack, Asset, Idc, Device

class NameForm(Form):
    name = StringField('what is your name?', validators=[InputRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(0,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    name = StringField(u'真实姓名', validators=[InputRequired(), Length(0,64)])
    qq = StringField(u'QQ号码')
    phone = StringField(u'手机号码')
    location = StringField(u'位置', validators=[Length(0,64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField('Email',validators=[InputRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    confirmed = BooleanField(u'confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')


class EditAssetTypeForm(Form):
    name = StringField(u'资产类名', validators=[InputRequired() ,Length(1,64)])             # 资产类名
    rremarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def validate_name(self,field):
        if Asset.query.filter_by(name=field.data).first():
            raise ValidationError('资产类名:{0}已经被使用了'.format(self.name))


class EditAssetForm(Form):
    assetclass = SelectField(u'资产类型', coerce=int)   # 资产类别   关联AssetType table
    an = StringField(u'AN号', validators=[InputRequired() ,Length(1,64)])   # AN 企业资产编号
    sn = StringField(u'SN号', validators=[InputRequired() ,Length(1,64)])                           # SN 设备序列号
    onstatus = SelectField(u'使用状态', coerce=int)                        # 使用状态
    flowstatus = SelectField(u'流程状态', coerce=int)                      # 流程状态
    dateofmanufacture = DateTimeField(u'生产时间')              # 生产时间
    manufacturer = StringField(u'生产商', validators=[Length(1,64)])                 # 生产商
    brand = StringField(u'品牌', validators=[Length(1,64)])                        # 品牌
    model = StringField(u'型号', validators=[Length(1,64)])                        # 型号
    site = StringField(u'位置', validators=[Length(1,64)])                         # 位置
    usedept = StringField(u'使用部门', validators=[Length(1,64)])                       # 使用部门
    usestaff = StringField(u'部门使用人', validators=[Length(1,64)])                     # 部门使用人
    usestarttime = DateTimeField(u'使用开始时间')                   # 使用开始时间
    useendtime = DateTimeField(u'使用结束时间')                     # 使用结束时间
    mainuses = StringField(u'部门使用人', validators=[Length(1,128)])                    # 主要用途
    managedept = StringField(u'管理部门', validators=[Length(1,64)])                   # 管理部门
    managestaff = StringField(u'管理人', validators=[Length(1,64)])                  # 管理人
    koriyasustarttime = DateTimeField(u'维保开始时间')              # 维保开始时间
    koriyasuendtime = DateTimeField(u'维保结束时间')                # 维保结束时间
    equipprice = IntegerField(u'设备价格', validators=[NumberRange(0,10,message=u'麻烦输入正确的值好嘛?')])                      # 设备价格
    remarks = TextAreaField(u'备注')                            # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditAssetForm, self).__init__(*args, **kwargs)

        self.assetclass.choices = [(1, u'还没设计')]

        self.onstatus.choices = [(1, u'使用'), (2, u'下线')]

        self.flowstatus.choices = [(1, u'正在审批'), (2, u'未审批')]

    def validate_an(self,field):
        if Asset.query.filter_by(an=field.data).first():
            raise ValidationError('AN:{0}已经被使用了'.format(self.an))

    def validate_sn(self,field):
        if Asset.query.filter_by(sn=field.data).first():
            raise ValidationError('SN:{0}已经被使用了'.format(self.sn))




class EditIdcForm(Form):
    name = StringField(u'Idc名称', validators=[InputRequired() ,Length(1,64)])
    ispname = StringField(u'运营商名称', validators=[InputRequired() ,Length(1,64)])                        # 运营商名称
    city = StringField(u'城市', validators=[InputRequired() ,Length(1,64)])                         # 城市
    address = StringField(u'机房地址', validators=[InputRequired() ,Length(1,64)])                     # 机房地址
    contactid = StringField(u'联系人', validators=[InputRequired() ,Length(1,64)])
    nettype = SelectField(u'网络类型', coerce=int)                      # 网络类型
    netout = StringField(u'出口带宽', validators=[InputRequired() ,Length(1,64)])                       # 出口带宽
    adnature = SelectField(u'机房类型', validators=[InputRequired() ,Length(1,64)])                     # 机房性质
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditIdcForm, self).__init__(*args, **kwargs)

        self.nettype.choices = [(1, u'单电信，单联通，双BGP，联通电信双线')]

        self.adnature.choices = [(1, u'租用，自建，合作，其他')]

    def validate_name(self,field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('Idc名称:{0}已经被使用了'.format(self.name))





class EditDeviceForm(Form):
    hostname = StringField(u'主机名', validators=[HostnameValidation, Length(0,64)])
    private_ip = StringField(u'内网IP', validators=[IPAddress(message=u'麻烦输入IP地址好嘛?'), Length(0,15)])
    private_mac = StringField(u'内网MAC', validators=[MacAddress(message=u'麻烦输入MAC地址好嘛?'), Length(0,20)])
    public_ip = StringField(u'公网IP', validators=[IPAddress(message=u'麻烦输入IP地址好嘛?'), Length(0,15)])                    # 公网IP地址
    public_mac = StringField(u'公网MAC', validators=[MacAddress(message=u'麻烦输入MAC地址好嘛?'), Length(0,20)])
    other_ip = StringField(u'其他IP', validators=[Length(0,64)])                        # 其他IP地址， 用“，”分隔多个
    idc = SelectField(u'机房', coerce=int)                          # 关联IDC table id
    rack = SelectField(u'机柜', coerce=int)                  # 关联Rack table id
    is_virtualization = BooleanField(u'虚拟化')               # 是否跑虚拟化  （如 OpenStack Compute）
    asset = SelectField(u'设备类型', coerce=int)           # 关联Asset 主表 id
    cpumodel = StringField(u'CPU型号', validators=[Length(0,64)])                     # CPU 型号
    cpucount = IntegerField(u'CPU内核(个)', validators=[NumberRange(0,2,message=u'麻烦输入正确的值好嘛?')])                        # CPU 核数
    memsize = IntegerField(u'内存大小(GB)', validators=[NumberRange(0,4,message=u'麻烦输入正确的值好嘛?')])                      # 内存容量
    singlemem = IntegerField(u'单根大小(GB)',validators=[NumberRange(0,4,message=u'麻烦输入正确的值好嘛?')])                       # 单根内存大小
    raidmodel = StringField(u'Raid级别', validators=[Length(0,16)])                    # RAID 级别
    disksize = IntegerField(u'磁盘大小(GB)', validators=[NumberRange(0,10,message=u'麻烦输入正确的值好嘛?')])                        # 磁盘容量
    remotecardip = StringField(u'远控卡IP', validators=[Length(0,15)])                 # 远控卡IP地址
    networkportcount = IntegerField(u'网卡端口(个)',validators=[NumberRange(0,3,message=u'麻烦输入正确的值好嘛?')])                # 网卡端口数量
    os = StringField(u'系统类型', validators=[IPAddress(message=u'麻烦输入IP地址好嘛?'), Length(0,64)])                           # os类型
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDeviceForm, self).__init__(*args, **kwargs)

        self.idc.choices = [(idc.id, idc.name)
                             for idc in Idc.query.order_by(Idc.name).all()]

        self.rack.choices = [(rack.id, rack.name)
                             for rack in Rack.query.order_by(Rack.name).all()]

        self.asset.choices = [(asset.id, asset.sn)
                             for asset in Asset.query.order_by(Asset.sn).all()]


    def validate_privateIP(self, field):
        if Device.query.filter_by(private_ip=field.data).first():
                raise ValidationError(u'内网IP: {0} 已经用了.'.format(self.private_ip))

    def validate_public_ip(self, field):
        if Device.query.filter_by(public_ip=field.data).first():
                raise ValidationError(u'公网IP: {0} 已经用了.'.format(self.public_ip))

    def validate_remotecardip(self, field):
        if Device.query.filter_by(remotecardip=field.data).first():
                raise ValidationError(u'远控卡IP: {0} 已经用了.'.format(self.remotecardip))


class EditRackForm(Form):
    name = StringField(u'机柜名称', validators=[InputRequired(), Length(1,64)])
    staff = StringField(u'管理人', validators=[Length(0,64)])                        # 机柜负责人
    idc = SelectField(u'机房', coerce=int)
    site = StringField(u'机柜位置', validators=[Length(1,64)])                         # 机柜位置
    racktype = SelectField(u'机柜类型', coerce=int)                     # 机柜类型
    usesize = IntegerField(u'已用(u)', validators=[NumberRange(0,2,message=u'麻烦输入正确的值好嘛?')])                      # 已用空间（u）
    remainsize = IntegerField(u'可用(u)', validators=[NumberRange(0,2,message=u'麻烦输入正确的值好嘛?')])                   # 剩余空间（U）
    electrictype = SelectField(u'电力类型', coerce=int)                 # 电力类型
    electricno = SelectField(u'电力路数(单, 双)', coerce=int)                   # 电力路数
    electriccapacity = IntegerField(u'电力容量(A)', validators=[NumberRange(0,2,message=u'麻烦输入正确的值好嘛?')])             # 电力容量
    leftelectric = IntegerField(u'剩余容量(A)', validators=[NumberRange(0,2,message=u'麻烦输入正确的值好嘛?')])                 # 剩余电力
    renttime = DateTimeField(u'租用时间')                   # 租用时间
    expiretime = DateTimeField(u'过期时间')                     # 过期时间
    nextpaytime = DateTimeField(u'下次支付时间')                    # 下次支付时间
    money = IntegerField(u'支付金额', validators=[NumberRange(0,10,message=u'麻烦输入正确的值好嘛?')])                        # 支付金额
    remarks = TextAreaField(u'备注')                            # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditRackForm, self).__init__(*args, **kwargs)

        self.idc.choices = [(idc.id, idc.name)
                             for idc in Idc.query.order_by(Idc.name).all()]

        self.racktype.choices = [(racktype.id, racktype.name)
                             for racktype in Rack.query.order_by(Rack.name).all()]

        self.electrictype.choices = [(1, u'直流'), (1, u'交流')]

        self.electricno.choices = [(1, u'单路'), (1, u'双路')]


    def validate_name(self, field):
        if Rack.query.filter_by(name=field.data).first():
                raise ValidationError(u'Idc名称: {0} 已经创建了.'.format(self.name))
