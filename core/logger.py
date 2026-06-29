from core.config import Settings


def log(*args):
    if Settings.DEBUG:
        print(*args, flush=True)
