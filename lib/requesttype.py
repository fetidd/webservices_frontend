from enum import Enum

class RequestType(Enum):
    NONE = 0
    TRANSACTIONQUERY = 1
    AUTH = 2
    REFUND = 4
    TRANSACTIONUPDATE = 8
    ACCOUNTCHECK = 16
    CUSTOM = 32