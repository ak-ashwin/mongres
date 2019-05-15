from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, Text, Float, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.db_init import postgres_db_init


def scf_invoice_model():
    db = postgres_db_init()
    Base = declarative_base(bind=db)
    Session = sessionmaker(bind=db)

    class ScfInvoice(Base):
        __tablename__ = 'scf_invoice'

        source_id = Column(Text, nullable=False)
        batch_id = Column(Float(53))
        business_id = Column(Text, nullable=False)
        check_amount = Column(Float(53))
        check_id = Column(Text)
        check_no = Column(Text)
        check_status = Column(Text)
        created_at = Column(Float(53))
        created_at_pretty = Column(Text)
        created_by = Column(Text)
        credit_product = Column(Text, nullable=False)
        credit_risk_notes = Column(Text)
        credit_risk_status = Column(Text)
        disbursement_date = Column(Text, nullable=False)
        invoice_due_date = Column(Text, nullable=False)
        invoice_id = Column(Text, nullable=False, unique=True, primary_key=True)
        invoice_issue_date = Column(Text, nullable=False)
        initiator = Column(Text)
        invoice_no = Column(Text, nullable=False)
        lending_org_name = Column(Text, nullable=False)
        loan_type = Column(Text, nullable=False)
        master_invoice_id = Column(Text, nullable=False)
        mode_of_repayment = Column(Text, nullable=False)
        org_name = Column(Text, nullable=False)
        overdrawn_percentage = Column(Float(53))
        program_id = Column(Text)
        remarks = Column(Text)
        retailer_id = Column(Text)
        status = Column(Text, nullable=False)
        total_amt_util_post_invoice = Column(Float(53))
        total_invoice_amount = Column(Float(53))
        ifsc_code = Column(Text)

    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all()
    session = Session()

    return session, ScfInvoice
