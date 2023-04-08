
"""Settings module"""

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="cache_app",
    settings_files=["settings.toml", ],
    environments=["development", "production", "testing"],
    env_switcher="api_cache_env",
    load_dotenv=False,
)
