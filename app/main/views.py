#coding:utf8

from flask import render_template, redirect, url_for, flash, current_app, abort, request, make_response
from flask.ext.login import login_required, current_user
from ..decorators import admin_required, permission_required
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, EditDeviceForm, EditIdcForm, EditRackForm, EditDeviceTypeForm
from .. import db
from ..models import User,Role,Permission, Device, Idc, Device, DeviceType, Rack, Logger
from ..email import send_email


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #posts = user.posts.order_by(Post.timestamp.desc()).all()
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
        log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users', logobj_id=current_user.id)
        db.session.add(log)
        db.session.commit()
        flash(u'提交成功!')
        return redirect(url_for('main.edit_profile',username=current_user.username, logs=logs))

    form.name.data = current_user.name
    form.username.data = current_user.username
    form.position.data = current_user.position
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.qq.data = current_user.qq
    form.phone.data = current_user.phone
    return render_template('edit_profile.html',form=form, username=current_user.username, logs=logs)


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')



@main.route('/edit-devicetype', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ASSET_EDIT)
def edit_assettype():
    form = EditDeviceTypeForm()
    if form.validate_on_submit():
        devicetype = DeviceType(name=form.name.data, remarks=form.remarks.data)
        db.session.add(devicetype)

        #log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users', logobj_id=current_user.id)
        #db.session.add(log)
        db.session.commit()
        flash(u'设备类型添加成功')
        return redirect(url_for('main.index'))

    return render_template('test.html', form=form)


@main.route('/edit-rack', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.RACK_EDIT)
def edit_rack():
    form = EditRackForm()
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

        #log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users', logobj_id=current_user.id)
        #db.session.add(log)
        db.session.commit()
        flash(u'机柜添加成功')
        return redirect(url_for('main.index'))

    return render_template('test.html', form=form)


@main.route('/edit-idc', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.IDC_EDIT)
def edit_idc():
    form = EditIdcForm()
    if form.validate_on_submit():
        idc = Idc(name=form.name.data,
                  ispid=form.ispid.data,
                  city=form.city.data,
                  address=form.address.data,
                  contactid=form.contactid.data,
                  nettype=form.nettype.data,
                  netout=form.netout.data,
                  adnature=form.adnature.data,
                  remarks=form.remarks.data)
        db.session.add(idc)

        #log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users', logobj_id=current_user.id)
        #db.session.add(log)
        db.session.commit()
        flash(u'机房添加成功')
        return redirect(url_for('main.index'))

    return render_template('test.html', form=form)


@main.route('/edit-device', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_EDIT)
def edit_device():
    form = EditDeviceForm()
    if form.validate_on_submit():

        device = Device(Devicetype=DeviceType.query.get(form.Devicetype.data),
                  an=form.an.data,
                  sn=form.sn.data,
                  onstatus=form.onstatus.data,
                  flowstatus=form.flowstatus.data,
                  dateofmanufacture=form.dateofmanufacture.data,
                  manufacturer=form.manufacturer.data,
                  brand=form.brand.data,
                  model=form.model.data,
                  site=form.site.data,
                  usedept=form.usedept.data,
                  usestarttime=form.usestarttime.data,
                  useendtime=form.useendtime.data,
                  mainuses=form.mainuses.data,
                  managedept=form.managedept.data,
                  managestaff=form.managestaff.data,
                  koriyasustarttime=form.koriyasustarttime.data,
                  koriyasuendtime=form.koriyasuendtime.data,
                  equipprice=form.equipprice.data,

                  hostname=form.hostname.data,
                  private_ip=form.private_ip.data,
                  private_mac=form.private_mac.data,
                  public_ip=form.public_ip.data,
                  public_mac=form.public_mac.data,
                  other_ip=form.other_ip.data,
                  other_mac=form.other_mac.data,
                  rack=Rack.query.get(form.rack.data),

                  is_virtualization=form.is_virtualization.data,
                  cpumodel=form.cpumodel.data,
                  cpucount=form.cpucount.data,
                  memsize=form.memsize.data,
                  singlemem=form.singlemem.data,
                  raidmodel=form.raidmodel.data,
                  #disks=form.disks.data,

                  powermanage_enable=form.powermanage_enable.data,
                  powermanage_ip=form.powermanage_ip.data,
                  powermanage_user=form.powermanage_user.data,
                  powermanage_id=form.powermanage_id.data,

                  networkportcount=form.networkportcount.data,
                  os=form.os.data,
                  remarks=form.remarks.data)
        db.session.add(device)

        #log = Logger(user=current_user._get_current_object(), content=u'你更新了个人设置.', action=2, logobjtype='users', logobj_id=current_user.id)
        #db.session.add(log)
        db.session.commit()
        flash(u'设备添加成功')
        return redirect(url_for('main.index'))

    return render_template('test.html', form=form)


@main.route('/show-devicetype', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ASSET_LOOK)
def show_assettype():
    page = request.args.get('page', 1, type=int)
    pagination = AssetType.query.order_by(DeviceType.name.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    items = pagination.items
    return render_template('show_assettype.html', items=items, endpoint='main.show_assettype', pagination=pagination)




@main.route('/show-devices', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_devices():
    page = request.args.get('page', 1, type=int)
    pagination = Device.query.order_by(Device.powerstatus.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    items = pagination.items
    return render_template('show_devices.html', items=items, endpoint='main.show_assettype', pagination=pagination)


@main.route('/show-devices', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DEVICE_LOOK)
def show_racks():
    page = request.args.get('page', 1, type=int)
    pagination = Rack.query.order_by(Rack.name.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    items = pagination.items
    return render_template('show_racks.html', items=items, endpoint='main.show_racks', pagination=pagination)


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
        return redirect(url_for('main.user',username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form=form,user=user)
#print url_for('index')

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
    #app.run(host='0.0.0.0',debug=True)
