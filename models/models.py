from sqlalchemy import MetaData, Table, Column, Integer, String, JSON, Boolean

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('referral_code', String),
    Column('referrals', JSON),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)
