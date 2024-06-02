import enum


class LogStatus(enum.Enum):
    SENT = "sent"
    PENDING = "pending"
    FAILED = "failed"
