from database.bi_models.scf_invoice import scf_invoice_model
from database.db_constants import scf_invoice_db_columns
from database.db_init import mongo_db_init


def scf_invoice_service(data, operation_type):
    session, ScfInvoice = scf_invoice_model()

    if not data:
        client = mongo_db_init()
        db = client.test2
        scf_invoice = db['scf_invoice']
        migrated_data = scf_invoice.find({})

    if not operation_type == 'delete':
        if not data:
            migrate_data(migrated_data, session, ScfInvoice)
        else:
            upsert_data(data, session, ScfInvoice)

        session.close()

    else:
        v = data['_id']
        del data['_id']
        data['source_id'] = str(v)

        obj = ScfInvoice.query.filter_by(_id=data['source_id']).one()
        session.delete(obj)
        session.commit()

    return "done"


def upsert_data(row, session, ScfInvoice):
    # change key
    v = row['_id']
    del row['_id']
    row['source_id'] = str(v)

    if 'initiator' not in row:
        row['initiator'] = "None"

    for key in list(row):
        if key not in scf_invoice_db_columns:
            del row[key]

    scf_invoice_row = ScfInvoice(**row)
    session.merge(scf_invoice_row)
    session.commit()


def migrate_data(data, session, ScfInvoice):
    for row in data:
        upsert_data(row, session, ScfInvoice)
