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
        self.FIELDS = OrderedDict({
            "accounttypedescription": {
                "val": lambda string: not not re.fullmatch("(ECOM|MOTO|RECUR)", string),
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Account",
                "activeInTransactionTableHeader": True
            },
            "billingemail": {
                "val": validateEmail,
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "E-mail",
                "activeInTransactionTableHeader": False
            },
            "billingfirstname": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "First name",
                "activeInTransactionTableHeader": False
            },
            "billinglastname": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Last name",
                "activeInTransactionTableHeader": False
            },
            "billingpostcode": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Postcode",
                "activeInTransactionTableHeader": False
            },
            "billingpremise": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Premise",
                "activeInTransactionTableHeader": False
            },
            "billingstreet": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Street",
                "activeInTransactionTableHeader": False
            },
            "currencyiso3a": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Currency",
                "activeInTransactionTableHeader": False
            },
            "customerip": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Customer IP",
                "activeInTransactionTableHeader": False,
                "val": validateIP
            },
            "orderreference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Order ref.",
                "activeInTransactionTableHeader": False
            },
            "maskedpan": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Card number",
                "activeInTransactionTableHeader": True
            },
            "parenttransactionreference": {
                "inc": QUERY | AUTH | REFUND | CUSTOM,
                "req": REFUND,
                "humanString": "Parent ref.",
                "activeInTransactionTableHeader": False
            },
            "paymenttypedescriptions": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Payment type",
                "activeInTransactionTableHeader": False
            },
            "paymenttypedescription": {
                "inc": QUERY,
                "req": NONE,
                "humanString": "Payment type",
                "activeInTransactionTableHeader": True
            },
            "requesttypedescriptions": {
                "inc": AUTH | REFUND | UPDATE | CHECK | CUSTOM,
                "req": CUSTOM,  # technically every request requires this, but the controller adds it to the other types
                "humanString": "Request types",
                "activeInTransactionTableHeader": False
            },
            "requesttypedescription": {
                "inc": QUERY,
                "req": NONE,
                "humanString": "Request type",
                "activeInTransactionTableHeader": True
            },
            "sitereference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": AUTH | REFUND | UPDATE | CHECK,
                "humanString": "Site ref.",
                "activeInTransactionTableHeader": True
            },
            "transactionreference": {
                "inc": QUERY | UPDATE | CUSTOM,
                "req": UPDATE,
                "humanString": "Reference",
                "activeInTransactionTableHeader": True
            },
            "authmethod": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Auth method",
                "activeInTransactionTableHeader": False
            },
            "credentialsonfile": {
                "inc": AUTH | CHECK | CUSTOM,
                "req": NONE,
                "humanString": "Tokenised?",
                "activeInTransactionTableHeader": False
            },
            "initiationreason": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Init. reason",
                "activeInTransactionTableHeader": False
            },
            "baseamount": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Amount",
                "activeInTransactionTableHeader": True
            },
            "expirydate": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Expiry",
                "activeInTransactionTableHeader": False
            },
            "securitycode": {
                "inc": AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "CVV",
                "activeInTransactionTableHeader": False
            },
            "chargedescription": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": NONE,
                "humanString": "Charge desc.",
                "activeInTransactionTableHeader": False
            },
            "merchantemail": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Merchant email",
                "activeInTransactionTableHeader": False
            },
            "operatorname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Operator name",
                "activeInTransactionTableHeader": True
            },
            "customerstreet": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. street",
                "activeInTransactionTableHeader": False
            },
            "customertown": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. town",
                "activeInTransactionTableHeader": False
            },
            "customercounty": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. country",
                "activeInTransactionTableHeader": False
            },
            "customercountryiso2a": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. country",
                "activeInTransactionTableHeader": False
            },
            "customerpostcode": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. postcode",
                "activeInTransactionTableHeader": False
            },
            "customeremail": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. email",
                "activeInTransactionTableHeader": False
            },
            "customertelephonetype": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. tel. type",
                "activeInTransactionTableHeader": False
            },
            "customertelephone": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust telephone no.",
                "activeInTransactionTableHeader": False
            },
            "customerprefixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. prefix",
                "activeInTransactionTableHeader": False
            },
            "customerfirstname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. first name",
                "activeInTransactionTableHeader": False
            },
            "customermiddlename": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. middle name",
                "activeInTransactionTableHeader": False
            },
            "customerlastname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. last name",
                "activeInTransactionTableHeader": False
            },
            "customersuffixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. suffix",
                "activeInTransactionTableHeader": False
            },
            "customerforwardedip": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. forwarded IP",
                "activeInTransactionTableHeader": False,
                "val": validateIP
            },
            "settleduedate": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle due date",
                "activeInTransactionTableHeader": False
            },
            "settlestatus": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle status",
                "activeInTransactionTableHeader": True
            },
            "settlebaseamount": {
                "inc": UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle base amount",
                "activeInTransactionTableHeader": False
            },
            "transactionstartedtimestamp": {
                "inc": NONE,
                "req": NONE,
                "humanString": "Transaction started",
                "activeInTransactionTableHeader": True
            },

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
