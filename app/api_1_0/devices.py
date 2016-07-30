# -*- coding:utf-8 -*-


__author__ = 'eric'



from . import api
from ..models import *
from flask import jsonify, g
from .decorators import permission_required
from .authentication import auth
from .errors import ValidationError



@api.route('/assets/')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_assets():
    assets = Asset.query.all()
    return jsonify({'assets': [ asset.to_json() for asset in assets ]})


@api.route('/asset/<int:id>')
@auth.login_required
@permission_required(Permission.ASSET_LOOK)
def get_asset(id):
    asset = Asset.query.get_or_404(id)
    return jsonify( {'assets': asset.to_json()} )

@api.route('/asset/', methods=['POST'])
@auth.login_required
@permission_required(Permission.ASSET_EDIT)
def new_asset():
    asset = Asset.from_json(request.json)
    asset.instaff = g.current_user
    db.session.add(asset)
    db.session.commit()
    return jsonify(asset.to_json()), 201, \
           {'url': url_for('api.get_asset', id=asset.id, _external=True)}



@api.route('/devices/')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_devices():
    devices = Device.query.all()
    return jsonify({'devices': [ device.to_json() for device in devices ]})


@api.route('/device/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_device(id):
    device = Device.query.get_or_404(id)
    return jsonify({'device': device.to_json()})

@api.route('/device/', methods=['POST'])
@auth.login_required
@permission_required(Permission.DEVICE_EDIT)
def new_device():

    sn = request.json.get('sn',None)
    if sn is None and sn == '':
        raise ValidationError(u'设备SN不能为空.')

    asset = db.session.query(Asset).filter(Asset.sn == sn).first()
    device = Device.from_json(request.json)
    device.asset_id = asset.id
    device.instaff = g.current_user
    db.session.add(device)
    db.session.commit()
    return jsonify(device.to_json()), 201, \
           {'url': url_for('api.get_device', id=device.id, _external=True)}


@api.route('/devicePower/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_devicePower(id):
    devicePower = DevicePower.query.get_or_404(id)
    return jsonify({'devicePower': devicePower.to_json()})


@api.route('/devicePort/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_devicePort(id):
    devicePort = DevicePorts.query.get_or_404(id)
    return jsonify({'devicePort': devicePort.to_json()})



        # @api.route('/devices/', methods=['POST'])
# @permission_required(Permission.DEVICE_EDIT)
# def new_device():
#     pass