import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST="guest"


class EmailType(str, enum.Enum):
    SMTP = "smtp"
    MSAL = "msal"
