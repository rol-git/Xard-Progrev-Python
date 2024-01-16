import json as js
import time
from eth_abi import encode
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from utils.client import Client
from .contracts import *


class SyncSwap(Client):

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        super().__init__(private_key, web3, chain_id, log, target_price_impact)
        self.router = SYNCSWAP_CONTRACT[self.chain_id]["router"]
        self.get_pool_address = SYNCSWAP_CONTRACT[self.chain_id]["pool"]
        self.router_abi = js.load(open("abi/syncswap_router.json"))
        self.pool_abi = js.load(open("abi/syncswap_pool.json"))
        self.get_pool_abi = js.load(open("abi/syncswap_get_pool.json"))
        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.router_abi)
        self.get_pool_contract = self.web3.eth.contract(address=self.get_pool_address, abi=self.get_pool_abi)

    def buy_token(self, token_name, token_hash, balance_percent, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Обмениваю ETH на {token_name}')
        try:
            balance = self.web3.eth.get_balance(self.wallet_address)
            amount = int(balance * (balance_percent / 100))
            if amount <= 0:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Недостаточно средств')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_token(token_name, token_hash, balance_percent, retry)
            pool_address = self.get_pool_contract.functions.getPool(self.eth, token_hash).call()
            contract_pool = self.web3.eth.contract(address=pool_address, abi=self.pool_abi)
            reserves = contract_pool.functions.getReserves().call()
            token_contract = self.web3.eth.contract(address=token_hash, abi=self.token_abi)
            decimal = token_contract.functions.decimals().call()
            data = encode(["address", "address", "uint8"], [self.eth, self.wallet_address, 1])
            zero_address = "0x0000000000000000000000000000000000000000"
            steps = [
                {
                    "pool": pool_address,
                    "data": data,
                    "callback": zero_address,
                    "callbackData": "0x"
                }
            ]
            [reserves_usdc, reserves_eth] = reserves
            reserves_usdc = reserves_usdc / 10e6
            reserves_eth = reserves_eth / 10e18
            price_one_token = reserves_eth / reserves_usdc
            min_amount_out = int(float(Web3.from_wei(amount, "ether")) / price_one_token * (1 - (SLIPPAGE / 100))
                                 * 10 ** decimal)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Проверяю price impact')
            self.price_impact_defender("ETH", amount, token_name, min_amount_out, self.target_price_impact)
            bought_amount = round(Web3.from_wei(min_amount_out, "picoether"), 3)
            paths = [
                {
                    "steps": steps,
                    "tokenIn": zero_address,
                    "amountIn": amount
                }
            ]
            contract_tx = self.router_contract.functions.swap(
                paths,
                min_amount_out,
                (int(time.time()) + 1800)
            ).build_transaction(self.prepare_transaction(amount))
            contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
            signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Куплено минимум {bought_amount} '
                              f'{token_name} | Хэш транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_token(token_name, token_hash, balance_percent, retry)
            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

    def sell_token(self, token_name, token_hash, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Обмениваю {token_name} на ETH')
        try:
            token_contract = self.web3.eth.contract(address=token_hash, abi=self.token_abi)
            decimal = token_contract.functions.decimals().call()
            token_balance = token_contract.functions.balanceOf(self.wallet_address).call()
            if token_balance == 0:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Баланс {token_name} - 0')
                retry += 1
                if retry > 3:
                    return False
                return self.sell_token(token_name, token_hash, retry)
            pool_address = self.get_pool_contract.functions.getPool(token_hash, self.eth).call()
            contract_pool = self.web3.eth.contract(address=pool_address, abi=self.pool_abi)
            reserves = contract_pool.functions.getReserves().call()
            data = encode(["address", "address", "uint8"], [token_hash, self.wallet_address, 1])
            zero_address = "0x0000000000000000000000000000000000000000"
            steps = [
                {
                    "pool": pool_address,
                    "data": data,
                    "callback": zero_address,
                    "callbackData": "0x"
                }
            ]
            [reserves_token, reserves_eth] = reserves
            reserves_token = reserves_token / 10e6
            reserves_eth = reserves_eth / 10e18
            price_one_token = reserves_token / reserves_eth
            min_amount_out = Web3.to_wei(float(token_balance / 10 ** decimal) / price_one_token *
                                         (1 - (SLIPPAGE / 100)), "ether")
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Проверяю price impact')
            self.price_impact_defender(token_name, token_balance, "ETH", min_amount_out, self.target_price_impact)
            paths = [
                {
                    "steps": steps,
                    "tokenIn": token_hash,
                    "amountIn": token_balance
                }
            ]
            bought_amount = round(Web3.from_wei(token_balance, "picoether"), 3)
            allowance = token_contract.functions.allowance(self.wallet_address, self.router).call()
            if allowance < 1000000 * 10 ** decimal:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Делаю approve')
                if self.approve(token_hash, self.router):
                    approved = True
                    time.sleep(5)
                else:
                    approved = False
            else:
                approved = True
            if approved:
                contract_tx = self.router_contract.functions.swap(
                    paths,
                    min_amount_out,
                    (int(time.time()) + 1800)
                ).build_transaction(self.prepare_transaction())
                contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
                signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Отправил транзакцию')
                tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
                if tx_receipt.status == 1:
                    hash_ = str(tx_hash.hex())
                    self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Продано {bought_amount} '
                                  f'{token_name} | Хэш транзакции: {hash_}')
                else:
                    self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Транзакция не прошла')
                    retry += 1
                    if retry > 3:
                        return False
                    return self.sell_token(token_name, token_hash, retry)
                return True
            return False

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | SyncSwap | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)
