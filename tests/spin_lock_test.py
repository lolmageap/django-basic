import time

from concurrent.futures import ThreadPoolExecutor

from common.spin_lock import SpinLock

value = 0


def no_lock_plus_one() -> int:
    global value
    temp = value
    time.sleep(0.1)
    value = temp + 1
    return value


def plus_one_with_spin_lock() -> int:
    with SpinLock("test1"):
        global value
        temp = value
        time.sleep(0.1)
        value = temp + 1
        return value


@SpinLock("test1")
def plus_one_with_spin_lock_v2() -> int:
    global value
    temp = value
    time.sleep(0.1)
    value = temp + 1
    return value


def test_no_lock():
    global value
    value = 0

    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(no_lock_plus_one) for _ in range(num_threads)]
        for future in futures:
            future.result()

    assert value < num_threads


def test_spin_lock():
    global value
    value = 0

    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(plus_one_with_spin_lock) for _ in range(num_threads)]
        for future in futures:
            future.result()

    assert value == num_threads


def test_spin_lock_v2():
    global value
    value = 0

    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(plus_one_with_spin_lock_v2) for _ in range(num_threads)]
        for future in futures:
            future.result()

    assert value == num_threads
