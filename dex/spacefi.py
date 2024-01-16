import json as js
import time
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from utils.client import Client
from .contracts import *


class SpaceFi(Client):

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        super().__init__(private_key, web3, chain_id, log, target_price_impact)
        self.router = SPACEFI_CONTRACT[self.chain_id]["router"]
        self.router_abi = js.load(open("abi/spacefi.json"))
        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.router_abi)

    def buy_token(self, token_name, token_hash, balance_percent, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Обмениваю ETH на {token_name}')
        try:
            balance = self.web3.eth.get_balance(self.wallet_address)
            amount = int(balance * (balance_percent / 100))
            if amount <= 0:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Недостаточно средств')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_token(token_name, token_hash, balance_percent, retry)
            amount_out = self.router_contract.functions.getAmountsOut(amount, [self.eth, token_hash]).call()[1]
            min_amount_out = int(amount_out * (1 - (SLIPPAGE / 100)))
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Проверяю price impact')
            self.price_impact_defender("ETH", amount, token_name, min_amount_out, self.target_price_impact)
            bought_amount = round(Web3.from_wei(min_amount_out, "picoether"), 3)
            contract_tx = self.router_contract.functions.swapETHForExactTokens(
                min_amount_out,
                [self.eth, token_hash],
                self.wallet_address,
                (int(time.time()) + 1800)
            ).build_transaction(self.prepare_transaction(amount))
            contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
            signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Куплено минимум {bought_amount} '
                              f'{token_name} | Хэш транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_token(token_name, token_hash, balance_percent, retry)
            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

    def sell_token(self, token_name, token_hash, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Обмениваю {token_name} на ETH')
        try:
            token_contract = self.web3.eth.contract(address=token_hash, abi=self.token_abi)
            token_balance = token_contract.functions.balanceOf(self.wallet_address).call()
            if token_balance == 0:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Баланс {token_name} - 0')
                retry += 1
                if retry > 3:
                    return False
                return self.sell_token(token_name, token_hash, retry)
            amount_out = self.router_contract.functions.getAmountsOut(token_balance, [token_hash, self.eth]).call()[1]
            min_amount_out = int(amount_out * (1 - (SLIPPAGE / 100)))
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Проверяю price impact')
            self.price_impact_defender(token_name, token_balance, "ETH", min_amount_out, self.target_price_impact)
            bought_amount = round(Web3.from_wei(token_balance, "picoether"), 3)
            decimal = token_contract.functions.decimals().call()
            allowance = token_contract.functions.allowance(self.wallet_address, self.router).call()
            if allowance < 100000 * 10 ** decimal:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Делаю approve')
                if self.approve(token_hash, self.router):
                    approved = True
                    time.sleep(5)
                else:
                    approved = False
            else:
                approved = True
            if approved:
                contract_tx = self.router_contract.functions.swapExactTokensForETH(
                    token_balance,
                    min_amount_out,
                    [token_hash, self.eth],
                    self.wallet_address,
                    (int(time.time()) + 1800)
                ).build_transaction(self.prepare_transaction())
                contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
                signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Отправил транзакцию')
                tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
                if tx_receipt.status == 1:
                    hash_ = str(tx_hash.hex())
                    self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Продано {bought_amount} '
                                  f'{token_name} | Хэш транзакции: {hash_}')
                else:
                    self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Транзакция не прошла')
                    retry += 1
                    if retry > 3:
                        return False
                    return self.sell_token(token_name, token_hash, retry)
                return True
            return False

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SpaceFi | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)
