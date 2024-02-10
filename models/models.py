from sqlalchemy import MetaData, Table, Column, Integer, String, JSON

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('email', Integer, nullable=False),
    Column('password', String, nullable=False),
    Column('referral_code', String),
    Column('referrals', JSON),
)
