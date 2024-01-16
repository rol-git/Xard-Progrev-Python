import requests


def check_proxy(proxy):
    proxies = {
        "http": proxy,
        "https": proxy
    }

    url = "https://api.ipify.org?format=json"

    while True:
        try:
            pc_ip = requests.get(url, timeout=5).json()["ip"]
            break

        except Exception:
            continue

    try:
        proxy_ip = requests.get(url, proxies=proxies, timeout=10).json()["ip"]
        if proxy_ip == pc_ip:
            return False

        return True

    except Exception:
        return False
