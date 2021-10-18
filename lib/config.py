"""
Configuration class.

FIELDS:
    Key: the field name the gateway expects
        val: A function used to validate the value in the input (optional)
        inc: A bitmask to show which requests this is a field for
        req: A bitmask to show which requests this field is required for
        humanString: a nicer string to use in headers etc.
        isActive: bool toggle for whether the field is a header in main table
        position: 0-indexed position for the header in the main table (should be None if activeInTransaction... is False)
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
        self.FIELDS = OrderedDict({
            "accounttypedescription": {
                "val": self.validateAccountType,
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Account",
                "isActive": False,
                "position": None
            },
            "billingemail": {
                "val": self.validateEmail,
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "E-mail",
                "isActive": False,
                "position": None
            },
            "billingfirstname": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "First name",
                "isActive": False,
                "position": None
            },
            "billinglastname": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Last name",
                "isActive": False,
                "position": None
            },
            "billingpostcode": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Postcode",
                "isActive": False,
                "position": None
            },
            "billingpremise": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Premise",
                "isActive": False,
                "position": None
            },
            "billingstreet": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Street",
                "isActive": False,
                "position": None
            },
            "currencyiso3a": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Currency",
                "isActive": False,
                "position": None
            },
            "customerip": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Customer IP",
                "isActive": False,
                "val": self.validateIP,
                "position": None
            },
            "orderreference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Order ref.",
                "isActive": False,
                "position": None
            },
            "pan": {
                "inc": AUTH | CHECK | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Card number",
                "isActive": False,
                "position": None
            },
            "maskedpan": {
                "inc": QUERY | CUSTOM,
                "req": NONE,
                "humanString": "Card number",
                "isActive": False,
                "position": None
            },
            "parenttransactionreference": {
                "inc": QUERY | AUTH | REFUND | CUSTOM,
                "req": REFUND,
                "humanString": "Parent ref.",
                "isActive": False,
                "position": None
            },
            "paymenttypedescriptions": {
                "inc": QUERY | AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Payment type",
                "isActive": False,
                "position": None
            },
            "paymenttypedescription": {
                "inc": QUERY,
                "req": NONE,
                "humanString": "Payment type",
                "isActive": False,
                "position": None
            },
            "requesttypedescriptions": {
                "inc": AUTH | REFUND | UPDATE | CHECK | CUSTOM,
                "req": CUSTOM,  # technically every request requires this, but the controller adds it to the other types
                "humanString": "Request types",
                "isActive": False,
                "position": None
            },
            "requesttypedescription": {
                "inc": QUERY,
                "req": NONE,
                "humanString": "Request type",
                "isActive": False,
                "position": None
            },
            "sitereference": {
                "inc": QUERY | AUTH | REFUND | UPDATE | CUSTOM,
                "req": AUTH | REFUND | UPDATE | CHECK,
                "humanString": "Site ref.",
                "isActive": False,
                "position": None
            },
            "transactionreference": {
                "inc": QUERY | UPDATE | CUSTOM,
                "req": UPDATE,
                "humanString": "Reference",
                "isActive": False,
                "position": None
            },
            "authmethod": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Auth method",
                "isActive": False,
                "position": None
            },
            "credentialsonfile": {
                "inc": AUTH | CHECK | CUSTOM,
                "req": NONE,
                "humanString": "Tokenised?",
                "isActive": False,
                "position": None
            },
            "initiationreason": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Init. reason",
                "isActive": False,
                "position": None
            },
            "baseamount": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Amount",
                "isActive": False,
                "position": None
            },
            "expirydate": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "Expiry",
                "isActive": False,
                "position": None
            },
            "securitycode": {
                "inc": AUTH | CUSTOM,
                "req": AUTH | CHECK,
                "humanString": "CVV",
                "isActive": False,
                "position": None
            },
            "chargedescription": {
                "inc": AUTH | REFUND | CUSTOM,
                "req": NONE,
                "humanString": "Charge desc.",
                "isActive": False,
                "position": None
            },
            "merchantemail": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Merchant email",
                "isActive": False,
                "position": None
            },
            "operatorname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Operator name",
                "isActive": False,
                "position": None
            },
            "customerstreet": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. street",
                "isActive": False,
                "position": None
            },
            "customertown": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. town",
                "isActive": False,
                "position": None
            },
            "customercounty": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. country",
                "isActive": False,
                "position": None
            },
            "customercountryiso2a": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. country",
                "isActive": False,
                "position": None
            },
            "customerpostcode": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. postcode",
                "isActive": False,
                "position": None
            },
            "customeremail": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. email",
                "isActive": False,
                "position": None
            },
            "customertelephonetype": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. tel. type",
                "isActive": False,
                "position": None
            },
            "customertelephone": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust telephone no.",
                "isActive": False,
                "position": None
            },
            "customerprefixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. prefix",
                "isActive": False,
                "position": None
            },
            "customerfirstname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. first name",
                "isActive": False,
                "position": None
            },
            "customermiddlename": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. middle name",
                "isActive": False,
                "position": None
            },
            "customerlastname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. last name",
                "isActive": False,
                "position": None
            },
            "customersuffixname": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. suffix",
                "isActive": False,
                "position": None
            },
            "customerforwardedip": {
                "inc": AUTH | CUSTOM,
                "req": NONE,
                "humanString": "Cust. forwarded IP",
                "isActive": False,
                "val": self.validateIP,
                "position": None
            },
            "settleduedate": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle due date",
                "isActive": False,
                "position": None
            },
            "settlestatus": {
                "inc": AUTH | UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle status",
                "isActive": True,
                "position": 1
            },
            "settlebaseamount": {
                "inc": UPDATE | CUSTOM,
                "req": NONE,
                "humanString": "Settle base amount",
                "isActive": False,
                "position": None
            },
            "transactionstartedtimestamp": {
                "inc": NONE,
                "req": NONE,
                "humanString": "Transaction started",
                "isActive": True,
                "position": 0
            },

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
            result = False
        return result

    def validateEmail(self, email):
        return not not re.fullmatch("[^@]+@[a-z]+\.[a-z]+", email)

    def validateIP(self, ip):
        return not not re.fullmatch("([0-9]{1,3}\.){3}[0-9]{1,3}", ip)

    def validateAccountType(self, acct):
        return not not re.fullmatch("(ECOM|MOTO|RECUR)", acct)
