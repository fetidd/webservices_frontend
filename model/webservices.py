import securetrading
from lib.logger import createLogger
import datetime

log = createLogger(__name__)


class Webservices:
    def __init__(self):
        self.st = None
        self.loggedIn = False

    def login(self, username, password):
        """
        Attempt to log in to Webservices by verifying credentials with a TRANSACTIONQUERY.
        Returns a GatewayResponse containing today's transactions, and sets the Webservices st property.
        Throws an InvalidCredentials exception if an error is returned from the gateway.
        """
        log.debug(f"Logging in with {username}:{password}")
        config = securetrading.Config()
        config.username = username
        config.password = password
        self.st = securetrading.Api(config)
        request = {
            "requesttypedescriptions": ["TRANSACTIONQUERY"],
            "filter": {
                "starttimestamp": [{"value": str(datetime.datetime.now().date()) + " 00:00:00"}],
                "endtimestamp": [{"value": str(datetime.datetime.now().date()) + " 23:59:59"}],
                "requesttypedescription": [
                    {"value": "AUTH"}, {"value": "REFUND"}, {"value": "THREEDQUERY"}
                ]
            }
        }
        response = self.makeRequest(request)["responses"][0]
        if response["errorcode"] == '0':
            log.debug("Login successful!")
            self.loggedIn = True
            return response
        else:
            errString = f"[{response['errorcode']}] {response['errormessage']} {response['errordata']}"
            log.error(errString)
            raise Exception(errString)

    def makeRequest(self, request: dict) -> dict:
        log.debug("Making a new request:")
        log.debug("\t--> " + str(request))
        isMultiRequest = True if len(request["requesttypedescriptions"]) > 1 else False
        # Send request to Trust Payments Webservices API
        response = self._send(request)
        log.debug("\t<-- " + str(response))
        return response

    # PRIVATE METHODS --------------------------------------------------------------------
    def _send(self, request: dict) -> dict:
        strequest = securetrading.Request()
        strequest.update(request)
        stresponse = self.st.process(strequest)
        return stresponse
