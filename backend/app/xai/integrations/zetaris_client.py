import os
from contextlib import contextmanager

import jaydebeapi


DRIVER_CLASS = "com.zetaris.lightning.jdbc.LightningDriver"


def get_zetaris_config():
    """Read Zetaris JDBC configuration from environment variables."""
    required = [
        "ZETARIS_JDBC_URL",
        "ZETARIS_USERNAME",
        "ZETARIS_PASSWORD",
        "ZETARIS_JDBC_DRIVER_PATH",
    ]

    missing = [name for name in required if not os.getenv(name)]

    if missing:
        raise RuntimeError(
            "Missing Zetaris configuration: " + ", ".join(missing)
        )

    return {
        "url": os.environ["ZETARIS_JDBC_URL"],
        "username": os.environ["ZETARIS_USERNAME"],
        "password": os.environ["ZETARIS_PASSWORD"],
        "driver_path": os.environ["ZETARIS_JDBC_DRIVER_PATH"],
    }


@contextmanager
def zetaris_connection():
    """Open and close a Zetaris JDBC connection."""
    config = get_zetaris_config()

    connection = jaydebeapi.connect(
        DRIVER_CLASS,
        config["url"],
        [config["username"], config["password"]],
        config["driver_path"],
    )

    try:
        yield connection
    finally:
        connection.close()


def test_zetaris_connection():
    """Run a basic Zetaris connectivity check."""
    with zetaris_connection() as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result[0] == 1
        finally:
            cursor.close()
