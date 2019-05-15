import json
import os
import logging
import boto3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from service.business import cas_business_service
from service.lms_check_details import lms_check_details_service
from service.lms_limits_master import lms_limits_master_service
from service.lms_loan_repayment import lms_loan_repayment_service
from service.lms_loans import lms_loans_service
from service.scf_invoice import scf_invoice_service

__logger = logging.getLogger(__name__)

"""
access is provisioned through IAM permissions.
"""
__sqs = boto3.resource('sqs')


def __report(code, message):
    """

    :param code:
    :param message:
    :return:
    """
    return dict(code=code, message=message)


def __is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def __fn_get_queue(queue_name):
    """

    :param queue_name:
    :return:
    """
    # Get the queue.
    queue = __sqs.get_queue_by_name(QueueName=queue_name)
    return queue


def process_messages(event, context):
    """
    This is the lambda event handler that is triggered when a message is sent to the corresponding SQS queue
    :param event:
    :param context:
    :return:
    """

    if event and "Records" in event and event["Records"]:
        event_records = event["Records"]
        if event_records:
            for event_record in event_records:
                __logger.info("event record")
                __logger.info(json.dumps(event_record, indent=4, sort_keys=True, default=str))
                __logger.info("Message Body: " + event_record["body"])
                message = json.loads(event_record["body"])
                if message:
                    try:
                        document = message[0]
                        collection_name = message[1]
                        operation_type = message[2]

                        if collection_name == 'cas_business':
                            cas_business_service(document, operation_type)

                        elif collection_name == 'scf_invoice':
                            scf_invoice_service(document, operation_type)

                        elif collection_name == 'lms_loan':
                            lms_loans_service(document, operation_type)

                        elif collection_name == 'lms_limits_master':
                            lms_limits_master_service(document, operation_type)

                        elif collection_name == 'lms_check_details':
                            lms_check_details_service(document, operation_type)



                    except:
                        import traceback
                        __logger.error("Critical exception in Human Task Handler!!!")
                        __logger.error(traceback.format_exc())

        else:
            print("event is empty! nothing to do")
        return "Success!"
