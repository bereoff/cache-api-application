from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name = "cache-app"
    version = "0.1.0",
    description = "Cache app is an application to get data from any source and cache on redis",  # noqaE501
    api_url: str

    class Config:
        env_file = ".env"
