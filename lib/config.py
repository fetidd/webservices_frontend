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
from collections import OrderedDict

load_dotenv()
log = createLogger(__name__)

AUTH = RequestType.AUTH.value
QUERY = RequestType.TRANSACTIONQUERY.value
UPDATE = RequestType.TRANSACTIONUPDATE.value
REFUND = RequestType.REFUND.value
CHECK = RequestType.ACCOUNTCHECK.value
NONE = RequestType.NONE.value
CUSTOM = RequestType.CUSTOM.value


def validateEmail(email):
    return not not re.fullmatch("[^@]+@[a-z]+\.[a-z]+", email)


def validateIP(ip):
    return not not re.fullmatch("([0-9]{1,3}\.){3}[0-9]{1,3}", ip)


class Config:
    def __init__(self):
        self.HEADERS = OrderedDict({
            "transactionstartedtimestamp": {"humanString": "Transaction started", "active": True},
            "transactionreference": {"humanString": "Reference", "active": True},
            "requesttypedescription": {"humanString": "Request type", "active": True},
            "accounttypedescription": {"humanString": "Account type", "active": True},
            "settlestatus": {"humanString": "Settle status", "active": True},
            "baseamount": {"humanString": "Amount", "active": True},
            "paymenttypedescription": {"humanString": "Payment type", "active": True},
            "maskedpan": {"humanString": "Card number", "active": True},
            "billingfirstname": {"humanString": "First name", "active": True},
            "billinglastname": {"humanString": "Last name", "active": True},
            "merchantname": {"humanString": "Merchant name", "active": True},
            "sitereference": {"humanString": "Site reference", "active": True},
            "operatorname": {"humanString": "Operator", "active": True},
        })

        self.FIELDS = OrderedDict({
            "accounttypedescription": {
                "val": lambda string: not not re.fullmatch("(ECOM|MOTO|RECUR)", string),
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK
            },
            "billingemail": {
                "val": validateEmail,
                "inc": QUERY | CUSTOM,
                "req": NONE
            },
            "billingfirstname": {
                "inc": QUERY | CUSTOM,
                "req": NONE
            },
            "billinglastname": {
                "inc": QUERY | CUSTOM,
                "req": NONE
            },
            "billingpostcode": {
                "inc": QUERY | CUSTOM,
                "req": NONE
            },
            "billingpremise": {
                "inc": QUERY | CUSTOM,
                "req": NONE
            },
            "billingstreet": {
                "inc": QUERY | CUSTOM,
                "req": NONE
            },
            "currencyiso3a": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK
            },
            "customerip": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "val": validateIP
            },
            "orderreference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": NONE
            },
            "pan": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK
            },
            "parenttransactionreference": {
                "inc": QUERY | AUTH | REFUND | CUSTOM,
                "req": REFUND
            },
            "paymenttypedescriptions": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE
            },
            "requesttypedescriptions": {
                "inc": AUTH | REFUND | UPDATE | CHECK | CUSTOM,
                "req": CUSTOM  # technically every request requires this, but the controller adds it to the other types
            },
            "requesttypedescription": {
                "inc": QUERY,
                "req": NONE
            },
            "sitereference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": AUTH | REFUND | UPDATE | CHECK
            },
            "transactionreference": {
                "inc": QUERY | UPDATE | CUSTOM,
                "req": UPDATE
            },
            "authmethod": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "credentialsonfile": {
                "inc": AUTH | CHECK | CUSTOM,
                "req": NONE
            },
            "initiationreason": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "baseamount": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK
            },
            "expirydate": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK
            },
            "securitycode": {
                "inc": AUTH | CUSTOM,
                "req": AUTH | CHECK
            },
            "chargedescription": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": NONE
            },
            "merchantemail": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "operatorname": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customerstreet": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customertown": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customercounty": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customercountryiso2a": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customerpostcode": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customeremail": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customertelephonetype": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customertelephone": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customerprefixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customerfirstname": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customermiddlename": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customerlastname": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customersuffixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "customerforwardedip": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "val": validateIP
            },
            "settleduedate": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
            },
            "settlestatus": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
            },
            "settlebaseamount": {
                "inc": UPDATE | CUSTOM,
                "req": NONE,
            }
        })

        self.INSTRUCTIONS = {
            RequestType.TRANSACTIONQUERY: """Select a start and end date for the period you wish to query.
                Click 'New field' to add a row containing a dropdown and input box to specify cfg.FIELDS to filter by. 
                To add multiple values for the same filter, separate the values with commas.""",
            RequestType.REFUND: """Enter the details of the transaction you wish to refund.
                Only AUTHS that have settled (settlestatus=100) can be refunded.""",
            RequestType.CUSTOM: """Click 'New field' to add a row containing a dropdown and input box to enter a value for the field.
                When submitting you must ensure the cfg.FIELDS and values follow the specification for the requesttype as shown 
                in the docs. 
                To add multiple values for the same field, separate the values with commas.""",
            RequestType.AUTH: """All the initial fields are required and cannot be empty, unless using a saved card.
                New field adds extra fields to the request.""",
            RequestType.ACCOUNTCHECK: """The card entered below will not be charged, but will be saved on the gateway
                for future use, requiring only the securitycode and transactionreference of this as parent.
                All the initial fields are required and cannot be empty.
                New field adds extra fields to the request.""",
        }

    def toggleHeader(self, header: str):
        try:
            self.HEADERS[header]["active"] = not self.HEADERS[header]["active"]
        except KeyError as e:
            log.error(f"Header label {e} does not exist")

    def runValidation(self, field, value):
        result = False
        try:
            result = self.FIELDS[field]["val"](value)
        except KeyError as ke:
            result = True
        return result
