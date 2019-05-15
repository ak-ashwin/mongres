from pymongo import MongoClient

from database.bi_models.lms_check_details import lms_check_details_model
from database.db_constants import business_db_columns, business_partners_db_columns, scf_invoice_db_columns, \
    lms_check_details_columns
from database.db_init import mongo_db_init


def upsert_data(row, session, LmsCheckDetail):
    # change key
    v = row['_id']
    del row['_id']
    row['source_id'] = str(v)

    for key in list(row):
        if key not in lms_check_details_columns:
            del row[key]

    lms_check_details_row = LmsCheckDetail(**row)
    session.merge(lms_check_details_row)
    session.commit()


def migrate_data(data, session, LmsCheckDetail):
    for row in data:
        upsert_data(row, session, LmsCheckDetail)


def lms_check_details_service(data, operation_type):
    session, LmsCheckDetail = lms_check_details_model()

    if not data:
        client = mongo_db_init()
        db = client.test
        lms_check_details = db['lms_check_details']
        migrated_data = lms_check_details.find({})

    if not operation_type == 'delete':
        if not data:
            migrate_data(migrated_data, session, LmsCheckDetail)
        else:
            upsert_data(data, session, LmsCheckDetail)

        session.close()

    else:
        v = data['_id']
        del data['_id']
        data['source_id'] = str(v)

        obj = LmsCheckDetail.query.filter_by(_id=data['source_id']).one()
        session.delete(obj)
        session.commit()

    return "done"
