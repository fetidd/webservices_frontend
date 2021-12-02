"""
Configuration class.

FIELDS:
    Key: the field name the gateway expects
        val: A function used to validate the value in the input (optional)
        inc: A bitmask to show which requests this is a field for
        req: A bitmask to show which requests this field is required for
        humanString: a nicer string to use in headers etc.
        activeInTransactionTableHeader: bool toggle for whether the field is a header in main table
        position: 0-indexed position for the header in the main table (should be 99 if activeInTransaction... is False)
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
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "billingemail": {
                "val": validateEmail,
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "E-mail",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "billingfirstname": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "First name",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "billinglastname": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Last name",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "billingpostcode": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Postcode",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "billingpremise": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Premise",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "billingstreet": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Street",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "currencyiso3a": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Currency",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customerip": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Customer IP",
                "activeInTransactionTableHeader": False,
                "val": validateIP,
                "position": 99
            },
            "orderreference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Order ref.",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "pan": {
                "inc": AUTH | CHECK | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Card number",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "maskedpan": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Card number",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "parenttransactionreference": {
                "inc": QUERY | AUTH | REFUND | CUSTOM,
                "req": REFUND,
                "humanString": "Parent ref.",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "paymenttypedescriptions": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Payment type",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "paymenttypedescription": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Payment type",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "requesttypedescriptions": {
                "inc": AUTH | REFUND | UPDATE | CHECK | CUSTOM,
                "req": CUSTOM,  # technically every request requires this, but the controller adds it to the other types
                "humanString": "Request types",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "requesttypedescription": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Request type",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "sitereference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": AUTH | REFUND | UPDATE | CHECK,
                "humanString": "Site ref.",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "transactionreference": {
                "inc": QUERY | UPDATE | CUSTOM,
                "req": UPDATE,
                "humanString": "Reference",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "authmethod": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Auth method",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "credentialsonfile": {
                "inc": AUTH | CHECK | CUSTOM,
                "req": NONE,
                "humanString": "Tokenised?",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "initiationreason": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Init. reason",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "baseamount": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Amount",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "expirydate": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Expiry",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "securitycode": {
                "inc": AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "CVV",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "chargedescription": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": NONE,
                "humanString": "Charge desc.",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "merchantemail": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Merchant email",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "operatorname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Operator name",
                "activeInTransactionTableHeader": True,
                "position": 99
            },
            "customerstreet": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. street",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customertown": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. town",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customercounty": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. country",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customercountryiso2a": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. country",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customerpostcode": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. postcode",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customeremail": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. email",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customertelephonetype": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. tel. type",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customertelephone": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust telephone no.",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customerprefixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. prefix",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customerfirstname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. first name",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customermiddlename": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. middle name",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customerlastname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. last name",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customersuffixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. suffix",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "customerforwardedip": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. forwarded IP",
                "activeInTransactionTableHeader": False,
                "val": validateIP,
                "position": 99
            },
            "settleduedate": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle due date",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "settlestatus": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle status",
                "activeInTransactionTableHeader": True,
                "position": 1
            },
            "settlebaseamount": {
                "inc": UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle base amount",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "transactionstartedtimestamp": {
                "inc": NONE,
                "req": NONE,
                "humanString": "Transaction started",
                "activeInTransactionTableHeader": True,
                "position": 0
            },
            "errorurlredirect": {
                "inc": CUSTOM,
                "req": NONE,
                "humanString": "ERROR_URL",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "successfulurlredirect": {
                "inc": CUSTOM,
                "req": NONE,
                "humanString": "SUCCESS_URL",
                "activeInTransactionTableHeader": False,
                "position": 99
            },
            "billingcountryiso2a": {
                "inc": CUSTOM,
                "req": NONE,
                "humanString": "BILLING_COUNTRY",
                "activeInTransactionTableHeader": False,
                "position": 99
            }

        })

        # TODO improve how instructions are displayed
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
                All the initial fields are required and cannot be empty.""",
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
