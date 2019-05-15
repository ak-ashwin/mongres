from flask import Flask

from service.business import cas_business_service
from service.lms_check_details import lms_check_details_service
from service.lms_limits_master import lms_limits_master_service
from service.lms_loan_repayment import lms_loan_repayment_service
from service.lms_loans import lms_loans_service
from service.scf_invoice import scf_invoice_service

app = Flask(__name__)


@app.route('/cas_business')
def cas_business():
    cas_business_service('', '')
    return "done"


@app.route('/scf_invoice')
def scf_invoice():
    scf_invoice_service('', '')
    return "done"


@app.route('/lms_loan_repayment')
def lms_loan_repayment():
    lms_loan_repayment_service('', '')
    return "done"


@app.route('/lms_check_details')
def lms_check_details():
    lms_check_details_service('', '')
    return "done"


@app.route('/lms_limits_master')
def lms_limits_master():
    lms_limits_master_service('', '')
    return "done"


@app.route('/lms_loans')
def lms_loans():
    lms_loans_service('', '')
    return "done"


if __name__ == '__main__':
    app.run()
