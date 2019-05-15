from pymongo import MongoClient

from database.bi_models.lms_limits_master import lms_limits_master_model
from database.db_constants import lms_limits_master_columns
from database.db_init import mongo_db_init


def upsert_data(row, session, LmsLimitsMaster):
    # change key
    v = row['_id']
    del row['_id']
    row['source_id'] = str(v)

    for key in list(row):
        if key not in lms_limits_master_columns:
            del row[key]

    lms_limits_master_row = LmsLimitsMaster(**row)
    session.merge(lms_limits_master_row)
    session.commit()


def migrate_data(data, session, LmsLimitsMaster):
    for row in data:
        upsert_data(row, session, LmsLimitsMaster)


def lms_limits_master_service(data, operation_type):
    session, LmsLimitsMaster = lms_limits_master_model()

    if not data:
        client = mongo_db_init()
        db = client.test
        lms_limits_master = db['lms_limits_master']
        migrated_data = lms_limits_master.find({})

    if not operation_type == 'delete':
        if not data:
            migrate_data(migrated_data, session, LmsLimitsMaster)
        else:
            upsert_data(data, session, LmsLimitsMaster)

        session.close()

    else:
        v = data['_id']
        del data['_id']
        data['source_id'] = str(v)

        obj = LmsLimitsMaster.query.filter_by(_id=data['source_id']).one()
        session.delete(obj)
        session.commit()

    return "done"
