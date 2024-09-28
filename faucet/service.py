from web3 import Web3
from faucet_task.settings import node_url

from faucet_task import settings

from .models import Transaction
from .repository import FaucetRepository


class FaucetService:
    def __init__(self):
        self._repository = FaucetRepository()
        self._web3 = Web3(Web3.HTTPProvider(node_url))

        self.PRIVATE_KEY: str = settings.private_key
        self.SOURCE_WALLET: str = settings.source_wallet
        self.FAUCET_AMOUNT = 0.0001
        self.CHAIN_ID = 11155111

    def fund_account(self, wallet_address: str) -> str:
        nonce = self._web3.eth.get_transaction_count(self.SOURCE_WALLET)
        sending_amount_converted = self._web3.to_wei(self.FAUCET_AMOUNT, "ether")
        gas_estimate = self._web3.eth.estimate_gas(
            {
                "from": self.SOURCE_WALLET,
                "to": wallet_address,
                "value": sending_amount_converted,
            }
        )
        gas_price = self._web3.eth.gas_price
        tx = {
            "chainId": self.CHAIN_ID,
            "nonce": nonce,
            "to": wallet_address,
            "value": sending_amount_converted,
            "gas": gas_estimate,
            "gasPrice": gas_price,
        }

        signed_tx = self._web3.eth.account.sign_transaction(tx, self.PRIVATE_KEY)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_id = self._web3.to_hex(tx_hash)

        self._repository.create_transaction(
            wallet_address=wallet_address, tx_id=tx_id, status="success"
        )

        return tx_id

    def create_error_transaction(self, wallet_address: str, error: str) -> Transaction:
        return self._repository.create_transaction(
            wallet_address=wallet_address, status=f"failed:{error}"
        )

    def get_transaction_stats(self) -> tuple[int, int]:
        return self._repository.get_transaction_stats()
