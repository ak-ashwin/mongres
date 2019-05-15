from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, Text, Float, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.db_init import postgres_db_init


def lms_loan_repayment_model():
    db = postgres_db_init()
    Base = declarative_base(bind=db)
    Session = sessionmaker(bind=db)

    class LmsLoanRepayment(Base):
        __tablename__ = 'lms_loan_repayment'

        source_id = Column(Text, nullable=False)
        business_id = Column(Text, nullable=False)
        created_at_pretty = Column(Text)
        created_by = Column(Text)
        initiator = Column(Text)
        installment_number = Column(Text)
        loan_account_id = Column(Text)
        org_name = Column(Text)
        payment_ref_no = Column(Text)
        preclosure = Column(Text)
        remarks = Column(Text)
        reason = Column(Text)
        repayment_amount = Column(Float(53), nullable=False)
        repayment_date = Column(Text, nullable=False)
        repayment_id = Column(Text, primary_key=True)
        repayment_mode = Column(Text, nullable=False)
        repayment_type = Column(Text, nullable=False)
        status = Column(Text, nullable=False)
        check_id = Column(Text)

    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all()
    session = Session()

    return session, LmsLoanRepayment
