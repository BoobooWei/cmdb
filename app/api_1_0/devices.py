# -*- coding:utf-8 -*-


__author__ = 'eric'



from . import api
from ..models import *
from flask import jsonify, g, abort
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
    devicePower = DevicePower.query.filter(DevicePower.device_id == id)
    if not devicePower.all():
        abort(404)
    if devicePower.count() >1:
        raise ValidationError(u'该设备电源管理ip有多个. 安全期间请在CMDB中删除不正确的电源管理.')

    return jsonify({'devicePower': devicePower.first().to_json()})


@api.route('/deviceModel/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_deviceModel(id):
    deviceModel = DeviceModel.query.get_or_404(id)
    return jsonify({'deviceModel': deviceModel.to_json()})



@api.route('/deviceModels/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_deviceModels(id):
    deviceModels = DeviceModel.query.filter(DeviceModel.device_id == id).all()
    return jsonify({'deviceModels': [ deviceModel.to_json() for deviceModel in deviceModels ]})



@api.route('/devicePort/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_devicePort(id):
    devicePort = DevicePorts.query.get_or_404(id)
    return jsonify({'devicePort': devicePort.to_json()})



@api.route('/devicePorts/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_devicePorts(id):
    devicePorts = DevicePorts.query.filter(DevicePorts.model_id == id).all()
    return jsonify({'devicePorts': [devicePort.to_json() for devicePort in devicePorts]})



@api.route('/deviceDisks/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_deviceDisks(id):
    deviceDisks = DeviceDisks.query.filter(DeviceDisks.device_id == id).all()
    return jsonify({'deviceDisks': [deviceDisk.to_json() for deviceDisk in deviceDisks]})



@api.route('/deviceDisk/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_deviceDisk(id):
    deviceDisk = DeviceDisks.query.get_or_404(id)
    return jsonify({'deviceDisk': deviceDisk.to_json()})



@api.route('/rack/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_rack(id):
    rack = Rack.query.get_or_404(id)
    return jsonify({'rack': rack.to_json()})



@api.route('/racks/')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_racks():
    racks = Rack.query.all()
    return jsonify({'racks': [ rack.to_json() for rack in racks]})



@api.route('/idc/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_idc(id):
    idc = Idc.query.get_or_404(id)
    return jsonify({'idc': idc.to_json()})



@api.route('/idcs/')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_idcs():
    idcs = Idc.query.all()
    return jsonify({'idcs': [idc.to_json() for idc in idcs]})

        # @api.route('/devices/', methods=['POST'])
# @permission_required(Permission.DEVICE_EDIT)
# def new_device():
#     pass