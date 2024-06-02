from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from app.choices import LogStatus
from app.database import Base, TimestampMixin


class Log(Base, TimestampMixin):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey('notifications.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    status = Column(Enum(LogStatus), default=LogStatus.PENDING)

    notification = relationship('Notification', uselist=False, back_populates='logs')
    student = relationship('Student', uselist=False, back_populates='logs')

    def __str__(self):
        return f'{self.id}'


class Notification(Base, TimestampMixin):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)

    logs = relationship('Log', uselist=False, back_populates='notification')

    def __str__(self):
        return f'{self.id}: {self.message[:10]}'


class Student(Base, TimestampMixin):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    username = Column(String, default='', nullable=True)
    full_name = Column(String, default='', nullable=True)
    birth_date = Column(Date, nullable=True)

    logs = relationship('Log', uselist=False, back_populates='student')

    def __str__(self):
        return f'{self.id}: {self.phone_number}'


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, default='', nullable=True)
    full_name = Column(String, default='', nullable=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    password = Column(String)

    def __str__(self):
        return f'{self.username}'
