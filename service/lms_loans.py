from pymongo import MongoClient

from database.bi_models.business import cas_business_model
from database.bi_models.lms_loans import lms_loan_model
from database.db_constants import business_db_columns, business_partners_db_columns, lms_loan_columns, \
    lms_loan_installment_columns
from database.db_init import mongo_db_init


def upsert_data(row, session, LmsLoan, LmsLoanInstallment):
    # change key
    v = row['_id']
    del row['_id']
    row['source_id'] = str(v)

    for key in list(row):
        if key not in lms_loan_columns:
            del row[key]

    rec = row.copy()
    if "installments" in rec:
        del rec["installments"]

    if 'principal_outstanding' not in rec:
        rec['principal_outstanding'] = 0.0

    lms_loan = LmsLoan(**rec)

    installments = []
    for i, data in enumerate(row['installments']):

        for key in list(data):
            if key not in lms_loan_installment_columns:
                del data[key]

        print("@@@@@@@@@@@@@@@")
        print(data)
        print("::::::::::::::::")

        data['loan_account_id'] = row['loan_account_id']
        data['source_id'] = row['source_id']

        installment_data = LmsLoanInstallment(**data)
        installments.append(installment_data)

    lms_loan.installments = installments
    session.merge(lms_loan)
    session.commit()


def migrate_data(data, session, LmsLoan, LmsLoanInstallment):
    for row in data:
        upsert_data(row, session, LmsLoan, LmsLoanInstallment)


def lms_loans_service(data, operation_type):
    session, LmsLoan, LmsLoanInstallment = lms_loan_model()

    if not data:
        client = mongo_db_init()
        db = client.test
        lms_loan = db['lms_loan']
        migrated_data = lms_loan.find({})

    if not operation_type == 'delete':
        if not data:
            migrate_data(migrated_data, session, LmsLoan, LmsLoanInstallment)
        else:
            upsert_data(data, session, LmsLoan, LmsLoanInstallment)

        session.close()

    else:
        v = data['_id']
        del data['_id']
        data['source_id'] = str(v)

        obj = LmsLoan.query.filter_by(_id=data['source_id']).one()
        session.delete(obj)
        session.commit()

    return "done"
