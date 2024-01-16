import json as js
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from hashlib import sha256
import random
from faker import Faker
from mnemonic import Mnemonic
from utils.client import Client
from .contracts import *


class Dmail(Client):

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        super().__init__(private_key, web3, chain_id, log, target_price_impact)
        self.router = DMAIL_CONTRACT[self.chain_id]["router"]
        self.router_abi = js.load(open("abi/dmail.json"))
        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.router_abi)

    @staticmethod
    def generate_email():
        return f'{Faker().word()}{random.randint(1, 999999)}@' \
               f'{random.choice(["gmail.com", "yahoo.com", "outlook.com", "icloud.com", "yandex.ru", "mail.com"])}'

    @staticmethod
    def generate_sentence():
        mnemo = Mnemonic("english")

        return mnemo.generate(256)

    def send_message(self, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Отправляю письмо')
        try:
            email = self.generate_email()
            text = self.generate_sentence()
            to_address = sha256(f'{email}'.encode()).hexdigest()
            message = sha256(f'{text}'.encode()).hexdigest()
            contract_tx = self.router_contract.functions.send_mail(
                to_address,
                message,
            ).build_transaction(self.prepare_transaction())
            contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
            signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Письмо отправлено успешно | Хэш '
                              f'транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.send_message(retry)

            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.send_message(retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.send_message(retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Dmail | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.send_message(retry)
