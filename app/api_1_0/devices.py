__author__ = 'eric'



from . import api
from ..models import Permission, Device, DevicePower
from flask import jsonify
from .decorators import permission_required

from .authentication import auth

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


@api.route('/devicePower/<int:id>')
@auth.login_required
@permission_required(Permission.DEVICE_LOOK)
def get_devicePower(id):
    devicePower = DevicePower.query.get_or_404(id)
    return jsonify({'devicePower': devicePower.to_json()})


        # @api.route('/devices/', methods=['POST'])
# @permission_required(Permission.DEVICE_EDIT)
# def new_device():
#     pass