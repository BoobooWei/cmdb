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

    return render_template('edit_assettype.html', form=form)


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







@main.route('/test', methods=['GET', 'POST'])
#@login_required
def test():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.qq = form.qq.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'提交成功!')
        return redirect(url_for('main.test',username=current_user.username))

    form.name.data = current_user.name
    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.qq.data = current_user.qq
    form.phone.data = current_user.phone
    return render_template('test.html',form=form)



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
