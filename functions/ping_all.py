import config
from ping3 import ping

def ping_all(update_icon_callback):
    for hostname, data in config.remotes.items():
        try:
            response = ping(data["address"], timeout=2)
            print(f'{data["address"]} je dostupný za {response}')
            new_state = response is not None
        except Exception:
            print(f'{data["address"]} není dostupný.')
            new_state = False

        if data["last_state"] != new_state:
            data["last_state"] = new_state
            update_icon_callback(hostname, new_state)