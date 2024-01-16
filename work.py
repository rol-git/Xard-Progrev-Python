import random
from tkinter import messagebox
from utils.file import read_lines
from utils.log import log
from utils.proxy import check_proxy
from utils.sleep import go_sleep
from dex.grape import Grape
from dex.dmail import Dmail
from dex.zkstars import ZkStars
from dex.izumi import Izumi
from dex.woofi import WooFi
from dex.maverick import Maverick
from dex.syncswap import SyncSwap
from dex.spacefi import SpaceFi
from dex.uniswap import Uniswap
from dex.pancakeswap import PancakeSwap
from dex.contracts import *


def arrange_settings(app):
    log.info("Начинаю работу")
    try:
        private_keys = read_lines(app.top.entry_path_field.get())
        is_proxy = app.top.proxy_checkbox.get() == "on"
        if is_proxy:
            proxy_list = read_lines("files/proxy_list.txt")
        else:
            proxy_list = []
        is_shuffle = app.top.shuffle_checkbox.get() == "on"
        if is_shuffle:
            random.shuffle(private_keys)
        txs_range = sorted(([int(x) for x in app.top.txs_amount_field.get().split("-")] * 2)[:2])
        delay_range = sorted(([max(int(x), 5) for x in app.top.delay_field.get().split("-")] * 2)[:2])
        timeout_range = sorted(([max(int(x), 5) for x in app.top.timeout_field.get().split("-")] * 2)[:2])
        tickets_range = sorted(([max(int(x), 1) for x in
                                 app.top.tickets_amount_field.get().split("-")] * 2)[:2])
        balance_percent_range = sorted(([min(max(float(x), 0.1), 80) for x in
                                         app.top.balance_percent_field.get().split("-")] * 2)[:2])
        target_price_impact = min(max(float(app.top.price_impact_field.get()), 0.1), 100) + SLIPPAGE

    except Exception as error:
        log.info(f'Ошибка при применении настроек ({error})')
        messagebox.showinfo("Info", "Ошибка при применении настроек (см. консоль)")
        return False

    dex_list = []

    dex_list += [(dex, CHAIN_ID["ZkSync"]) for i, dex in
                 enumerate((Grape, Dmail, ZkStars, Izumi, WooFi, Maverick, SyncSwap,
                            SpaceFi))
                 if app.bottom.zksync_dex_checkboxes[i].get() == "on"]

    dex_list += [(dex, CHAIN_ID["Base"]) for i, dex in enumerate((Grape, Dmail, ZkStars, Izumi, WooFi, Maverick,
                                                                  Uniswap, PancakeSwap))
                 if app.bottom.base_dex_checkboxes[i].get() == "on"]

    if len(dex_list) > 0:
        for i, private_key in enumerate(private_keys):
            result = worker(private_key, proxy_list, dex_list, txs_range, delay_range,
                            tickets_range, balance_percent_range, target_price_impact)
            if i != len(private_keys) - 1 and result:
                go_sleep(*timeout_range)

    log.info("Закончил всю работу")
    messagebox.showinfo("Info", "Вся работа выполнена!")


def worker(private_key, proxy_list, dex_list, txs_range, delay_range, tickets_range, balance_percent_range,
           target_price_impact):
    dex_copy = dex_list.copy()
    proxy = None
    proxy_list_copy = proxy_list.copy()
    while proxy_list_copy:
        proxy = random.choice(proxy_list_copy)
        proxy_list_copy.remove(proxy)
        if check_proxy(proxy):
            break
        if not proxy_list_copy:
            web3 = Web3(Web3.HTTPProvider(RPC[CHAIN_ID["ZkSync"]], request_kwargs={"timeout": 60}))
            wallet_address = web3.eth.account.from_key(private_key).address
            log.info(f'{wallet_address} | Нет рабочих прокси | Пропускаю аккаунт')
            with open("files/no_working_proxies.txt", mode="w") as f:
                f.write(private_key + "\n")
                f.write(private_key + "\n")
            return False

    if proxy:
        web3 = {
            CHAIN_ID["ZkSync"]: Web3(
                Web3.HTTPProvider(RPC[CHAIN_ID["ZkSync"]],
                                  request_kwargs={"proxies": {"https": proxy, "http": proxy},
                                                  "timeout": 60})),
            CHAIN_ID["Base"]: Web3(
                Web3.HTTPProvider(RPC[CHAIN_ID["Base"]],
                                  request_kwargs={"proxies": {"https": proxy, "http": proxy},
                                                  "timeout": 60}))
        }

    else:
        web3 = {
            CHAIN_ID["ZkSync"]: Web3(
                Web3.HTTPProvider(RPC[CHAIN_ID["ZkSync"]], request_kwargs={"timeout": 60})),
            CHAIN_ID["Base"]: Web3(Web3.HTTPProvider(RPC[CHAIN_ID["Base"]], request_kwargs={"timeout": 60}))
        }

    parsed_private_key = "0x" + private_key if private_key[:2] != "0x" else private_key

    for i in range(len(dex_copy)):
        try:
            dex_copy[i] = dex_copy[i][0](parsed_private_key, web3[dex_copy[i][1]], dex_copy[i][1], log,
                                         target_price_impact)
        except Exception:
            log.info(f'Ошибка одного из аккаунтов (скорее всего, некорректный приватный ключ -> {private_key})')
            with open("files/invalid_private_keys.txt", mode="w") as f:
                f.write(private_key + "\n")
            return False

    tx_map = dict(filter(lambda item: item[1] > 0, {dex: random.randint(*txs_range) for dex in dex_copy}.items()))

    straight_failed_tx = {
        CHAIN_ID["ZkSync"]: 0,
        CHAIN_ID["Base"]: 0
    }

    log.info(f'Начинаю работать с {dex_copy[0].wallet_address}')

    while tx_map:

        current_dex = random.choice(list(tx_map.keys()))

        if isinstance(current_dex, Grape):
            if current_dex.buy_tickets(random.randint(*tickets_range)):
                straight_failed_tx[current_dex.chain_id] = 0
                tx_map[current_dex] -= 1
            else:
                straight_failed_tx[current_dex.chain_id] += 1
        elif isinstance(current_dex, Dmail):
            if current_dex.send_message():
                straight_failed_tx[current_dex.chain_id] = 0
                tx_map[current_dex] -= 1
            else:
                straight_failed_tx[current_dex.chain_id] += 1
        elif isinstance(current_dex, ZkStars):
            if current_dex.mint_nft():
                straight_failed_tx[current_dex.chain_id] = 0
                tx_map[current_dex] -= 1
            else:
                straight_failed_tx[current_dex.chain_id] += 1
        else:
            if current_dex.buy_token(*list(TOKENS[current_dex.chain_id]["STABLE"].items())[0],
                                     round(random.uniform(*balance_percent_range), 2), target_price_impact):
                straight_failed_tx[current_dex.chain_id] = 0
                go_sleep(*delay_range)
                if current_dex.sell_token(*list(TOKENS[current_dex.chain_id]["STABLE"].items())[0],
                                          target_price_impact):
                    tx_map[current_dex] -= 1
                else:
                    straight_failed_tx[current_dex.chain_id] += 1
            else:
                straight_failed_tx[current_dex.chain_id] += 1

        for chain_id in straight_failed_tx.keys():
            if straight_failed_tx[chain_id] > 2:
                log.info(f'{CHAIN_NAME[chain_id]} | {dex_copy[0].wallet_address} | '
                         f'Не прошло три разные транзакции подряд')
                for dex in tx_map.keys():
                    if dex.chain_id == chain_id:
                        tx_map[dex] = 0
                with open(f'files/failed_{CHAIN_NAME[chain_id].lower()}.txt', mode="w") as f:
                    f.write(private_key + "\n")
                straight_failed_tx[chain_id] = 0

        tx_map = dict(filter(lambda item: item[1] > 0, tx_map.items()))

        if tx_map:
            go_sleep(*delay_range)

    log.info(f'Закончил работать с {dex_copy[0].wallet_address}')

    return True
