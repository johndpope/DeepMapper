from sqlalchemy import *
from sqlalchemy.engine import Engine
import enum


def connect(user, password, db, host='localhost', port=5432):
    """Returns a connection and a metadata object"""
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    _con = create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    _meta = MetaData(bind=_con, reflect=False)

    return _con, _meta


con: Engine
con, meta = connect("snap", "chat", "snapdata", port=4818)

tbl_users = \
    Table("users", meta,
          Column("username", String),
          Column("gender", String),
          Column("age", Integer),
          Column("location", String),
          Column("sfw", Boolean),
          Column("bio", String),
          Column("profile_url", String)
          )


meta.create_all(con)
