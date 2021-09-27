from lib.logger import createLogger

log = createLogger(__name__)


class TransactionStore:
    def __init__(self):
        self._data = {}

    def add(self, transactions: list):
        log.debug(f"Added:")
        for t in transactions:
            log.debug("\t<-- " + str(t))
            self._data[t["transactionreference"]] = t

    def get(self, ref) -> dict:
        log.debug(f"Gave:")
        transaction = self._data.get(ref, None)
        log.debug(f"\t--> " + str(transaction))
        return transaction

    def getAll(self) -> list:
        transactions = list(self._data.values())
        log.debug(f"Gave:")
        for t in transactions:
            log.debug(f"\t--> " + str(t))
        return transactions
