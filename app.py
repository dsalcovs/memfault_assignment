from flask import Flask, request

from models import models
from services import database_service, validation_service

app = Flask(__name__)

db_service = database_service.DatabaseService()
session = db_service.session

val_service = validation_service.ValidationService(session)


@app.route('/populate_database')
def populate_database():
    db_service.populate_database_initially()
    return "Data successfully initialized"


@app.route('/upload_firmware_update', methods=['POST'])
def upload_firmware_update():
    data = request.get_json()
    device_id = data['device_id']
    secret = data['secret']
    version = data['version']

    # validation
    is_version_format_valid = val_service.validate_version_format(version)
    if not is_version_format_valid:
        return "Version string formatting not valid"

    is_secret_valid = val_service.validate_device(device_id, secret)
    if not is_secret_valid:
        return "Invalid request"  # Don't want to return specific information about the secret being incorrect

    # persist event if validation passes
    firmware_update = models.DeviceFirmwareUpdates(device_id=device_id, version=version)
    session.add(firmware_update)
    session.commit()

    return "Successfully updated firmware version"


@app.route('/get_firmware_updates_by_device_id', methods=['GET'])
def get_firmware_updates_by_device_id():

