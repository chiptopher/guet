import time


def current_millis() -> int:
    return int(round(time.time() * 1000))
