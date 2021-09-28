"""
Configuration.

FIELDS:
    Key: the field name the gateway expects
        val: A function used to validate the value in the input
        inc: A bitmask to show which requests this is a field for
        req: A bitmask to show which requests this field is required for 
            (must be smaller than inc)
"""
from lib.requesttype import RequestType
import re
from lib.logger import createLogger
from dotenv import load_dotenv
import os

load_dotenv()
log = createLogger(__name__)

AUTH = RequestType.AUTH.value
QUERY = RequestType.TRANSACTIONQUERY.value
UPDATE = RequestType.TRANSACTIONUPDATE.value
REFUND = RequestType.REFUND.value
CHECK = RequestType.ACCOUNTCHECK.value
NONE = RequestType.NONE.value


def validateDateTime(datetime):
    return not not re.fullmatch(  # not not returns True rather than the match object
        "[12]{1}[0-9]{3}-(01|02|03|04|05|06|07|08|09|10|11|12)-([012]{1}[0-9]{1}|30|31)\s([01]{1}[0-9]{1}|20|21|22|23)(:[0-5]{1}[0-9]{1}){2}",
        datetime
    )


def validateBaseamount(amount):
    return not not re.fullmatch(  # not not returns True rather than the match object
        "[1-9]+[0-9]*",
        amount
    )


def validateEmail(email):
    return not not re.fullmatch("[^@]+@[a-z]+\.[a-z]+", email)


def validateIP(ip):
    return not not re.fullmatch("([0-9]{1,3}\.){3}[0-9]{1,3}", ip)


FIELDS = {
    "accounttypedescription": {
        "val": lambda string: not not re.fullmatch("(ECOM|MOTO|RECUR)", string),
        "inc": QUERY | AUTH,
        "req": AUTH
    },
    "billingemail": {
        "val": validateEmail,
        "inc": QUERY,
        "req": NONE
    },
    "billingfirstname": {
        "inc": QUERY,
        "req": NONE
    },
    "billinglastname": {
        "inc": QUERY,
        "req": NONE
    },
    "billingpostcode": {
        "inc": QUERY,
        "req": NONE
    },
    "billingpremise": {
        "inc": QUERY,
        "req": NONE
    },
    "billingstreet": {
        "inc": QUERY,
        "req": NONE
    },
    "currencyiso3a": {
        "inc": QUERY | AUTH,
        "req": AUTH
    },
    "customerip": {
        "inc": QUERY | AUTH,
        "req": NONE,
        "val": validateIP
    },
    "orderreference": {
        "inc": QUERY | AUTH | REFUND | UPDATE,
        "req": NONE
    },
    "pan": {
        "inc": QUERY | AUTH,
        "req": AUTH,
    },
    "parenttransactionreference": {
        "inc": QUERY | AUTH | REFUND,
        "req": REFUND
    },
    "paymenttypedescriptions": {
        "inc": QUERY | AUTH,
        "req": NONE
    },
    "requesttypedescriptions": {
        "inc": AUTH | REFUND | UPDATE | CHECK,
        "req": AUTH | REFUND | UPDATE | CHECK
    },
    "requesttypedescription": {
        "inc": QUERY,
        "req": NONE
    },
    "sitereference": {
        "inc": QUERY | AUTH | REFUND | UPDATE,
        "req": AUTH | REFUND | UPDATE
    },
    "transactionreference": {
        "inc": QUERY | UPDATE,
        "req": UPDATE
    },
    "authmethod": {
        "inc": AUTH,
        "req": NONE
    },
    "credentialsonfile": {
        "inc": AUTH | CHECK,
        "req": CHECK
    },
    "initiationreason": {
        "inc": AUTH,
        "req": NONE
    },
    "baseamount": {
        "inc": AUTH | REFUND,
        "req": AUTH
    },
    "expirydate": {
        "inc": AUTH | REFUND,
        "req": AUTH
    },
    "securitycode": {
        "inc": AUTH,
        "req": NONE
    },
    "chargedescription": {
        "inc": AUTH | REFUND,
        "req": NONE
    },
    "merchantemail": {
        "inc": AUTH,
        "req": NONE
    },
    "operatorname": {
        "inc": AUTH,
        "req": NONE
    },
    "customerstreet": {
        "inc": AUTH,
        "req": NONE
    },
    "customertown": {
        "inc": AUTH,
        "req": NONE
    },
    "customercounty": {
        "inc": AUTH,
        "req": NONE
    },
    "customercountryiso2a": {
        "inc": AUTH,
        "req": NONE
    },
    "customerpostcode": {
        "inc": AUTH,
        "req": NONE
    },
    "customeremail": {
        "inc": AUTH,
        "req": NONE
    },
    "customertelephonetype": {
        "inc": AUTH,
        "req": NONE
    },
    "customertelephone": {
        "inc": AUTH,
        "req": NONE
    },
    "customerprefixname": {
        "inc": AUTH,
        "req": NONE
    },
    "customerfirstname": {
        "inc": AUTH,
        "req": NONE
    },
    "customermiddlename": {
        "inc": AUTH,
        "req": NONE
    },
    "customerlastname": {
        "inc": AUTH,
        "req": NONE
    },
    "customersuffixname": {
        "inc": AUTH,
        "req": NONE
    },
    "customerforwardedip": {
        "inc": AUTH,
        "req": NONE,
        "val": validateIP
    },
    "settleduedate": {
        "inc": AUTH | UPDATE,
        "req": NONE,
    },
    "settlestatus": {
        "inc": AUTH | UPDATE,
        "req": NONE,
    },
    "settlebaseamount": {
        "inc": UPDATE,
        "req": NONE,
    }
}

tableHeaders = {
    "Transaction started": "transactionstartedtimestamp",
    "Reference": "transactionreference",
    "Amount": "baseamount",
    "Account type": "accounttypedescription",
    "Request type": "requesttypedescription",
    "Payment type": "paymenttypedescription",
    "Card number": "maskedpan",
    "Settle status": "settlestatus",
    "First name": "billingfirstname",
    "Last name": "billinglastname"
}


def runValidation(field, value):
    result = False
    try:
        result = FIELDS[field]["val"](value)
    except KeyError as ke:
        result = True
    return result
