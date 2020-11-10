import boto3
from config.aws_config import *


def ses_verify_email_address(email):
    if not email:
        return None

    ses = boto3.client(
        'ses',
        region_name=AWS_SES_REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    return ses.verify_email_identity(EmailAddress=email)
