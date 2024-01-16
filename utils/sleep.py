import random
from time import sleep
from .log import log


def go_sleep(t1, t2):
    value = random.randint(t1, t2)
    log.info(f'Сплю {value} секунд')
    sleep(value)
