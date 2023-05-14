from sqlalchemy import select
from sqlalchemy.sql.functions import count, func

from models import models
import re


class ValidationService:
    def __init__(self, session):
        self.session = session

    def validate_device(self, device_id, secret):
        device_api_key_count = self.session.query(models.DeviceApiKeys).filter(
            models.DeviceApiKeys.device_id == device_id,
            models.DeviceApiKeys.secret == secret
        ).count()

        return True if device_api_key_count else False

    def is_user_allow_to_access_device_updates(self, email, device_id, secret):
        device = self.session.query(models.Devices).filter(models.Devices.id == device_id).one()

        project_membership = self.session.query(models.ProjectMemberships).filter(
            models.ProjectMemberships.project_id == device.project_id,
            models.ProjectMemberships.email == email
        ).one()
        project_membership_api_key_count = self.session.query(models.ProjectMembershipApiKeys).filter(
            models.ProjectMembershipApiKeys.project_membership_id == project_membership.id,
            models.ProjectMembershipApiKeys.secret == secret
        ).count()

        return True if project_membership_api_key_count else False

    def validate_version_format(self, version):
        validation_regex = re.compile(r'^SemVer+[0-9]+\.+[0-9]*$')
        return True if validation_regex.match(version) else False
