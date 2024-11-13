from typing import Optional
from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2
from pytoniq_core import Cell, StateInit

from config import TONAPI_KEY, MNEMONIC_PHRASE, IS_MAINNET


class BignoWallet:

    def __init__(self):
        self.client = TonapiClient(
            api_key=TONAPI_KEY, is_testnet=not IS_MAINNET)
        wallet, _, _, _ = WalletV4R2.from_mnemonic(
            self.client, MNEMONIC_PHRASE)
        self.wallet = wallet

    async def send_transfer(self, to: str, amount: float, msg_body: Optional[Cell] = None, state_init: Optional[Cell] = None):
        hash = await self.wallet.transfer(destination=to, amount=amount, body=msg_body, state_init=StateInit.deserialize(state_init.begin_parse()) if state_init else None)
        return hash
