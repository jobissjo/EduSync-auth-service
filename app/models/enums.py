import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    MODERATOR = "moderator"


class EmailType(str, enum.Enum):
    SMTP = "smtp"
    MSAL = "msal"
