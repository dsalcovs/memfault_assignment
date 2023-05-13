from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import models


class DatabaseService:
    def __init__(self):
        engine = create_engine('postgresql://localhost:5432/memfault_assignment')
        Session = sessionmaker(engine)
        self.session = Session()

    # delete all data from tables to make sure we are not entering duplicate records
    # when the endpoint is hit multiple times. Will also clear any changes made to the DB
    # through the app.
    # Meant to be private to this service
    def __depopulate_database(self):
        self.session.query(models.DeviceFirmwareUpdates).delete()
        self.session.query(models.DeviceApiKeys).delete()
        self.session.query(models.Devices).delete()
        self.session.query(models.ProjectMembershipApiKeys).delete()
        self.session.query(models.ProjectMemberships).delete()
        self.session.query(models.Projects).delete()
        self.session.commit()

    def populate_database_initially(self):
        # first we depopulate to avoid entering duplicate records
        self.__depopulate_database()

        # projects
        project_1 = models.Projects()
        project_2 = models.Projects()
        self.session.add_all([project_1, project_2])
        self.session.commit()

        # project memberships
        project_membership_1 = models.ProjectMemberships(project_id=project_1.id, email="diegosalcovsky@gmail.com")
        project_membership_2 = models.ProjectMemberships(project_id=project_2.id, email="jasontatum@gmail.com")
        self.session.add_all([project_membership_1, project_membership_2])
        self.session.commit()

        # project memberships api keys
        project_membership_api_key_1 = models.ProjectMembershipApiKeys(project_membership_id=project_membership_1.id,
                                                                       secret="ABC")
        project_membership_api_key_2 = models.ProjectMembershipApiKeys(project_membership_id=project_membership_2.id,
                                                                       secret="DEF")
        self.session.add_all([project_membership_api_key_1, project_membership_api_key_2])
        self.session.commit()

        # devices
        device_1 = models.Devices(project_id=project_1.id)
        device_2 = models.Devices(project_id=project_2.id)
        self.session.add_all([device_1, device_2])
        self.session.commit()

        # device_firmware_updates
        device_firmware_updates_1 = models.DeviceFirmwareUpdates(device_id=device_1.id, version="SemVer1.0")
        device_firmware_updates_2 = models.DeviceFirmwareUpdates(device_id=device_2.id, version="SemVer1.0")
        self.session.add_all([device_firmware_updates_1, device_firmware_updates_2])
        self.session.commit()

        # device api keys
        device_api_key_1 = models.DeviceApiKeys(device_id=device_1.id, secret="AAA")
        device_api_key_2 = models.DeviceApiKeys(device_id=device_2.id, secret="BBB")
        self.session.add_all([device_api_key_1, device_api_key_2])
        self.session.commit()


