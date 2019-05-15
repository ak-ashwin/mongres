from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, Text, Float, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.db_init import postgres_db_init


def lms_loan_model():
    db = postgres_db_init()
    Base = declarative_base(bind=db)
    Session = sessionmaker(bind=db)

    class LmsLoanInstallment(Base):
        __tablename__ = 'lms_loan_installments'

        source_id = Column(Text, nullable=False)

        cashback_amount = Column(Float(53))
        cashback_paid = Column(Float(53))
        cashback_rate = Column(Text)
        cashback_type = Column(Text)
        check_id = Column(Text)
        from_date = Column(Text, nullable=False)
        installment_amount = Column(Float(53), nullable=False)
        installment_number = Column(Float(53), primary_key=True, nullable=False)
        interest_amount_accrued = Column(Float(53), nullable=False)
        interest_amount_outstanding = Column(Float(53), nullable=False)
        interest_days = Column(Float(53), nullable=False)
        interest_rate = Column(Text, nullable=False)
        interest_rate_definition_method = Column(Text)
        interest_repaid = Column(Float(53), nullable=False)
        interest_scheduled_to_be_repaid = Column(Float(53), nullable=False)
        interest_under_clearing = Column(Float(53))
        last_interest_applied_date = Column(Text)
        loan_overdue_date = Column(Text)
        loan_principal_outstanding = Column(Float(53))
        overdue_duration = Column(BigInteger)
        overdue_interest_amount = Column(Float(53), nullable=False)
        overdue_interest_repaid = Column(Float(53), nullable=False)
        overdue_outstanding = Column(Float(53), nullable=False)
        overdue_under_clearing = Column(Float(53))
        principal_expected = Column(Float(53), nullable=False)
        principal_outstanding = Column(Float, nullable=False)
        principal_repaid = Column(Float(53), nullable=False)
        principal_under_clearing = Column(Float(53))
        repayment_due_date = Column(Text, nullable=False)
        repayment_mode = Column(Text)
        repayment_ref_no = Column(Text)
        status = Column(Text, nullable=False)
        to_date = Column(Text, nullable=False)

        loan_account_id = Column(ForeignKey('lms_loan.loan_account_id', ondelete='cascade'), primary_key=True)

    class LmsLoan(Base):
        __tablename__ = 'lms_loan'

        source_id = Column(Text, nullable=False)
        business_id = Column(Text)
        cashback_amount = Column(Float(53))
        cashback_paid = Column(Float(53))
        created_at = Column(Text)
        fee_amount = Column(Float(53))
        fee_amount_outstanding = Column(Float(53))
        fee_amount_paid = Column(Float(53))
        fee_amount_waived = Column(Float(53))
        fee_under_clearing = Column(Float(53))
        interest_amount_accrued = Column(Float(53))
        interest_amount_outstanding = Column(Float(53), nullable=False)
        interest_repaid = Column(Float(53), nullable=False)
        last_modified_date = Column(Text)
        last_repayment_date = Column(Text)
        lending_org_name = Column(Text, nullable=False)
        loan_account_id = Column(Text, nullable=False, primary_key=True)
        loan_closed_date = Column(Text)
        loan_type = Column(Text, nullable=False)
        master_loan_account_id = Column(Text, nullable=False)
        maturity_date = Column(Text, nullable=False)
        org_name = Column(Text, nullable=False)
        overdue_duration = Column(BigInteger, nullable=False)
        overdue_interest_amount = Column(Float(53), nullable=False)
        overdue_interest_repaid = Column(Float(53), nullable=False)
        overdue_outstanding = Column(Float(53), nullable=False)
        principal_disbursed = Column(Float(53), nullable=False)
        principal_expected = Column(Float(53), nullable=False)
        principal_outstanding = Column(Float, nullable=False)
        principal_repaid = Column(Float(53), nullable=False)
        product_code = Column(Text, nullable=False)
        retailer_id = Column(Text)
        start_date = Column(Text, nullable=False)
        status = Column(Text, nullable=False)
        sub_status = Column(Text, nullable=False)

        installments = relationship(
            LmsLoanInstallment,
            backref='lms_loan',
            cascade="save-update, merge, delete, delete-orphan",
            lazy='dynamic',
            passive_deletes=True
        )

    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all()
    session = Session()

    return session, LmsLoan, LmsLoanInstallment
