import json as js
import requests
from web3.exceptions import TransactionNotFound
from dex.contracts import *


class Client:

    def __init__(self, private_key, web3, chain_id, log, target_price_impact):
        self.private_key = private_key
        self.web3 = web3
        self.chain_id = chain_id
        self.log = log
        self.target_price_impact = target_price_impact
        self.wallet_address = self.web3.eth.account.from_key(private_key).address
        self.token_abi = js.load(open("abi/token.json"))
        self.chain_name = CHAIN_NAME[self.chain_id]
        self.eth = TOKENS[self.chain_id]["ETH"]

    def get_priority_fee(self):
        fee_history = self.web3.eth.fee_history(25, "latest", [20.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]
        divisor_priority = max(len(non_empty_block_priority_fees), 1)
        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))
        return priority_fee

    def prepare_transaction(self, value=0):
        tx_params = {
            "from": self.web3.to_checksum_address(self.wallet_address),
            "nonce": self.web3.eth.get_transaction_count(self.wallet_address),
            "value": value,
            "chainId": self.chain_id,
        }
        base_fee = int(self.web3.eth.gas_price * 1.1)
        max_priority_fee_per_gas = self.get_priority_fee()
        max_fee_per_gas = base_fee + max_priority_fee_per_gas
        tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        tx_params["maxFeePerGas"] = max_fee_per_gas
        tx_params["type"] = "0x2"
        return tx_params

    @staticmethod
    def get_token_price(token_name, vs_currency="usd"):
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {'ids': f'{token_name}', 'vs_currencies': f'{vs_currency}'}

        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return float(response.json()[token_name][vs_currency])
        else:
            raise RuntimeError(f'Не выполнен запрос к CoinGecko API: {response.status_code}')

    def price_impact_defender(self, from_token_name, from_token_amount_in_wei,
                              to_token_name, to_token_amount_in_wei, target_price_impact):
        from_token_amount = float(Web3.from_wei(from_token_amount_in_wei, "ether"))
        to_token_amount = float(Web3.from_wei(to_token_amount_in_wei, "picoether"))
        token_info = {
            "ETH": "ethereum",
            "USDC": "usd-coin",
            "USDbC": "bridged-usd-coin-base"
        }
        amount1_in_usd = (self.get_token_price(token_info[from_token_name])) * from_token_amount
        amount2_in_usd = (self.get_token_price(token_info[to_token_name])) * to_token_amount
        price_impact = 100 - (amount2_in_usd / amount1_in_usd) * 100
        if price_impact > target_price_impact:
            raise RuntimeError(f'Превышен установленный price impact: {(price_impact - SLIPPAGE):.3}% > '
                               f'{target_price_impact - SLIPPAGE}%')

    def approve(self, token_to_approve, address_to_approve, retry=0):
        try:
            token_contract = self.web3.eth.contract(address=token_to_approve, abi=self.token_abi)
            max_amount = Web3.to_wei(2 ** 64 - 1, "ether")
            contract_tx = token_contract.functions.approve(
                address_to_approve,
                max_amount
            ).build_transaction(self.prepare_transaction())
            contract_tx["gas"] = self.web3.eth.estimate_gas(contract_tx)
            signed_tx = self.web3.eth.account.sign_transaction(contract_tx, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Approve | Отправил транзакцию')
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            if tx_receipt.status == 1:
                hash_ = str(tx_hash.hex())
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Approve | Транзакция прошла успешно | Хэш '
                              f'транзакции: {hash_}')
            else:
                self.log.info(f'{self.chain_name} | {self.wallet_address} | Approve | Транзакция не прошла')
                retry += 1
                if retry > 3:
                    return False
                return self.approve(token_to_approve, address_to_approve, retry)
            return True

        except TransactionNotFound:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Approve | Транзакция не прошла за долгий '
                          f'промежуток времени')
            retry += 1
            if retry > 3:
                return False
            return self.approve(token_to_approve, address_to_approve, retry)

        except ConnectionError:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Approve | Ошибка подключения к интернету или '
                          f'проблемы с RPC')
            retry += 1
            if retry > 3:
                return False
            return self.approve(token_to_approve, address_to_approve, retry)

        except Exception as error:
            self.log.info(f'{self.chain_name} | {self.wallet_address} | Approve | Ошибка ({error})')
            retry += 1
            if retry > 3:
                return False
            return self.approve(token_to_approve, address_to_approve, retry)

