from flask import Flask, request
from services import database_service

app = Flask(__name__)

db_service = database_service.DatabaseService()
session = db_service.session


@app.route('/populate_database')
def populate_database():
    db_service.populate_database_initially()
    return "Data successfully initialized"


@app.route('/upload-firmware_update', methods=['POST'])
def upload_firmware_update():
    data = request.get_json()
    print('Data Received: "{data}"'.format(data=data))
    return data
