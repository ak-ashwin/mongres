from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, Text, Float, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.db_init import postgres_db_init


def cas_business_model():
    db = postgres_db_init()
    Base = declarative_base(bind=db)
    Session = sessionmaker(bind=db)

    class CasBusinessPartner(Base):
        __tablename__ = 'cas_business_partners'

        id = Column(BigInteger, Sequence('id'))
        aadhaar_no = Column(Text)
        address_line_1 = Column(Text)
        address_line_3 = Column(Text)
        applicant_type = Column(Text)
        city_name = Column(Text)
        city_pin_code = Column(Text)
        date_of_birth = Column(Text)
        educational_qualification = Column(Text)
        email_address = Column(Text)
        first_name = Column(Text)
        gender = Column(Text)
        individual_address_geolocation = Column(Text)
        individual_address_google_geocoder = Column(Text)
        individual_address_lat = Column(Float)
        individual_address_lng = Column(Float)
        last_name = Column(Text)
        main_applicant = Column(Text)
        marital_status = Column(Text)
        mobile_number = Column(BigInteger)
        pan_no = Column(Text, primary_key=True, nullable=False)
        residence_ownership = Column(Text)
        source_id = Column(Text, nullable=False)

        country_name = Column(Text)
        email_id = Column(Text)
        state_name = Column(Text)
        image_uploaded = Column(Text)
        aadhaar_qr_scan = Column(Text)

        business_id = Column(ForeignKey('cas_business.business_id', ondelete='cascade'), primary_key=True)

    class CasBusiness(Base):
        __tablename__ = 'cas_business'

        id = Column(BigInteger, Sequence('id'))
        annual_turnover = Column(Text, nullable=False)
        bank_od_cc_limit = Column(Text, nullable=False)
        business_address_geolocation = Column(Text)
        business_address_google_geocoder = Column(Text)
        business_address_lat = Column(Float)
        business_address_lng = Column(Float)
        business_category_code = Column(Text, nullable=False)
        business_id = Column(Text, unique=True, primary_key=True)
        business_mobile_no = Column(BigInteger)
        business_name = Column(Text, nullable=False)
        business_ownership = Column(Text, nullable=False)
        business_pan = Column(Text, nullable=False)
        business_type_code = Column(Text, nullable=False)
        created_at = Column(Numeric, nullable=False)
        created_at_pretty = Column(Text, nullable=False)
        created_by = Column(Text, nullable=False)
        gstin_no = Column(Text)
        initiator = Column(Text, nullable=False)
        migrated = Column(Text)
        no_of_employees = Column(BigInteger, nullable=False)
        no_of_partners = Column(BigInteger, nullable=False)
        old_business_id = Column(Text)
        operating_since_month = Column(Text, nullable=False)
        operating_since_year = Column(BigInteger, nullable=False)
        operating_type_code = Column(Text, nullable=False)
        org_name = Column(Text, nullable=False)
        primary_address_line_1 = Column(Text, nullable=False)
        primary_address_line_3 = Column(Text)
        primary_city_name = Column(Text, nullable=False)
        primary_pin_code = Column(BigInteger, nullable=False)
        retailer_id = Column(Text, nullable=False)
        version = Column(BigInteger)
        source_id = Column(Text, nullable=False)
        primary_state_name = Column(Text)

        business_partners = relationship(
            CasBusinessPartner,
            backref='cas_business',
            cascade="save-update, merge, delete, delete-orphan",
            lazy='dynamic',
            passive_deletes=True
        )

    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all()
    session = Session()

    return session, CasBusiness, CasBusinessPartner
