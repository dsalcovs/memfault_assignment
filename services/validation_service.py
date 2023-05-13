from sqlalchemy import select
from sqlalchemy.sql.functions import count, func

from models import models
import re


class ValidationService:
    def __init__(self, session):
        self.session = session

    def validate_device(self, device_id, secret):
        device_api_key = self.session.query(models.DeviceApiKeys).filter(models.DeviceApiKeys.device_id == device_id,
                                                                         models.DeviceApiKeys.secret == secret).count()

        return True if device_api_key else False

    def validate_user(self, device_id, email):
        pass

    def validate_version_format(self, version):
        validation_regex = re.compile(r'^SemVer+[0-9]+\.+[0-9]*$')
        return True if validation_regex.match(version) else False
