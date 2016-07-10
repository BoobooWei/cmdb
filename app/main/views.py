# coding:utf8

from flask import render_template, redirect, url_for, flash, current_app, abort, request, make_response
from flask.ext.login import login_required, current_user
from ..decorators import admin_required, permission_required
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, EditAssetForm, EditDeviceForm, EditIdcForm, EditRackForm, EditDeviceTypeForm
from .forms import EditDevicePortForm, EditDeviceMemoryForm, EditDevicePoolsForm, EditDevicePowermanageForm, EditVritMachineForm
from .. import db
from ..models import User, Role, Permission, DevicePorts, DeviceMemorys, VirtMachine, Idc, Device, DeviceType, Rack, Logger
from ..models import DevicePools, DevicePowerManage
from ..email import send_email


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, endpoint='main.user', pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    logs = Logger.query.order_by(Logger.logtime.desc()).all()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.position = form.position.data
        current_user.qq = form.qq.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        # action  [ 1: add , 2: edit, 3: del ]
        log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users',
                     logobj_id=current_user.id)
        db.session.add(log)
        db.session.commit()
        flash(u'提交成功!')
        return redirect(url_for('main.edit_profile', username=current_user.username, logs=logs))

    form.name.data = current_user.name
    form.username.data = current_user.username
    form.position.data = current_user.position
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.qq.data = current_user.qq
    form.phone.data = current_user.phone
    return render_template('edit_profile.html', form=form, username=current_user.username, logs=logs)


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@main.route('/create-device.type', methods=['GET', 'POST'])
@login_required
def create_deviceType():
    form = EditDeviceTypeForm(deviceType=None)
    if form.validate_on_submit():
        deviceType = DeviceType(name=form.name.data,
                            remarks=form.remarks.data)
        db.session.add(deviceType)
        db.session.commit()
        flash(u'创建设备类型:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.index'))
    return render_template('test.html', form=form)



@main.route('/edit-device.type/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_deviceType(id):
    deviceType = DeviceType.query.get_or_404(id)
    form = EditDeviceTypeForm(deviceType=deviceType)
    if form.validate_on_submit():
        deviceType.name=form.name.data
        deviceType.remarks=form.remarks.data
        db.session.add(deviceType)
        db.session.commit()
        flash(u'编辑设备类型:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.index'))

    form.name.data = deviceType.name
    form.remarks.data = deviceType.remarks
    return render_template('test.html', form=form)



@main.route('/show-device.type', methods=['GET', 'POST'])
@login_required
def show_deviceType(id):
    deviceType = DeviceType.query.all()
    return render_template('test.html', deviceType=deviceType)


@main.route('/show-device.ports', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePorts():
    devicePorts = DevicePorts.query.all()
    return render_template('test.html', devicePorts=devicePorts)



@main.route('/create-device.ports', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePorts():
    form = EditDevicePortForm()
    if form.validate_on_submit():
        devicePorts = DevicePorts(name=form.name.data,
                                    ip=form.ip.data,
                                    mac=form.mac.data,
                                    portType=form.portType.data,
                                    device=Device.query.get(form.device.data),
                                    remarks=form.remarks.data)
        db.session.add(devicePorts)
        db.session.commit()
        flash(u'创建设备端口:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.index'))
    return render_template('test.html', form=form)


@main.route('/edit-device.ports/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_devicePorts(id):
    devicePorts = DevicePorts.query.get_or_404(id)
    form = EditDevicePortForm()
    if form.validate_on_submit():
        devicePorts.name=form.name.data,
        devicePorts.ip=form.ip.data,
        devicePorts.mac=form.mac.data,
        devicePorts.portType=form.portType.data,
        devicePorts.device=Device.query.get(form.device.data)
        devicePorts.remarks=form.remarks.data
        db.session.add(devicePorts)
        db.session.commit()
        flash(u'修改设备端口:{0}成功!'.format(devicePorts.name))
        return redirect(url_for('main.index'))

    form.name.data = devicePorts.name
    form.ip.data = devicePorts.ip
    form.mac.data = devicePorts.mac
    form.portType.data = devicePorts.portType
    form.device.data = devicePorts.device
    form.remarks.data = devicePorts.remarks
    return render_template('test.html', form=form)


@main.route('/delete-device.ports/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_devicePorts(id):
    devicePorts = DevicePorts.query.get_or_404(id)
    db.session.delete(devicePorts)
    flash(u'删除设备端口:{0}成功!'.format(devicePorts.name))
    return redirect(url_for('main.show_devicePorts'))


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
        deviceMemorys = DeviceMemorys(slot_id=form.slot_id.data,
                                    SN=form.SN.data,
                                    Size=form.Size.data,
                                    device=Device.query.get(form.device.data),
                                    remarks=form.remarks.data)
        db.session.add(deviceMemorys)
        flash(u'创建设备内存:{0}成功!'.format(form.SN.data))
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('test.html', form=form)



@main.route('/edit-device.memorys/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_deviceMemorys(id):
    deviceMemorys = DeviceMemorys.query.get_or_404(id)
    form = EditDeviceMemoryForm()
    if form.validate_on_submit():

        deviceMemorys.slot_id=form.slot_id.data
        deviceMemorys.SN=form.SN.data
        deviceMemorys.Size=form.Size.data
        deviceMemorys.device=Device.query.get(form.device.data)
        deviceMemorys.remarks=form.remarks.data

        db.session.add(deviceMemorys)
        db.session.commit()
        flash(u'修改设备内存:{0}成功!'.format(deviceMemorys.SN))
        return redirect(url_for('main.index'))

    form.slot_id.data = deviceMemorys.slot_id
    form.SN.data = deviceMemorys.SN
    form.Size.data = deviceMemorys.Size
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
    return redirect(url_for('main.index'))

#######################################################################


@main.route('/show-device.pools', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePools():
    devicePools = DevicePools.query.all()
    return render_template('test.html', deviceMemorys=devicePools)



@main.route('/create-device.pools', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePools():
    form = EditDevicePoolsForm()
    if form.validate_on_submit():
        devicePools = DevicePools(name=form.name.data,
                                  remarks=form.remarks.data)
        db.session.add(devicePools)
        db.session.commit()
        flash(u'创建资源池:{0}成功!'.format(form.name.data))
        return redirect(url_for('main.index'))
    return render_template('test.html', form=form)



@main.route('/edit-device.pools/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_devicePools(id):
    devicePools = DevicePools.query.get_or_404(id)
    form = EditDevicePoolsForm()
    if form.validate_on_submit():

        devicePools.name = form.name.data
        devicePools.remarks=form.remarks.data

        db.session.add(devicePools)
        db.session.commit()
        flash(u'修改资源池:{0}成功!'.format(devicePools.name))
        return redirect(url_for('main.index'))

    form.name.data = devicePools.name
    form.remarks.data = devicePools.remarks
    return render_template('test.html', form=form)



@main.route('/delete-device.pools/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_devicePools(id):
    devicePools = DevicePools.query.get_or_404(id)
    db.session.delete(devicePools)
    flash(u'资源池: {0} 已删除!'.format(devicePools.id))
    return redirect(url_for('main.index'))

########################################################################

@main.route('/show-device.powermanage', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devicePowermanage():
    devicePowermanage = DevicePowerManage.query.all()
    return render_template('test.html', devicePowermanage=devicePowermanage)


@main.route('/create-device.powermanage', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_devicePowermanage():
    form = EditDevicePowermanageForm()
    if form.validate_on_submit():
        devicePowermanage = DevicePowerManage(powermanageType=form.powermanageType.data,
                                              powermanageEnable=form.powermanageEnable.data,
                                              powermanageIp=form.powermanageIp.data,
                                              powermanageUser=form.powermanageUser.data,
                                              powermanagePassword=form.powermanagePassword.data,
                                              powermanageId=form.powermanageId.data,
                                              remarks=form.remarks.data)
        db.session.add(devicePowermanage)
        db.session.commit()
        flash(u'创建电源管理:{0}成功!'.format(devicePowermanage.powermanageIp))
        return redirect(url_for('main.index'))
    return render_template('test.html', form=form)


@main.route('/edit-device.powermanage/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_devicePowermanage(id):
    devicePowermanage = DevicePowerManage.query.get_or_404(id)
    form = EditDevicePowermanageForm()
    if form.validate_on_submit():
        devicePowermanage.powermanageType=form.powermanageType.data,
        devicePowermanage.powermanageEnable=form.powermanageEnable.data,
        devicePowermanage.powermanageIp=form.powermanageIp.data,
        devicePowermanage.powermanageUser=form.powermanageUser.data,
        devicePowermanage.powermanagePassword=form.powermanagePassword.data,
        devicePowermanage.powermanageId=form.powermanageId.data,
        devicePowermanage.remarks=form.remarks.data

        db.session.add(devicePowermanage)
        db.session.commit()
        flash(u'修改电源管理:{0}成功!'.format(devicePowermanage.powermanageIp))
        return redirect(url_for('main.index'))

    form.powermanageType.data = devicePowermanage.powermanageType
    form.powermanageEnable.data = devicePowermanage.powermanageEnable
    form.powermanageIp.data = devicePowermanage.powermanageIp
    form.powermanageUser.data = devicePowermanage.powermanageUser
    form.powermanagePassword.data = devicePowermanage.powermanagePassword
    form.powermanageId.data = devicePowermanage.powermanageId
    form.remarks.data = devicePowermanage.remarks

    return render_template('test.html', form=form)


@main.route('/delete-device.powermanage/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_devicePowermanage(id):
    devicePowermanage = DevicePowerManage.query.get_or_404(id)
    db.session.delete(devicePowermanage)
    flash(u'电源管理: {0} 已删除!'.format(devicePowermanage.powermanageIp))
    return redirect(url_for('main.index'))


########################################################################

@main.route('/show-device.assets', methods=['GET', 'POST'])
@login_required
#@permission_required(Permission.ASSET_LOOK)
def show_assets():
    deviceAssets = Asset.query.all()
    return render_template('test.html', deviceAssets=deviceAssets)



@main.route('/create-device.asset', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ASSET_EDIT)
def create_asset():
    form = EditAssetForm()
    if form.validate_on_submit():
        asset = Asset(Devicetype = DeviceType.query.get(form.Devicetype.data),
                        an = form.an.data,
                        sn = form.sn.data,
                        onstatus = form.onstatus.data,
                        dateofmanufacture = form.dateofmanufacture.data,
                        manufacturer = form.manufacturer.data,
                        brand = form.brand.data,
                        model = form.model.data,
                        usedept = form.usedept.data,
                        usestarttime = form.usestarttime.data,
                        useendtime = form.useendtime.data,
                        mainuses = form.mainuses.data,
                        managedept = form.managedept.data,
                        managestaff = form.managestaff.data,
                        koriyasustarttime = form.koriyasustarttime.data,
                        koriyasuendtime = form.koriyasuendtime.data,
                        equipprice = form.equipprice.data,
                        os = form.os.data,
                        remarks = form.remarks.data)
        db.session.add(asset)
        db.session.commit()
        flash(u'设备添加完成')
        return redirect(url_for('main.index'))

    return render_template('create_asset.html', form=form)


@main.route('/edit-device.asset/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ASSET_EDIT)
def edit_asset(id):
    asset = Asset.query.get_or_404(id)
    form = EditAssetForm()
    if form.validate_on_submit():
        asset.DeviceType = DeviceType.query.get(form.DeviceType.data)
        asset.an = form.an.data
        asset.sn = form.sn.data
        asset.onstatus = form.onstatus.data
        asset.dateofmanufacture = form.dateofmanufacture.data
        asset.manufacturer = form.manufacturer.data
        asset.brand = form.brand.data
        asset.model = form.model.data
        asset.usedept = form.usedept.data
        asset.usestarttime = form.usestarttime.data
        asset.useendtime = form.useendtime.data
        asset.mainuses = form.mainuses.data
        asset.managedept = form.managedept.data
        asset.managestaff = form.managestaff.data
        asset.koriyasustarttime = form.koriyasustarttime.data
        asset.koriyasuendtime = form.koriyasuendtime.data
        asset.equipprice = form.equipprice.data
        asset.remarks = form.remarks.data
        db.session.add(asset)
        db.session.commit()
        flash(u'设备修改完成')
        return redirect(url_for('main.index'))

    form.DeviceType.data = asset.DeviceType
    form.an.data = asset.an
    form.sn.data = asset.sn
    form.onstatus.data = asset.onstatus
    form.dateofmanufacture.data = asset.dateofmanufacture
    form.manufacturer.data = asset.manufacturer
    form.brand.data = asset.brand
    form.model.data = asset.model
    form.usedept.data = asset.usedept
    form.usestarttime.data = asset.usestarttime
    form.useendtime.data = asset.useendtime
    form.mainuses.data = asset.mainuses
    form.managedept.data = asset.managedept
    form.managestaff.data = asset.managestaff
    form.koriyasustarttime.data = asset.koriyasustarttime
    form.koriyasuendtime.data = asset.koriyasuendtime
    form.equipprice.data = asset.equipprice
    form.remarks.data = asset.remarks

    return render_template('create_asset.html', form=form)


@main.route('/delete-device.asset/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_deviceAssets(id):
    deviceAssets = Asset.query.get_or_404(id)
    db.session.delete(deviceAssets)
    flash(u'内存: {0} 已删除!'.format(deviceAssets.id))
    return redirect(url_for('main.index'))


#########################################################################


@main.route('/create-device.device', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def create_device():
    form = EditDeviceForm()
    if form.validate_on_submit():

        device = Device(hostname = form.hostname.data,
                        rack = Rack.query.get(form.rack.data),

                        is_virtualization = form.is_virtualization.data,
                        cpumodel = form.cpumodel.data,
                        cpucount = form.cpucount.data,
                        memsize = form.memsize.data,
                        raidmodel = form.raidmodel.data,
                        # disks=form.disks.data,
                        os = form.os.data,
                        remarks = form.remarks.data)

        db.session.add(device)
        db.session.commit()
        flash(u'设备添加完成')


        return redirect(url_for('main.index'))

    return render_template('create_device.html', form=form)


@main.route('/show-device.devices', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devices():
    # page = request.args.get('page', 1, type=int)
    # pagination = Device.query.order_by(Device.powerstatus.desc()).paginate(
    #    page=page, per_page=20, error_out=False
    # )

    # items = pagination.items
    # return render_template('show_devices1.html', items=items, endpoint='main.show_devices', pagination=pagination)

    devices = Device.query.all()
    return render_template('show_devices.html', devices=devices)

######################################################################

@main.route('/show-device.virtmachine', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_virtmachine():
    virtMachine = VirtMachine.query.all()
    return render_template('show_devices.html', virtMachine=virtMachine)


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
        virtMachine.businss = form.businss.data
        virtMachine.powerstatus = form.powerstatus.data
        virtMachine.remarks = form.remarks.data

        db.session.add(virtMachine)
        db.session.commit()
        flash(u'设备添加完成')


        return redirect(url_for('main.index'))

    return render_template('test.html', form=form)


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
        virtMachine.pool = DevicePools.query.get(form.pool.data)
        virtMachine.hostname = form.hostname.data
        virtMachine.os = form.os.data
        virtMachine.cpumodel = form.cpumodel.data
        virtMachine.cpucount = form.cpucount.data
        virtMachine.memsize = form.memsize.data
        virtMachine.disksize = form.disksize.data
        virtMachine.businss = form.businss.data
        virtMachine.powerstatus = form.powerstatus.data
        virtMachine.remarks = form.remarks.data

        db.session.add(virtMachine)
        db.session.commit()
        flash(u'设备添加完成')
        return redirect(url_for('main.index'))

    form.deviceType.data = virtMachine.deviceType
    form.onstatus.data = virtMachine.onstatus
    form.usedept.data = virtMachine.usedept
    form.usestaff.data = virtMachine.usestaff
    form.mainuses.data = virtMachine.mainuses
    form.managedept.data = virtMachine.managedept
    form.managestaff.data = virtMachine.managestaff
    form.pool.data = virtMachine.pool
    form.hostname.data = virtMachine.hostname
    form.os.data = virtMachine.os
    form.cpumodel.data = virtMachine.cpumodel
    form.cpucount.data = virtMachine.cpucount
    form.memsize.data = virtMachine.memsize
    form.disksize.data = virtMachine.disksize
    form.businss.data = virtMachine.businss
    form.powerstatus.data = virtMachine.powerstatus
    form.remarks.data = virtMachine.remarks

    return render_template('test.html', form=form)


@main.route('/delete-device.virtmachine/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_DEL)
def delete_virtmachine(id):
    virtMachine = VirtMachine.query.get_or_404(id)
    db.session.delete(virtMachine)
    flash(u'虚拟机: {0} 已删除!'.format(virtMachine.hostname))
    return redirect(url_for('main.index'))


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
        rack = Rack(name=form.name.data,
                    staff=form.staff.data,
                    idcname=Idc.query.get(form.idcname.data),
                    site=form.site.data,
                    racktype=form.racktype.data,
                    usesize=form.usesize.data,
                    remainsize=form.remainsize.data,
                    electrictype=form.electrictype.data,
                    electricno=form.electricno.data,
                    leftelectric=form.leftelectric.data,
                    renttime=form.renttime.data,
                    expiretime=form.expiretime.data,
                    nextpaytime=form.nextpaytime.data,
                    money=form.money.data,
                    remarks=form.remarks.data)
        db.session.add(rack)
        db.session.commit()
        flash(u'机柜: {0} 添加完成'.format(form.name.data))
        return redirect(url_for('main.show_racks'))

    return render_template('create_rack.html', form=form)



@main.route('/edit-rack/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.RACK_EDIT)
def edit_rack(id):
    rack = Rack.query.get_or_404(id)
    form = EditRackForm(rack)
    if form.validate_on_submit():
        rack.name=form.name.data
        rack.staff=form.staff.data
        rack.idcname=Idc.query.get(form.idcname.data)
        rack.site=form.site.data
        rack.racktype=form.racktype.data
        rack.usesize=form.usesize.data
        rack.remainsize=form.remainsize.data
        rack.electrictype=form.electrictype.data
        rack.electricno=form.electricno.data
        rack.electriccapacity = form.electriccapacity.data
        rack.leftelectric=form.leftelectric.data
        rack.renttime=form.renttime.data
        rack.expiretime=form.expiretime.data
        rack.nextpaytime=form.nextpaytime.data
        rack.money=form.money.data
        rack.remarks=form.remarks.data
        db.session.add(rack)

        db.session.commit()
        flash(u'机柜:{0} 修改完成'.format(rack.name))
        return redirect(url_for('main.show_racks'))

    form.name.data = rack.name
    form.staff.data = rack.staff
    form.idcname.data = rack.idcname
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
#@permission_required(Permission.RACK_DEL)
def delete_rack(id):
    rack = Rack.query.get_or_404(id)
    db.session.delete(rack)
    flash(u'机柜: {0} 已删除!'.format(rack.name))
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
        idc = Idc(name=form.name.data,
                  ispid=form.ispid.data,
                  city=form.city.data,
                  address=form.address.data,
                  contactname=form.contactname.data,
                  contactphone=form.contactphone.data,
                  nettype=form.nettype.data,
                  netout=form.netout.data,
                  adnature=form.adnature.data,
                  remarks=form.remarks.data)
        db.session.add(idc)

        # log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users', logobj_id=current_user.id)
        # db.session.add(log)
        db.session.commit()
        flash(u'机房:{0} 添加完成'.format(form.name.data))
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
        db.session.add(idc)
        db.session.commit()
        flash(u'机房:{0} 修改完成'.format(idc.name))
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
#@permission_required(Permission.IDC_DEL)
def delete_idc(id):
    idc = Idc.query.get_or_404(id)
    db.session.delete(idc)
    flash(u'机房: {0} 已删除!'.format(idc.name))
    return redirect(url_for('main.show_idcs'))


########################################################################



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
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash(u'修改资料成功!')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
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
