import os

SECRET_KEY = 'p9Bv<3Eid9%$i01'

HOST = "http://localhost:8081/"

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

BROKER_HOST = os.environ.get("BROKER_HOST")
BROKER_PORT = os.environ.get("BROKER_PORT")

TOKEN = os.environ.get("TOKEN")

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(POSTGRES_USER,
                                                            POSTGRES_PASSWORD,
                                                            POSTGRES_HOST,
                                                            POSTGRES_DB)
