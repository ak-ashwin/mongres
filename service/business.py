from pymongo import MongoClient

from database.bi_models.business import cas_business_model
from database.db_constants import business_db_columns, business_partners_db_columns
from database.db_init import mongo_db_init


def upsert_data(row, session, CasBusiness, CasBusinessPartner):
    # change key
    v = row['_id']
    del row['_id']
    row['source_id'] = v

    if 'initiator' not in row:
        row['initiator'] = "None"

    if 'business_address_lng' not in row:
        row['business_address_lng'] = 0.0
    elif row['business_address_lng'] == '':
        row['business_address_lng'] = 0.0

    if 'business_address_lat' not in row:
        row['business_address_lat'] = 0.0
    elif row['business_address_lat'] == '':
        row['business_address_lat'] = 0.0

    if 'business_address_geolocation' not in row:
        row['business_address_geolocation'] = ''

    if 'business_address_google_geocoder' not in row:
        row['business_address_google_geocoder'] = ''

    if row['business_mobile_no'] == 'nan' or row['business_mobile_no'] == '':
        row['business_mobile_no'] = 0

    for key in list(row):
        if key not in business_db_columns:
            del row[key]

    only_business = all_business_data(**row)

    business = CasBusiness(**only_business)

    business_partners = []
    for i, data in enumerate(row['business_partners']):

        for key in list(data):
            if key not in business_partners_db_columns:
                del data[key]

        if 'individual_address_lng' not in data:
            data['individual_address_lng'] = 0.0
        elif data['individual_address_lng'] == '':
            data['individual_address_lng'] = 0.0

        if 'individual_address_lat' not in data:
            data['individual_address_lat'] = 0.0
        elif data['individual_address_lat'] == '':
            data['individual_address_lat'] = 0.0

        if 'individual_address_geolocation' not in data:
            data['individual_address_geolocation'] = ''

        if 'individual_address_google_geocoder' not in data:
            data['individual_address_google_geocoder'] = ''

        data['business_id'] = row['business_id']
        data['source_id'] = row['source_id']

        business_partner = CasBusinessPartner(**data)
        business_partners.append(business_partner)

    business.business_partners = business_partners
    session.merge(business)
    session.commit()


def migrate_data(data, session, CasBusiness, CasBusinessPartner):
    for row in data:
        upsert_data(row, session, CasBusiness, CasBusinessPartner)


def cas_business_service(data, operation_type):
    session, CasBusiness, CasBusinessPartner = cas_business_model()

    if not data:
        client = mongo_db_init()
        db = client.test3
        cas_business = db['cas_business']
        migrated_data = cas_business.find({})

    if not operation_type == 'delete':
        if data:
            migrate_data(migrated_data, session, CasBusiness, CasBusinessPartner)
        else:
            upsert_data(data, session, CasBusiness, CasBusinessPartner)

        session.close()

    else:
        v = data['_id']
        del data['_id']
        data['source_id'] = str(v)

        obj = CasBusiness.query.filter_by(_id=data['source_id']).one()
        session.delete(obj)
        session.commit()


def all_business_data(**data):
    if 'business_partners' in data:
        del data['business_partners']
    return data


def all_business_partners(**data):
    bus_partners = {}
    if 'business_partners' in data:
        bus_partners['business_partners'] = data['business_partners']
    return bus_partners
