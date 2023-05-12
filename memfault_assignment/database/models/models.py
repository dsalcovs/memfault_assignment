from sqlalchemy import Column, String, Integer, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, nullable=False)

    def __repr__(self):
        return 'id: {}'.format(self.id)


class ProjectMemberships(Base):
    __tablename__ = 'project_memberships'
    id = Column(Integer, primary_key=True, nullable=False)
    project_id = Column(ForeignKey('projects.id'), nullable=False, index=True)
    email = Column(String, nullable=False)

    project = relationship(Projects)

    def __repr__(self):
        return 'id: {}'.format(self.id)


class ProjectMembershipApiKeys(Base):
    __tablename__ = 'project_membership_api_keys'
    id = Column(Integer, primary_key=True, nullable=False)
    project_membership_id = Column(ForeignKey('project_memberships.id'), nullable=False, index=True)
    secret = Column(String, nullable=False)

    project_membership = relationship(ProjectMemberships)

    def __repr__(self):
        return 'id: {}'.format(self.id)


class Devices(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, nullable=False)
    project_id = Column(ForeignKey('projects.id'), nullable=False, index=True)

    project = relationship(Projects)

    def __repr__(self):
        return 'id: {}'.format(self.id)


class DeviceApiKeys(Base):
    __tablename__ = 'device_api_keys'
    id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(ForeignKey('devices.id'), nullable=False, index=True)
    secret = Column(String, nullable=False)

    device = relationship(Devices)

    def __repr__(self):
        return 'id: {}'.format(self.id)
