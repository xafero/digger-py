import time


class SystemX:
    @classmethod
    def current_millis(cls):
        return round(time.time() * 1000)

    @classmethod
    def sleep(cls, wait_ms):
        sec = wait_ms / 1000.0
        time.sleep(sec)
