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


class Config:
    def __init__(self):
        self.HEADERS = OrderedDict({
            "Transaction started": {"apiField": "transactionstartedtimestamp", "active": True},
            "Reference": {"apiField": "transactionreference", "active": True},
            "Request type": {"apiField": "requesttypedescription", "active": True},
            "Account type": {"apiField": "accounttypedescription", "active": True},
            "Settle status": {"apiField": "settlestatus", "active": True},
            "Amount": {"apiField": "baseamount", "active": True},
            "Payment type": {"apiField": "paymenttypedescription", "active": True},
            "Card number": {"apiField": "maskedpan", "active": True},
            "First name": {"apiField": "billingfirstname", "active": True},
            "Last name": {"apiField": "billinglastname", "active": True},
            "Merchant name": {"apiField": "merchantname", "active": True},
            "Site reference": {"apiField": "sitereference", "active": True},
            "Operator": {"apiField": "operatorname", "active": True},
        })
        self.FIELDS = OrderedDict({
            "accounttypedescription": {
                "val": lambda string: not not re.fullmatch("(ECOM|MOTO|RECUR)", string),
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH
            },
            "billingemail": {
                "val": self.validateEmail,
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
                "req": AUTH
            },
            "customerip": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "val": self.validateIP
            },
            "orderreference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": NONE
            },
            "pan": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH,
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
                "req": AUTH | REFUND | UPDATE | CHECK
            },
            "requesttypedescription": {
                "inc": QUERY,
                "req": NONE
            },
            "sitereference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": AUTH | REFUND | UPDATE
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
                "req": CHECK
            },
            "initiationreason": {
                "inc": AUTH | CUSTOM,
                "req": NONE
            },
            "baseamount": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH
            },
            "expirydate": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH
            },
            "securitycode": {
                "inc": AUTH | CUSTOM,
                "req": NONE | AUTH
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
                "val": self.validateIP
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
            RequestType.TRANSACTIONQUERY: """
        Select a start and end date for the period you wish to query.
        Click 'New field' to add a row containing a dropdown and input box to specify cfg.FIELDS to filter by. 
        To add multiple values for the same filter, separate the values with commas.
        """,
            RequestType.REFUND: """
            Enter the details of the transaction you wish to refund.
            Only AUTHS that have settled (settlestatus=100) can be refunded.
            """,
            RequestType.CUSTOM: """
        Click 'New field' to add a row containing a dropdown and input box to enter a value for the field.
        When submitting you must ensure the cfg.FIELDS and values follow the specification for the requesttype as shown 
        in the docs. 
        To add multiple values for the same field, separate the values with commas.
        """,
            RequestType.AUTH: "",
            RequestType.ACCOUNTCHECK: "",

        }

    def toggleHeader(self, header: str):
        try:
            self.HEADERS[header]["active"] = not self.HEADERS[header]["active"]
        except Exception as e:
            log.error("Header label does not exist")

    def runValidation(self, field, value):
        result = False
        try:
            result = self.FIELDS[field]["val"](value)
        except KeyError as ke:
            result = True
        return result

    def validateEmail(self, email):
        return not not re.fullmatch("[^@]+@[a-z]+\.[a-z]+", email)


    def validateIP(self, ip):
        return not not re.fullmatch("([0-9]{1,3}\.){3}[0-9]{1,3}", ip)
