from pydantic import BaseModel


class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    is_admin_email: bool
    email_setting_user_id: int
    template_name: str


class EmailLogSchema(BaseModel):
    to_email: str
    template_name: str
    status: str
    payload: dict
    send_by_id: int | None
    user_id: int | None
    error_message: str | None
