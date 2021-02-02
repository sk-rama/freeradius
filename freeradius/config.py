from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My Awesome Freeradius API"
    admin_email: str = "admin@email.com"
    items_per_user: int = 50