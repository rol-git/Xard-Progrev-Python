import json as js
import time
from requests import ConnectionError
from hexbytes import HexBytes
from web3.exceptions import TransactionNotFound
from utils.client import Client
from .contracts import *


class Izumi(Client):

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        super().__init__(private_key, web3, chain_id, log, target_price_impact)
        self.router = IZUMI_CONTRACT[self.chain_id]["router"]
        self.quoter = IZUMI_CONTRACT[self.chain_id]["quoter"]
        self.router_abi = js.load(open("abi/izumi_router.json"))
        self.quoter_abi = js.load(open("abi/izumi_quoter.json"))
        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.router_abi)
        self.quoter_contract = self.web3.eth.contract(address=self.quoter, abi=self.quoter_abi)

    @staticmethod
    def get_path(from_token_address, to_token_address, fee):
        from_token_bytes = HexBytes(from_token_address).rjust(20, b'\0')
        to_token_bytes = HexBytes(to_token_address).rjust(20, b'\0')
        fee_bytes = fee.to_bytes(3, "big")
        return from_token_bytes + fee_bytes + to_token_bytes

    @staticmethod
    def get_min_amount_out(quoter_contract, path, amount):
        min_amount, _ = quoter_contract.functions.swapAmount(
            amount,
            path
        ).call()
        return int(min_amount * (1 - (SLIPPAGE / 100)))

    def get_pool_fee(self, quoter_contract, from_token_address, to_token_address, fee=400):
        pool_address = quoter_contract.functions.pool(
            from_token_address,
            to_token_address,
            fee
        ).call()
        if pool_address != ZERO_ADDRESS:
            return fee
        return self.get_pool_fee(quoter_contract, from_token_address, to_token_address, 500)

    def buy_token(self, token_name, token_hash, balance_percent, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Обмениваю ETH на {token_name}')
        try:
            balance = self.web3.eth.get_balance(self.wallet_address)
            amount = int(balance * (balance_percent / 100))
            if amount <= 0:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Недостаточно средств')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_token(token_name, token_hash, balance_percent, retry)
            pool_fee = self.get_pool_fee(self.quoter_contract, self.eth, token_hash)
            path = self.get_path(str(self.eth), str(token_hash), pool_fee)
            min_amount_out = self.get_min_amount_out(self.quoter_contract, path, amount)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Проверяю price impact')
            self.price_impact_defender("ETH", amount, token_name, min_amount_out, self.target_price_impact)
            bought_amount = round(Web3.from_wei(min_amount_out, "picoether"), 3)
            contract_tx = self.router_contract.functions.multicall(
                [
                    self.router_contract.encodeABI(
                        fn_name="swapAmount",
                        args=[(
                            path,
                            self.wallet_address,
                            amount,
                            min_amount_out,
                            int(time.time()) + 1800
                        )]
                    ),
                    self.router_contract.encodeABI(
                        fn_name="refundETH"
                    )
                ]
            ).build_transaction(self.prepare_transaction(amount))
            contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
            signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Куплено минимум {bought_amount} '
                              f'{token_name} | Хэш транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.buy_token(token_name, token_hash, balance_percent, retry)
            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.buy_token(token_name, token_hash, balance_percent, retry)

    def sell_token(self, token_name, token_hash, retry=1):
        self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Обмениваю {token_name} на ETH')
        try:
            token_contract = self.web3.eth.contract(address=token_hash, abi=self.token_abi)
            token_balance = token_contract.functions.balanceOf(self.wallet_address).call()
            if token_balance == 0:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Баланс {token_name} - 0')
                retry += 1
                if retry > 3:
                    return False
                return self.sell_token(token_name, token_hash, retry)
            pool_fee = self.get_pool_fee(self.quoter_contract, token_hash, self.eth)
            path = self.get_path(token_hash, self.eth, pool_fee)
            min_amount_out = self.get_min_amount_out(self.quoter_contract, path, token_balance)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Проверяю price impact')
            self.price_impact_defender(token_name, token_balance, "ETH", min_amount_out, self.target_price_impact)
            bought_amount = round(Web3.from_wei(token_balance, "picoether"), 3)
            decimal = token_contract.functions.decimals().call()
            allowance = token_contract.functions.allowance(self.wallet_address, self.router).call()
            if allowance < 1000000 * 10 ** decimal:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Делаю approve')
                if self.approve(token_hash, self.router):
                    approved = True
                    time.sleep(5)
                else:
                    approved = False
            else:
                approved = True
            if approved:
                contract_tx = self.router_contract.functions.multicall(
                    [
                        self.router_contract.encodeABI(
                            fn_name="swapAmount",
                            args=[(
                                path,
                                ZERO_ADDRESS,
                                token_balance,
                                min_amount_out,
                                int(time.time()) + 1800
                            )]
                        ),
                        self.router_contract.encodeABI(
                            fn_name="unwrapWETH9",
                            args=[
                                min_amount_out,
                                self.wallet_address
                            ]
                        )
                    ]
                ).build_transaction(self.prepare_transaction())
                contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
                signed_tx = self.web3.eth.account.sign_transaction(contract_tx, private_key=self.private_key)
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Отправил транзакцию')
                tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
                if tx_receipt.status == 1:
                    hash_ = str(tx_hash.hex())
                    self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Продано {bought_amount} '
                                  f'{token_name} | Хэш транзакции: {hash_}')
                else:
                    self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Транзакция не прошла')
                    retry += 1
                    if retry > 3:
                        return False
                    return self.sell_token(token_name, token_hash, retry)
                return True
            return False

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Izumi | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.sell_token(token_name, token_hash, retry)
