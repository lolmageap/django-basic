import time
from concurrent.futures import ThreadPoolExecutor

from common.spin_lock import SpinLock

value = 0


@SpinLock("test1")
def plus_one() -> int:
    global value
    temp = value
    time.sleep(0.1)
    value = temp + 1
    print(value)
    return value


def test_spin_lock():
    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(plus_one) for _ in range(num_threads)]
        for future in futures:
            future.result()
