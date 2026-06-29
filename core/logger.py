from core.config import Settings


def log(*args):
    if Settings.debug:
        print(*args, flush=True)
