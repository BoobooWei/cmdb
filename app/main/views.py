# coding:utf8

from flask import render_template, redirect, url_for, flash, current_app, abort, request, make_response
from flask.ext.login import login_required, current_user
from ..decorators import admin_required, permission_required
from . import main
from .forms import *
from .. import db
from ..models import *
from ..email import send_email


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    logs = Logger.query.order_by(Logger.logtime.desc()).all()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.position = form.position.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'提交成功!')
        return redirect(url_for('main.edit_profile', username=current_user.username, logs=logs))

    form.name.data = current_user.name
    form.username.data = current_user.username
    form.position.data = current_user.position
    form.location.data = current_user.location
    form.phone.data = current_user.phone
    return render_template('edit_profile.html', form=form, username=current_user.username, logs=logs)


##################################################################


@main.route('/show-system.users', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.USER_LOOK)
def show_system_users():
    users = User.query.all()
    return render_template('show_system_users.html', users=users)


@main.route('/create-system.users', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.USER_EDIT)
def create_system_users():
    form = EditProfileAdminForm(None)
    if form.validate_on_submit():

        user = User()
        user.email = form.email.data
        user.name = form.name.data
        user.username = form.username.data
        user.password = form.password.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.position = form.position.data
        user.phone = form.phone.data
        user.location = form.location.data

        db.session.add(user)
        db.session.commit()
        flash(u'创建用户:{0}成功!'.format(user.username))
        return redirect(url_for('main.show_system_users'))

    return render_template('create_system_users.html', form=form)



@main.route('/edit-system.users/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.USER_EDIT)
def edit_system_users(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():

        user.email = form.email.data
        user.name = form.name.data
        user.username = form.username.data
        user.password = form.password.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.position = form.position.data
        user.phone = form.phone.data
        user.location = form.location.data

        db.session.add(user)
        db.session.commit()
        flash(u'修改用户:{0}成功!'.format(user.username))
        return redirect(url_for('main.show_system_users'))

    form.email.data = user.email
    form.name.data = user.name
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.position.data = user.position
    form.phone.data = user.phone
    form.location.data = user.location

    return render_template('edit_system_users.html', form=form, user=user)


@main.route('/delete-system.users/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.USER_DEL)
def delete_system_users(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    flash(u'删除用户:{0}成功!'.format(user.username))
    return redirect(url_for('main.show_system_users'))


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    #return render_template('index.html')
    return redirect(url_for('main.show_devices'))


##################################################################

@main.route('/create-class.type', methods=['GET', 'POST'])
@login_required
def create_classType():
    form = EditClassTypeForm(classType=None)
    if form.validate_on_submit():
        classType = ClassType()
        classType.name = form.name.data
        classType.type = form.type.data
        classType.remarks = form.remarks.data
        db.session.add(classType)
        db.session.commit()
        flash(u'创建设备类型:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.show_classType'))
    return render_template('create_classType.html', form=form)


@main.route('/edit-class.type/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_classType(id):
    classType = ClassType.query.get_or_404(id)
    form = EditClassTypeForm(classType=classType)
    if form.validate_on_submit():
        classType.name = form.name.data
        classType.type = form.type.data
        classType.remarks = form.remarks.data
        db.session.add(classType)
        db.session.commit()
        flash(u'编辑设备类型:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.show_classType'))

    form.name.data = classType.name
    form.type.data = classType.type
    form.remarks.data = classType.remarks
    return render_template('edit_classType.html', form=form, classType=classType)


@main.route('/show-class.type', methods=['GET', 'POST'])
@login_required
def show_classType():
    classType = ClassType.query.all()
    return render_template('show_classType.html', classType=classType)


@main.route('/delete-class.type/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_classType(id):
    classType = ClassType.query.get_or_404(id)
    db.session.delete(classType)
    flash(u'删除设备类型:{0}成功!'.format(classType.name))
    return redirect(url_for('main.show_classType'))


##################################################################


@main.route('/show-device.ports', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePorts():
    devicePorts = DevicePorts.query.all()
    return render_template('show_devicePorts.html', devicePorts=devicePorts)



@main.route('/create-device.ports', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePorts():
    form = EditDevicePortForm(None)
    if form.validate_on_submit():
        devicePorts = DevicePorts()
        deviceMaps = DevicePortMap()

        devicePorts.name = form.name.data
        devicePorts.netmask = form.netmask.data
        devicePorts.gateway = form.gateway.data
        devicePorts.ip = form.ip.data
        devicePorts.mac = form.mac.data
        devicePorts.type = form.type.data
        devicePorts.mode = form.mode.data
        devicePorts.rate = form.rate.data
        devicePorts.vlanid = form.vlanid.data
        devicePorts.model_id = form.model_id.data
        devicePorts.display = form.display.data
        devicePorts.remarks = form.remarks.data

        db.session.add(devicePorts)
        db.session.commit()
        flash(u'创建设备端口:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.show_devicePorts'))
    return render_template('create_devicePorts.html', form=form)




@main.route('/edit-device.ports/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_devicePorts(id):
    devicePorts = DevicePorts.query.get_or_404(id)
    form = EditDevicePortForm(devicePorts)
    if form.validate_on_submit():

        devicePorts.name = form.name.data
        devicePorts.netmask = form.netmask.data
        devicePorts.gateway = form.gateway.data
        devicePorts.ip = form.ip.data
        devicePorts.mac = form.mac.data
        devicePorts.type = form.type.data
        devicePorts.mode = form.mode.data
        devicePorts.rate = form.rate.data
        devicePorts.vlanid = form.vlanid.data
        devicePorts.model_id = form.model_id.data
        devicePorts.display = form.display.data
        devicePorts.remarks = form.remarks.data

        db.session.add(devicePorts)
        db.session.commit()
        flash(u'修改设备端口:{0}成功!'.format(devicePorts.name))
        return redirect(url_for('main.show_devicePorts'))

    form.name.data = devicePorts.name
    form.netmask.data = devicePorts.netmask
    form.gateway.data = devicePorts.gateway
    form.ip.data = devicePorts.ip
    form.mac.data = devicePorts.mac
    form.type.data = devicePorts.type
    form.mode.data = devicePorts.mode
    form.rate.data = devicePorts.rate
    form.vlanid.data = devicePorts.vlanid
    form.model_id.data = devicePorts.model_id
    form.display.data = devicePorts.display
    form.remarks.data = devicePorts.remarks
    return render_template('edit_devicePorts.html', form=form, devicePorts=devicePorts)


@main.route('/delete-device.ports/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_devicePorts(id):
    devicePorts = DevicePorts.query.get_or_404(id)
    db.session.delete(devicePorts)
    flash(u'删除设备端口:{0}成功!'.format(devicePorts.name))
    return redirect(url_for('main.show_devicePorts'))

##################################################################

@main.route('/show-device.portmaps', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePortMaps():
    devicePortMap = DevicePortMap.query.all()
    return render_template('test.html', devicePortMap=devicePortMap)


@main.route('/create-device.portmap', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePortMap():
    form = EditDevicePortMapForm()
    if form.validate_on_submit():
        devicePortMap = DevicePortMap()

        devicePortMap.source_id = form.source_id.data
        devicePortMap.target_id = form.target_id.data
        devicePortMap.use = form.use.data
        devicePortMap.isbond = form.isbond.data
        devicePortMap.remarks = form.remarks.data

        db.session.add(devicePortMap)
        flash(u'创建端口映射成功!')
        db.session.commit()
        return redirect(url_for('main.show_devicePortMaps'))
    return render_template('create_devicePortMap.html', form=form)



##################################################################

@main.route('/show-device.memorys', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_deviceMemorys():
    deviceMemorys = DeviceMemorys.query.all()
    return render_template('test.html', deviceMemorys=deviceMemorys)


@main.route('/create-device.memorys', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_deviceMemorys():
    form = EditDeviceMemoryForm()
    if form.validate_on_submit():
        deviceMemorys = DeviceMemorys()

        deviceMemorys.slot_id = form.slot_id.data
        deviceMemorys.sn = form.sn.data
        deviceMemorys.size = form.size.data
        deviceMemorys.device = Device.query.get(form.device.data)
        deviceMemorys.remarks = form.remarks.data

        db.session.add(deviceMemorys)
        flash(u'创建设备内存:{0}成功!'.format(form.sn.data))
        db.session.commit()
        return redirect(url_for('main.show_deviceMemorys'))
    return render_template('test.html', form=form)


@main.route('/edit-device.memorys/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_deviceMemorys(id):
    deviceMemorys = DeviceMemorys.query.get_or_404(id)
    form = EditDeviceMemoryForm()
    if form.validate_on_submit():
        deviceMemorys.slot_id = form.slot_id.data
        deviceMemorys.sn = form.sn.data
        deviceMemorys.size = form.size.data
        deviceMemorys.device = Device.query.get(form.device.data)
        deviceMemorys.remarks = form.remarks.data

        db.session.add(deviceMemorys)
        db.session.commit()
        flash(u'修改设备内存:{0}成功!'.format(deviceMemorys.sn))
        return redirect(url_for('main.show_deviceMemorys'))

    form.slot_id.data = deviceMemorys.slot_id
    form.sn.data = deviceMemorys.sn
    form.size.data = deviceMemorys.size
    form.device.data = deviceMemorys.device
    form.remarks.data = deviceMemorys.remarks

    return render_template('test.html', form=form)


@main.route('/delete-device.memorys/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_deviceMemorys(id):
    deviceMemorys = DeviceMemorys.query.get_or_404(id)
    db.session.delete(deviceMemorys)
    flash(u'内存: {0} 已删除!'.format(deviceMemorys.id))
    return redirect(url_for('main.show_deviceMemorys'))


#######################################################################

@main.route('/show-device.disks', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_deviceDisks():
    deviceDisks = DeviceDisks.query.all()
    return render_template('test.html', deviceDisks=deviceDisks)


@main.route('/create-device.disks', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_deviceDisks():
    form = EditDeviceDiskForm()
    if form.validate_on_submit():
        deviceDisks = DeviceDisks()

        deviceDisks.slot_id = form.slot_id.data
        deviceDisks.sn = form.sn.data
        deviceDisks.size = form.size.data
        deviceDisks.type = form.type.data
        deviceDisks.raid = form.raid.data
        deviceDisks.revolutions = form.revolutions.data
        deviceDisks.status = form.status.data
        deviceDisks.physics_error = form.physics_error.data
        deviceDisks.logic_error = form.logic_error.data
        deviceDisks.device = Device.query.get(form.device.data)
        deviceDisks.remarks = form.remarks.data

        db.session.add(deviceDisks)
        flash(u'创建设备磁盘:{0}成功!'.format(form.sn.data))
        db.session.commit()
        return redirect(url_for('main.create_deviceDisks'))
    return render_template('test.html', form=form)


@main.route('/edit-device.disks/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_deviceDisks(id):
    deviceDisks = DeviceDisks.query.get_or_404(id)
    form = EditDeviceDiskForm()
    if form.validate_on_submit():
        deviceDisks.slot_id = form.slot_id.data
        deviceDisks.sn = form.sn.data
        deviceDisks.size = form.size.data
        deviceDisks.type = form.type.data
        deviceDisks.raid = form.raid.data
        deviceDisks.revolutions = form.revolutions.data
        deviceDisks.status = form.status.data
        deviceDisks.physics_error = form.physics_error.data
        deviceDisks.logic_error = form.logic_error.data
        deviceDisks.device = Device.query.get(form.device.data)
        deviceDisks.remarks = form.remarks.data

        db.session.add(deviceDisks)
        db.session.commit()
        flash(u'修改设备内存:{0}成功!'.format(deviceDisks.sn))
        return redirect(url_for('main.create_deviceDisks'))

    form.slot_id.data = deviceDisks.slot_id
    form.sn.data = deviceDisks.sn
    form.size.data = deviceDisks.size
    form.type.data = deviceDisks.type
    form.raid.data = deviceDisks.raid
    form.revolutions.data = deviceDisks.revolutions
    form.status.data = deviceDisks.status
    form.physics_error.data = deviceDisks.physics_error
    form.logic_error.data = deviceDisks.logic_error
    form.device.data = deviceDisks.device
    form.remarks.data = deviceDisks.remarks

    return render_template('test.html', form=form)


@main.route('/delete-device.disks/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_deviceDisks(id):
    deviceDisks = DeviceDisks.query.get_or_404(id)
    db.session.delete(deviceDisks)
    flash(u'磁盘: {0} 已删除!'.format(deviceDisks.id))
    return redirect(url_for('main.create_deviceDisks'))


#######################################################################


@main.route('/show-device.pools', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePools():
    devicePools = DevicePools.query.all()
    return render_template('show_devicePools.html', devicePools=devicePools)


@main.route('/create-device.pools', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePools():
    form = EditDevicePoolsForm()
    if form.validate_on_submit():
        devicePools = DevicePools()
        devicePools.name = form.name.data
        devicePools.type = form.type.data
        devicePools.usedept = form.usedept.data
        devicePools.remarks = form.remarks.data
        db.session.add(devicePools)
        db.session.commit()
        flash(u'创建资源池:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.show_devicePools'))
    return render_template('create_devicePools.html', form=form)


@main.route('/edit-device.pools/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_devicePools(id):
    devicePools = DevicePools.query.get_or_404(id)
    form = EditDevicePoolsForm()
    if form.validate_on_submit():
        devicePools.name = form.name.data
        devicePools.type = form.type.data
        devicePools.usedept = form.usedept.data
        devicePools.remarks = form.remarks.data

        db.session.add(devicePools)
        db.session.commit()
        flash(u'修改资源池:{0}成功!'.format(devicePools.name))
        return redirect(url_for('main.show_devicePools'))

    form.name.data = devicePools.name
    form.type.data = devicePools.type
    form.usedept.data = devicePools.usedept
    form.remarks.data = devicePools.remarks
    return render_template('edit_devicePools.html', form=form, devicePools=devicePools)


@main.route('/delete-device.pools/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_devicePools(id):
    devicePools = DevicePools.query.get_or_404(id)
    db.session.delete(devicePools)
    flash(u'资源池: {0} 已删除!'.format(devicePools.id))
    return redirect(url_for('main.show_devicePools'))


########################################################################

@main.route('/show-device.devicePowers', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePower():
    devicePowers = DevicePower.query.all()
    return render_template('show_devicePowers.html', devicePowers=devicePowers)


@main.route('/create-device.devicePower', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePower():
    form = EditDevicePowerForm()
    if form.validate_on_submit():
        devicePower = DevicePower()

        devicePower.device_id = form.device_id.data
        devicePower.type = form.type.data
        devicePower.enabled = form.enabled.data
        devicePower.ip = form.ip.data
        devicePower.user = form.user.data
        devicePower.password = form.password.data
        devicePower.powerid = form.powerid.data
        devicePower.remarks = form.remarks.data

        db.session.add(devicePower)
        db.session.commit()
        flash(u'创建电源管理:{0}成功!'.format(devicePower.ip))
        return redirect(url_for('main.show_devicePower'))
    return render_template('create_devicePower.html', form=form)


@main.route('/edit-device.devicePower/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_devicePower(id):
    devicePower = DevicePower.query.get_or_404(id)
    form = EditDevicePowerForm()
    if form.validate_on_submit():
        devicePower.device_id = form.device_id.data
        devicePower.type = form.type.data
        devicePower.enabled = form.enabled.data
        devicePower.ip = form.ip.data
        devicePower.user = form.user.data
        devicePower.password = form.password.data
        devicePower.powerid = form.powerid.data
        devicePower.remarks = form.remarks.data

        db.session.add(devicePower)
        db.session.commit()
        flash(u'修改电源管理:{0}成功!'.format(devicePower.ip))
        return redirect(url_for('main.show_devicePower'))

    form.device_id.data = devicePower.device_id
    form.type.data = devicePower.type
    form.enabled.data = devicePower.enabled
    form.ip.data = devicePower.ip
    form.user.data = devicePower.user
    form.password.data = devicePower.password_hash
    form.powerid.data = devicePower.powerid
    form.remarks.data = devicePower.remarks

    return render_template('edit_devicePower.html', form=form, devicePower=devicePower)


@main.route('/delete-device.devicePower/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_devicePower(id):
    devicePower = DevicePower.query.get_or_404(id)
    db.session.delete(devicePower)
    flash(u'电源管理: {0} 已删除!'.format(devicePower.ip))
    return redirect(url_for('main.show_devicePower'))



########################################################################


@main.route('/show-device.models', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_deviceModels():
    deviceModels = DeviceModel.query.all()
    return render_template('show_deviceModels.html', deviceModels=deviceModels)


@main.route('/create-device.model', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_deviceModel():
    form = EditDeviceModelForm()
    if form.validate_on_submit():
        deviceModel = DeviceModel()

        deviceModel.name = form.name.data
        deviceModel.type = form.type.data
        deviceModel.slot_id = form.slot_id.data
        deviceModel.portcount = form.portcount.data
        deviceModel.sn = form.sn.data
        deviceModel.device_id = form.device_id.data
        deviceModel.remarks = form.remarks.data

        db.session.add(deviceModel)
        db.session.commit()
        flash(u'创建模块:{0}成功!'.format(deviceModel.name))
        return redirect(url_for('main.show_deviceModels'))
    return render_template('create_deviceModel.html', form=form)


@main.route('/edit-device.model/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_deviceModel(id):
    deviceModel = DeviceModel.query.get_or_404(id)
    form = EditDeviceModelForm()
    if form.validate_on_submit():

        deviceModel.name = form.name.data
        deviceModel.type = form.type.data
        deviceModel.slot_id = form.slot_id.data
        deviceModel.portcount = form.portcount.data
        deviceModel.sn = form.sn.data
        deviceModel.device_id = form.device_id.data
        deviceModel.remarks = form.remarks.data

        db.session.add(deviceModel)
        db.session.commit()
        flash(u'创建模块:{0}成功!'.format(deviceModel.name))
        return redirect(url_for('main.show_deviceModels'))

    form.name.data = deviceModel.name
    form.type.data = deviceModel.type
    form.slot_id.data = deviceModel.slot_id
    form.portcount.data = deviceModel.portcount
    form.sn.data = deviceModel.sn
    form.device_id.data = deviceModel.device_id
    form.remarks.data = deviceModel.remarks

    return render_template('edit_deviceModel.html', form=form, deviceModel=deviceModel)



@main.route('/delete-device.model/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_deviceModel(id):

    deviceModels = DeviceModel.query.get_or_404(id)
    devicePorts = DevicePorts.query.filter(DevicePorts.model_id == deviceModels.id).all()

    for port in devicePorts:
        ip = IpResourceManage.query.filter(IpResourceManage.ip == port.ip).first()
        ip.status = 0
        db.session.add(ip)

    db.session.query(DevicePorts).filter(DevicePorts.model_id == deviceModels.id).delete()
    db.session.delete(deviceModels)
    db.session.commit()

    return redirect(url_for('main.show_deviceModels'))


########################################################################

@main.route('/show-device.deviceAssets/<int:id>', methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ASSET_LOOK)
def show_deviceAssets(id):
    deviceAssets = Asset.query.filter(Asset.classType_id == id).all()
    print deviceAssets
    return render_template('show_deviceAssets.html', deviceAssets=deviceAssets, id=id)


@main.route('/create-device.deviceAsset', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ASSET_EDIT)
def create_deviceAsset():
    form = EditAssetForm(None)
    if form.validate_on_submit():
        deviceAsset = Asset()
        deviceAsset.classType_id = form.classType_id.data
        deviceAsset.an = form.an.data
        deviceAsset.sn = form.sn.data
        deviceAsset.onstatus = form.onstatus.data
        deviceAsset.dateofmanufacture = form.dateofmanufacture.data
        deviceAsset.manufacturer = form.manufacturer.data
        deviceAsset.brand = form.brand.data
        deviceAsset.model = form.model.data
        deviceAsset.usedept = form.usedept.data
        deviceAsset.usestaff = form.usestaff.data
        deviceAsset.mainuses = form.mainuses.data
        deviceAsset.managedept = form.managedept.data
        deviceAsset.managestaff = form.managestaff.data
        deviceAsset.koriyasustarttime = form.koriyasustarttime.data
        deviceAsset.koriyasuendtime = form.koriyasuendtime.data
        deviceAsset.equipprice = form.equipprice.data
        deviceAsset.remarks = form.remarks.data

        db.session.add(deviceAsset)
        db.session.commit()
        flash(u'设备添加完成')
        return redirect(url_for('main.show_deviceAssets',id=deviceAsset.classType_id))

    return render_template('create_deviceAsset.html', form=form)

@main.route('/edit-device.deviceAsset/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ASSET_EDIT)
def edit_deviceAsset(id):
    deviceAsset = Asset.query.get_or_404(id)
    form = EditAssetForm(deviceAsset)
    if form.validate_on_submit():
        deviceAsset.classType_id = form.classType_id.data
        deviceAsset.an = form.an.data
        deviceAsset.sn = form.sn.data
        deviceAsset.onstatus = form.onstatus.data
        deviceAsset.dateofmanufacture = form.dateofmanufacture.data
        deviceAsset.manufacturer = form.manufacturer.data
        deviceAsset.brand = form.brand.data
        deviceAsset.model = form.model.data
        deviceAsset.usedept = form.usedept.data
        deviceAsset.usestaff = form.usestaff.data
        deviceAsset.mainuses = form.mainuses.data
        deviceAsset.managedept = form.managedept.data
        deviceAsset.managestaff = form.managestaff.data
        deviceAsset.koriyasustarttime = form.koriyasustarttime.data
        deviceAsset.koriyasuendtime = form.koriyasuendtime.data
        deviceAsset.equipprice = form.equipprice.data
        deviceAsset.remarks = form.remarks.data
        db.session.add(deviceAsset)
        db.session.commit()
        flash(u'设备修改完成')
        return redirect(url_for('main.show_deviceAssets', id=deviceAsset.classType_id))

    form.classType_id.data = deviceAsset.classType_id
    form.an.data = deviceAsset.an
    form.sn.data = deviceAsset.sn
    form.onstatus.data = deviceAsset.onstatus
    form.dateofmanufacture.data = deviceAsset.dateofmanufacture
    form.manufacturer.data = deviceAsset.manufacturer
    form.brand.data = deviceAsset.brand
    form.model.data = deviceAsset.model
    form.usedept.data = deviceAsset.usedept
    form.usestaff.data = deviceAsset.usestaff
    form.mainuses.data = deviceAsset.mainuses
    form.managedept.data = deviceAsset.managedept
    form.managestaff.data = deviceAsset.managestaff
    form.koriyasustarttime.data = deviceAsset.koriyasustarttime
    form.koriyasuendtime.data = deviceAsset.koriyasuendtime
    form.equipprice.data = deviceAsset.equipprice
    form.remarks.data = deviceAsset.remarks

    return render_template('edit_deviceAsset.html', form=form, deviceAsset=deviceAsset)


@main.route('/delete-device.deviceAsset/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_deviceAsset(id):
    deviceAsset = Asset.query.get_or_404(id)
    db.session.delete(deviceAsset)
    flash(u'内存: {0} 已删除!'.format(deviceAsset.id))
    return redirect(url_for('main.show_deviceAssets', id=id))


#########################################################################


@main.route('/create-device.device', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_device():
    form = EditDeviceForm()
    if form.validate_on_submit():
        device = Device()
        device.asset_id = form.asset_id.data
        device.classType_id = form.classType_id.data
        device.rack_id = form.rack_id.data
        device.hostname = form.hostname.data
        device.is_virtualization = form.is_virtualization.data
        device.os = form.os.data
        device.cpumodel = form.cpumodel.data
        device.cpucount = form.cpucount.data
        device.memsize = form.memsize.data
        device.disksize = form.disksize.data
        device.useracksize = form.rackusesize.data
        device.use = form.use.data
        device.business = form.business.data
        device.powerstatus = form.powerstatus.data
        device.remarks = form.remarks.data

        db.session.add(device)
        db.session.commit()
        flash(u'设备添加完成')

        return redirect(url_for('main.show_devices',id=device.classType_id))

    return render_template('create_device.html', form=form)


@main.route('/edit-device.device/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_device(id):
    device = Device.query.get_or_404(id)
    form = EditDeviceForm()
    if form.validate_on_submit():
        device.asset_id = form.asset_id.data
        device.classType_id = form.classType_id.data
        device.rack_id = form.rack_id.data
        device.hostname = form.hostname.data
        device.is_virtualization = form.is_virtualization.data
        device.os = form.os.data
        device.cpumodel = form.cpumodel.data
        device.cpucount = form.cpucount.data
        device.memsize = form.memsize.data
        device.disksize = form.disksize.data
        device.useracksize = form.rackusesize.data
        device.use = form.use.data
        device.business = form.business.data
        device.powerstatus = form.powerstatus.data
        device.remarks = form.remarks.data

        db.session.add(device)
        db.session.commit()
        flash(u'设备添加完成')

        return redirect(url_for('main.show_devices', id=device.classType_id))

    form.asset_id.data = device.asset_id
    form.classType_id.data = device.classType_id
    form.rack_id.data = device.rack_id
    form.hostname.data = device.hostname
    form.is_virtualization.data = device.is_virtualization
    form.os.data = device.os
    form.cpumodel.data = device.cpumodel
    form.cpucount.data = device.cpucount
    form.memsize.data = device.memsize
    form.disksize.data = device.disksize
    form.use.data = device.use
    form.rackusesize.data = device.useracksize
    form.business.data = device.business
    form.powerstatus.data = device.powerstatus
    form.remarks.data = device.remarks

    return render_template('edit_device.html', form=form, device=device)


@main.route('/show-device.devices/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devices(id):
    # page = request.args.get('page', 1, type=int)
    # pagination = Device.query.order_by(Device.powerstatus.desc()).paginate(
    #    page=page, per_page=20, error_out=False
    # )

    # items = pagination.items
    # return render_template('show_devices1.html', items=items, endpoint='main.show_devices', pagination=pagination)


    if id != 0:
        devices = Device.query.filter(Device.classType_id == id).all()
    else:
        devices = Device.query.all()

    return render_template('show_devices.html', devices=devices)


@main.route('/delete-device.devices/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def delete_device(id):
    device = Device.query.get_or_404(id)

    deviceModel = db.session.query(DeviceModel).filter(DeviceModel.device_id == device.id).all()
    print deviceModel
    if deviceModel:
        for model in deviceModel:
            db.session.query(DevicePorts).filter(DevicePorts.model_id == model.id).delete()

    db.session.query(DeviceModel).filter(DeviceModel.device_id == device.id).delete()
    db.session.query(DeviceDisks).filter(DeviceDisks.device_id == device.id).delete()
    db.session.query(DeviceMemorys).filter(DeviceMemorys.device_id == device.id).delete()
    db.session.query(DevicePower).filter(DevicePower.device_id == device.id).delete()

    db.session.delete(device)
    db.session.commit()
    flash(u'设备: {0} 已删除!'.format(device.hostname))
    return redirect(url_for('main.show_devices', id=device.classType_id))


######################################################################

@main.route('/show-device.networks/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_deviceNetworks(id):
    if id != 0:
        deviceNetworks = DeviceNetwork.query.filter(DeviceNetwork.classType_id == id).all()
    else:
        deviceNetworks = DeviceNetwork.query.all()

    return render_template('show_deviceNetworks.html', deviceNetworks=deviceNetworks)


@main.route('/create-device.network', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_deviceNetwork():
    form = EditDeviceNetworkForm()
    if form.validate_on_submit():
        deviceNetwork = DeviceNetwork()

        deviceNetwork.classType_id = form.classType_id.data
        deviceNetwork.asset_id = form.asset_id.data
        deviceNetwork.rack_id = form.rack_id.data
        deviceNetwork.firmversion = form.firmversion.data
        deviceNetwork.enginecount = form.enginecount.data
        deviceNetwork.powercount = form.powercount.data
        deviceNetwork.powertype = form.powertype.data
        deviceNetwork.fancount = form.fancount.data

        try:
            db.session.add(deviceNetwork)
            db.session.commit()
            flash(u'网络设备: {0} 添加成功!'.format(deviceNetwork.id))
        except:
            db.session.rollback()
            flash(u'网络设备: {0} 添加失败!'.format(deviceNetwork.id))

        return redirect(url_for('main.show_deviceNetworks',id=deviceNetwork.classType_id))

    return render_template('create_deviceNetwork.html', form=form)


@main.route('/edit-device.network/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_deviceNetwork(id):
    deviceNetwork = DeviceNetwork.query.get_or_404(id)
    form = EditDeviceNetworkForm()
    if form.validate_on_submit():

        deviceNetwork.classType_id = form.classType_id.data
        deviceNetwork.asset_id = form.asset_id.data
        deviceNetwork.rack_id = form.rack_id.data
        deviceNetwork.firmversion = form.firmversion.data
        deviceNetwork.enginecount = form.enginecount.data
        deviceNetwork.powercount = form.powercount.data
        deviceNetwork.powertype = form.powertype.data
        deviceNetwork.fancount = form.fancount.data

        try:
            db.session.add(deviceNetwork)
            db.session.commit()
            flash(u'网络设备: {0} 修改成功!'.format(deviceNetwork.id))
        except:
            db.session.rollback()
            flash(u'网络设备: {0} 修改失败!'.format(deviceNetwork.id))

        return redirect(url_for('main.show_deviceNetworks',id=deviceNetwork.classType_id))

    form.classType_id.data = deviceNetwork.classType_id
    form.asset_id.data = deviceNetwork.asset_id
    form.rack_id.data = deviceNetwork.rack_id
    form.firmversion.data = deviceNetwork.firmversion
    form.enginecount.data = deviceNetwork.enginecount
    form.powercount.data = deviceNetwork.powercount
    form.powertype.data = deviceNetwork.powertype
    form.fancount.data = deviceNetwork.fancount

    return render_template('edit_deviceNetwork.html', form=form, deviceNetwork=deviceNetwork)


@main.route('/delete-device.network/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_deviceNetwork(id):
    deviceNetwork = DeviceNetwork.query.get_or_404(id)
    try:
        db.session.delete(deviceNetwork)
        db.session.commit()
        flash(u'网络设备: {0} 删除成功!'.format(deviceNetwork.id))
    except:
        db.session.rollback()
        flash(u'网络设备: {0} 删除失败!'.format(deviceNetwork.id))

    return redirect(url_for('main.show_deviceNetworks',id=deviceNetwork.classType_id))

######################################################################


@main.route('/show-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_virtmachine(id):
    if id != 0:
        virtMachine = DevicePools.query.get_or_404(id).devices.all()
    else:
        virtMachine = VirtMachine.query.all()
    return render_template('show_virtmachine.html', virtMachine=virtMachine)


@main.route('/create-device.virtmachine', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_virtmachine():
    form = EditVritMachineForm()
    if form.validate_on_submit():
        virtMachine = VirtMachine()
        virtMachine.deviceType = form.deviceType.data
        virtMachine.onstatus = form.onstatus.data
        virtMachine.usedept = form.usedept.data
        virtMachine.usestaff = form.usestaff.data
        virtMachine.mainuses = form.mainuses.data
        virtMachine.managedept = form.managedept.data
        virtMachine.managestaff = form.managestaff.data
        virtMachine.pool = DevicePools.query.get(form.pool.data)
        virtMachine.hostname = form.hostname.data
        virtMachine.os = form.os.data
        virtMachine.cpumodel = form.cpumodel.data
        virtMachine.cpucount = form.cpucount.data
        virtMachine.memsize = form.memsize.data
        virtMachine.disksize = form.disksize.data
        virtMachine.business = form.business.data
        virtMachine.powerstatus = form.powerstatus.data
        virtMachine.remarks = form.remarks.data

        try:
            db.session.add(virtMachine)
            db.session.commit()
            flash(u'虚拟机添加完成!')
        except:
            db.session.rollback()
            flash(u'虚拟机添加失败!')

        return redirect(url_for('main.show_virtmachine', id=virtMachine.deviceType))

    return render_template('create_virtmachine.html', form=form)


@main.route('/edit-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_virtmachine(id):
    virtMachine = VirtMachine.query.get_or_404(id)
    form = EditVritMachineForm()
    if form.validate_on_submit():
        virtMachine.deviceType = form.deviceType.data
        virtMachine.onstatus = form.onstatus.data
        virtMachine.usedept = form.usedept.data
        virtMachine.usestaff = form.usestaff.data
        virtMachine.mainuses = form.mainuses.data
        virtMachine.managedept = form.managedept.data
        virtMachine.managestaff = form.managestaff.data
        virtMachine.device_id = form.device_id.data
        virtMachine.pool = DevicePools.query.get(form.pool.data)
        virtMachine.hostname = form.hostname.data
        virtMachine.os = form.os.data
        virtMachine.cpumodel = form.cpumodel.data
        virtMachine.cpucount = form.cpucount.data
        virtMachine.memsize = form.memsize.data
        virtMachine.disksize = form.disksize.data
        virtMachine.business = form.business.data
        virtMachine.powerstatus = form.powerstatus.data
        virtMachine.remarks = form.remarks.data

        try:
            db.session.add(virtMachine)
            db.session.commit()
            flash(u'设备添加完成!')
        except:
            db.session.rollback()
            flash(u'设备添加失败!')

        return redirect(url_for('main.show_virtmachine', id=virtMachine.deviceType))

    form.deviceType.data = virtMachine.deviceType
    form.onstatus.data = virtMachine.onstatus
    form.usedept.data = virtMachine.usedept
    form.usestaff.data = virtMachine.usestaff
    form.mainuses.data = virtMachine.mainuses
    form.managedept.data = virtMachine.managedept
    form.managestaff.data = virtMachine.managestaff
    form.device_id.data = virtMachine.device_id
    form.pool.data = virtMachine.pool
    form.hostname.data = virtMachine.hostname
    form.os.data = virtMachine.os
    form.cpumodel.data = virtMachine.cpumodel
    form.cpucount.data = virtMachine.cpucount
    form.memsize.data = virtMachine.memsize
    form.disksize.data = virtMachine.disksize
    form.business.data = virtMachine.business
    form.powerstatus.data = virtMachine.powerstatus
    form.remarks.data = virtMachine.remarks

    return render_template('edit_virtmachine.html', form=form, virtMachine=virtMachine)


@main.route('/delete-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_virtmachine(id):
    virtMachine = VirtMachine.query.get_or_404(id)

    try:
        db.session.delete(virtMachine)
        flash(u'虚拟机: {0} 已删除!'.format(virtMachine.hostname))
    except:
        db.session.rollback()
        flash(u'虚拟机: {0} 删除失败!'.format(virtMachine.hostname))

    return redirect(url_for('main.show_virtmachine', id=virtMachine.deviceType))


@main.route('/show-racks', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.RACK_LOOK)
def show_racks():
    # page = request.args.get('page', 1, type=int)
    # pagination = Rack.query.order_by(Rack.name.desc()).paginate(
    #    page=page, per_page=20, error_out=False
    # )

    # items = pagination.items
    # return render_template('show_racks.html', items=items, endpoint='main.show_racks', pagination=pagination)

    racks = Rack.query.all()
    return render_template('show_racks.html', racks=racks)


@main.route('/create-rack', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.RACK_EDIT)
def create_rack():
    form = EditRackForm(rack=None)
    if form.validate_on_submit():
        rack = Rack()
        rack.name = form.name.data
        rack.staff = form.staff.data
        rack.idc = Idc.query.get(form.idc.data)
        rack.site = form.site.data
        rack.racktype = form.racktype.data
        rack.usesize = form.usesize.data
        rack.remainsize = form.remainsize.data
        rack.electrictype = form.electrictype.data
        rack.electricno = form.electricno.data
        rack.leftelectric = form.leftelectric.data
        rack.renttime = form.renttime.data
        rack.expiretime = form.expiretime.data
        rack.nextpaytime = form.nextpaytime.data
        rack.money = form.money.data
        rack.remarks = form.remarks.data
        try:
            db.session.add(rack)
            db.session.commit()
            flash(u'机柜: {0} 添加完成!'.format(form.name.data))
        except:
            db.session.rollback()
            flash(u'机柜: {0} 添加失败!'.format(form.name.data))

        return redirect(url_for('main.show_racks'))

    return render_template('create_rack.html', form=form)


@main.route('/edit-rack/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.RACK_EDIT)
def edit_rack(id):
    rack = Rack.query.get_or_404(id)
    form = EditRackForm(rack)
    if form.validate_on_submit():
        rack.name = form.name.data
        rack.staff = form.staff.data
        rack.idc = Idc.query.get(form.idc.data)
        rack.site = form.site.data
        rack.racktype = form.racktype.data
        rack.usesize = form.usesize.data
        rack.remainsize = form.remainsize.data
        rack.electrictype = form.electrictype.data
        rack.electricno = form.electricno.data
        rack.electriccapacity = form.electriccapacity.data
        rack.leftelectric = form.leftelectric.data
        rack.renttime = form.renttime.data
        rack.expiretime = form.expiretime.data
        rack.nextpaytime = form.nextpaytime.data
        rack.money = form.money.data
        rack.remarks = form.remarks.data

        try:
            db.session.add(rack)
            db.session.commit()
            flash(u'机柜:{0} 修改完成!'.format(rack.name))
        except:
            db.session.rollback()
            flash(u'机柜:{0} 修改失败!'.format(rack.name))

        return redirect(url_for('main.show_racks'))

    form.name.data = rack.name
    form.staff.data = rack.staff
    form.idc.data = rack.idc
    form.site.data = rack.site
    form.racktype.data = rack.racktype
    form.usesize.data = rack.usesize
    form.remainsize.data = rack.remainsize
    form.electrictype.data = rack.electrictype
    form.electricno.data = rack.electricno
    form.electriccapacity.data = rack.electriccapacity
    form.leftelectric.data = rack.leftelectric
    form.renttime.data = rack.renttime
    form.expiretime.data = rack.expiretime
    form.nextpaytime.data = rack.nextpaytime
    form.money.data = rack.money
    form.remarks.data = rack.remarks
    return render_template('edit_rack.html', form=form, rack=rack)


@main.route('/delete-rack/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.RACK_DEL)
def delete_rack(id):
    rack = Rack.query.get_or_404(id)
    try:
        devices = db.session.query(Device).filter(Device.rack_id == rack.id).all()
        for device in devices:
            db.session.query(Asset).filter(device.asset_id == Asset.id).delete()

        networks = db.session.query(DeviceNetwork).filter(DeviceNetwork.rack_id == rack.id).all()
        for network in networks:
            db.session.query(Asset).filter(network.asset_id == Asset.id).delete()


        db.session.delete(rack)
        db.session.commit()
        flash(u'机柜: {0} 删除成功!'.format(rack.name))
    except:
        db.session.rollback()
        flash(u'机柜: {0} 删除失败!'.format(rack.name))


    return redirect(url_for('main.show_racks'))


########################################################################

@main.route('/show-idcs', methods=['GET'])
@login_required
@permission_required(Permission.IDC_LOOK)
def show_idcs():
    idcs = Idc.query.all()
    return render_template('show_idcs.html', idcs=idcs)


@main.route('/create-idc', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.IDC_EDIT)
def create_idc():
    form = EditIdcForm(idc=None)
    if form.validate_on_submit():
        idc = Idc()
        idc.name = form.name.data
        idc.ispid = form.ispid.data
        idc.city = form.city.data
        idc.address = form.address.data
        idc.contactname = form.contactname.data
        idc.contactphone = form.contactphone.data
        idc.nettype = form.nettype.data
        idc.netout = form.netout.data
        idc.adnature = form.adnature.data
        idc.remarks = form.remarks.data

        try:
            db.session.add(idc)
            db.session.commit()
            flash(u'机房:{0} 添加完成!'.format(form.name.data))
        except:
            db.session.rollback()
            flash(u'机房:{0} 添加失败!'.format(form.name.data))

        return redirect(url_for('main.show_idcs'))
    return render_template('create_idc.html', form=form)


@main.route('/edit-idc/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.IDC_EDIT)
def edit_idc(id):
    idc = Idc.query.get_or_404(id)
    form = EditIdcForm(idc=idc)

    if form.validate_on_submit():
        idc.name = form.name.data
        idc.ispid = form.ispid.data
        idc.city = form.city.data
        idc.address = form.address.data
        idc.contactname = form.contactname.data
        idc.contactphone = form.contactphone.data
        idc.nettype = form.nettype.data
        idc.netout = form.netout.data
        idc.adnature = form.adnature.data
        idc.remarks = form.remarks.data

        try:
            db.session.add(idc)
            db.session.commit()
            flash(u'机房:{0} 修改完成'.format(idc.name))
        except:
            db.session.rollback()
            flash(u'机房:{0} 修改失败'.format(idc.name))


        return redirect(url_for('main.show_idcs'))

    form.name.data = idc.name
    form.ispid.data = idc.ispid
    form.city.data = idc.city
    form.address.data = idc.address
    form.contactname.data = idc.contactname
    form.contactphone.data = idc.contactphone
    form.nettype.data = idc.nettype
    form.netout.data = idc.netout
    form.adnature.data = idc.adnature
    form.remarks.data = idc.remarks
    return render_template('edit_idc.html', form=form, idc=idc)


@main.route('/delete-idc/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.IDC_DEL)
def delete_idc(id):
    idc = Idc.query.get_or_404(id)

    try:
        db.session.query(Rack).filter(Rack.idc_id == idc.id).delete()
        db.session.delete(idc)
        flash(u'机房: {0} 已删除!'.format(idc.name))
    except:
        db.session.rollback()
        flash(u'机房: {0} 删除失败!'.format(idc.name))


    return redirect(url_for('main.show_idcs'))


########################################################################


@main.route('/show-ip.manage/<int:id>', methods=['GET'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_IpResourceManage(id):
    ipResourceManage = IpResourceManage.query.filter(IpResourceManage.ipPool_id == id)
    return render_template('show_ipResourceManage.html', ipResourceManage=ipResourceManage)



@main.route('/edit-ip.manage/<int:id>', methods=['GET'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_IpResourceManage(id):
    ipResourceManage = IpResourceManage.query.get(id)
    form = EditIpResourceManageForm()
    if form.validate_on_submit():

        ipResourceManage.status = form.status.data
        ipResourceManage.remarks = form.remarks.data
        db.session.add(ipResourceManage)
        db.session.commit()

    form.ipPool_id.data = ipResourceManage.ipPool_id
    form.ip.data = ipResourceManage.ip
    form.status.data = ipResourceManage.status
    form.devicePort_id = ipResourceManage.devicePort_id
    form.remarks.data = ipResourceManage.remarks

    return render_template('show_ipResourceManage.html', ipResourceManage=ipResourceManage)

########################################################################


@main.route('/show-ip.pools', methods=['GET'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_IpResourcePools():
    ipResourcePools = IpResourcePools.query.all()
    return render_template('show_ipResourcePools.html', ipResourcePools=ipResourcePools)


@main.route('/create-ip.pools', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_IpResourcePools():
    form = EditIpResourcePoolsForm()
    if form.validate_on_submit():
        ipResourcePools = IpResourcePools()
        ipResourcePools.idc_id = form.idc_id.data
        ipResourcePools.type = form.type.data
        ipResourcePools.netmask = form.netmask.data
        ipResourcePools.gateway = form.gateway.data
        ipResourcePools.vlan = form.vlan.data
        ipResourcePools.remarks = form.remarks.data
        ipResourcePools.range = form.range.data

        db.session.add(ipResourcePools)
        db.session.commit()
        flash(u'创建IP资源池:{0}成功!'.format(ipResourcePools.range))
        return redirect(url_for('main.show_IpResourcePools'))
    return render_template('create_ipResourcePools.html', form=form)


@main.route('/edit-ip.pools/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_IpResourcePools(id):
    ipResourcePools = IpResourcePools.query.get(id)
    form = EditIpResourcePoolsForm()
    if form.validate_on_submit():
        ipResourcePools.idc_id = form.idc_id.data
        ipResourcePools.type = form.type.data
        ipResourcePools.netmask = form.netmask.data
        ipResourcePools.gateway = form.gateway.data
        ipResourcePools.vlan = form.vlan.data
        ipResourcePools.remarks = form.remarks.data
        ipResourcePools.range = form.range.data

        db.session.add(ipResourcePools)
        db.session.commit()
        flash(u'修改IP资源池:{0}成功!'.format(ipResourcePools.range))
        return redirect(url_for('main.show_IpResourcePools'))

    form.idc_id.data = ipResourcePools.idc_id
    form.type.data = ipResourcePools.type
    form.netmask.data = ipResourcePools.netmask
    form.gateway.data = ipResourcePools.gateway
    form.vlan.data = ipResourcePools.vlan
    form.remarks.data = ipResourcePools.remarks
    form.range.data = ipResourcePools.range

    return render_template('edit_ipResourcePools.html', form=form, ipResourcePools=ipResourcePools)



@main.route('/delete-ip.pools/<int:id>', methods=['GET'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_IpResourcePools(id):
    ipResourcePools = IpResourcePools.query.get(id)
    db.session.query(IpResourceManage).filter(IpResourceManage.ipPool_id == ipResourcePools.id).delete()
    db.session.delete(ipResourcePools)
    db.session.commit()
    flash(u'删除IP资源池:{0}成功!'.format(ipResourcePools.range))
    return redirect(url_for('main.show_IpResourcePools'))



@main.route('/xxx')
def xxx():
    return render_template('xxx.html')


# @main.route('/test', methods=['GET', 'POST'])
# @login_required
# def test():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         current_user.name = form.name.data
#         current_user.username = form.username.data
#         current_user.qq = form.qq.data
#         current_user.phone = form.phone.data
#         current_user.location = form.location.data
#         current_user.about_me = form.about_me.data
#         db.session.add(current_user)
#         flash(u'提交成功!')
#         return redirect(url_for('main.test',username=current_user.username))
#
#     form.name.data = current_user.name
#     form.username.data = current_user.username
#     form.location.data = current_user.location
#     form.about_me.data = current_user.about_me
#     form.qq.data = current_user.qq
#     form.phone.data = current_user.phone
#     return render_template('test.html',form=form)
#


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data

        try:
            db.session.add(user)
            db.session.commit()
            flash(u'修改资料成功!')
        except:
            db.session.rollback()
            flash(u'修改资料失败!')


        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    return render_template('edit_profile.html', form=form, user=user)


# print url_for('index')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For Administrators!'


@main.route('/moderator')
@login_required
@permission_required(Permission.ADMINISTER)
def for_moderators_only():
    return 'For moderators!'


if __name__ == '__main__':
    manager.run()
