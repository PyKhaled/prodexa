import hashlib


def make_cache_key(url: str, soft: bool) -> str:
    raw = f"{url}|soft={soft}"
    return hashlib.sha256(raw.encode()).hexdigest()

def _check_updates(root):
    update = check_for_update()
    if update:
        UpdateDialog(root, update)