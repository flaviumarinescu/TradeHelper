from os import environ

DATABASE_URL = f'postgres://{environ.get("POSTGRES_USER")}:{environ.get("POSTGRES_PASSWORD")}@db:5432/{environ.get("POSTGRES_DB")}'


DATABASE_URL = (
    "postgres://{}:{}@{}:{}/{}".format(  # pylint: disable=consider-using-f-string
        environ.get("POSTGRES_USER"),
        environ.get("POSTGRES_PASSWORD"),
        "db",  # service name
        "5432",
        environ.get("POSTGRES_DB"),
    )
)


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.database.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
