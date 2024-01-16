from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from utils.client import Client
from .contracts import *


class Grape(Client):

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        super().__init__(private_key, web3, chain_id, log, target_price_impact)
        self.contract = GRAPE_CONTRACT[self.chain_id]["router"]

    def buy_tickets(self, tickets_amount, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Покупаю билеты ({tickets_amount})')
        try:
            hex_value = hex(tickets_amount)[2:]
            n = 64 - len(str(hex_value))
            data = "0x7a183e84" + "0" * n + str(hex_value)
            tx = {
                "data": data,
                "to": self.contract,
            }
            tx = self.prepare_transaction(Web3.to_wei(0.0001 * tickets_amount, "ether")) | tx
            tx["gas"] = self.web3.eth.estimate_gas(tx)
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Билеты ({tickets_amount}) куплены '
                              f'успешно | Хэш транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_tickets(tickets_amount, retry)
            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.buy_tickets(tickets_amount, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.buy_tickets(tickets_amount, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Grape | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.buy_tickets(tickets_amount, retry)
