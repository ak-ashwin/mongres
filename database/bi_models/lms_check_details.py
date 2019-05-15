from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, Text, Float, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.db_init import postgres_db_init


def lms_check_details_model():
    db = postgres_db_init()
    Base = declarative_base(bind=db)
    Session = sessionmaker(bind=db)

    class LmsCheckDetail(Base):
        __tablename__ = 'lms_check_details'

        source_id = Column(Text, nullable=False)
        business_id = Column(Text, primary_key=True)
        check_amount = Column(Float(53), nullable=False)
        check_id = Column(Text, nullable=False)
        check_no = Column(Text, nullable=False)
        ifsc_code = Column(Text)
        reason = Column(Text)
        repayment_id = Column(Text)
        status = Column(Text)

    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all()
    session = Session()

    return session, LmsCheckDetail
