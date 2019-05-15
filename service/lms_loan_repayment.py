from pymongo import MongoClient

from database.bi_models.business import cas_business_model
from database.bi_models.lms_loan_repayment import lms_loan_repayment_model
from database.bi_models.scf_invoice import scf_invoice_model
from database.db_constants import business_db_columns, business_partners_db_columns, scf_invoice_db_columns, \
    lms_loan_repayment_columns
from database.db_init import mongo_db_init


def upsert_data(row, session, LmsLoanRepayment):
    # change key
    v = row['_id']
    del row['_id']
    row['source_id'] = str(v)

    if 'initiator' not in row:
        row['initiator'] = "None"

    for key in list(row):
        if key not in lms_loan_repayment_columns:
            del row[key]

    lms_loan_repayment_row = LmsLoanRepayment(**row)
    session.merge(lms_loan_repayment_row)
    session.commit()


def migrate_data(data, session, LmsLoanRepayment):
    for row in data:
        upsert_data(row, session, LmsLoanRepayment)


def lms_loan_repayment_service(data, operation_type):
    session, LmsLoanRepayment = lms_loan_repayment_model()

    if not data:
        client = mongo_db_init()
        db = client.test3
        lms_loan_repayment = db['lms_loan_repayment']
        migrated_data = lms_loan_repayment.find({})

    if not operation_type == 'delete':
        if not data:
            migrate_data(migrated_data, session, LmsLoanRepayment)
        else:
            upsert_data(data, session, LmsLoanRepayment)

        session.close()

    else:
        v = data['_id']
        del data['_id']
        data['source_id'] = str(v)

        obj = LmsLoanRepayment.query.filter_by(_id=data['source_id']).one()
        session.delete(obj)
        session.commit()

    return "done"
