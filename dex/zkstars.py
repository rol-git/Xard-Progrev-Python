import random
import json as js
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from utils.client import Client
from .contracts import *


class ZkStars(Client):

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        super().__init__(private_key, web3, chain_id, log, target_price_impact)
        self.contract_abi = js.load(open("abi/zkstars.json"))

    def mint_nft(self, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Делаю минт nft')
        try:
            nft_id, nft_address = random.choice(list(ZKSTARS_NFT[self.chain_id].items()))
            contract = self.web3.eth.contract(address=nft_address, abi=self.contract_abi)
            mint_price_in_wei = contract.functions.getPrice().call()
            contract_tx = contract.functions.safeMint(
                "0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5"
            ).build_transaction(self.prepare_transaction(mint_price_in_wei))
            contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
            signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Минт nft прошел успешно | Хэш '
                              f'транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.mint_nft(retry)
            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.mint_nft(retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.mint_nft(retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | ZkStars | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.mint_nft(retry)
