from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, Text, Float, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.db_init import postgres_db_init


def lms_limits_master_model():
    db = postgres_db_init()
    Base = declarative_base(bind=db)
    Session = sessionmaker(bind=db)

    class LmsLimitsMaster(Base):
        __tablename__ = 'lms_limits_master'

        source_id = Column(Text, nullable=False)
        available_limit = Column(Float(53), nullable=False)
        blocked_limit = Column(Float(53))
        business_id = Column(Text, nullable=False, primary_key=True)
        created_at = Column(Text)
        lending_org_name = Column(Text)
        limit_amount_sanctioned = Column(Float(53), nullable=False)
        limit_amount_utilized = Column(Float(53), nullable=False)
        limits_under_clearing = Column(Float(53))
        org_name = Column(Text, nullable=False)
        retailer_id = Column(Text)
        status = Column(Text, nullable=False)
        updated_at = Column(Text)
        version = Column(BigInteger)

    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all()
    session = Session()

    return session, LmsLimitsMaster
