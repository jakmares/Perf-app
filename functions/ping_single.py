from ping3 import ping
import socket

def ping_single(hostname, update_icon_callback, update_jmeter_icon_callback):
    try:
        response = ping(hostname["address"], timeout=2)
        print(f'{hostname["address"]} je dostupný za {response}')
        new_state = response is not None
    except Exception:
        print(f'{hostname["address"]} není dostupný.')
        new_state = False

    if hostname["last_state"] != new_state:
        hostname["last_state"] = new_state
        update_icon_callback(hostname, new_state)

    if response is not None:
        try:
            with socket.create_connection((hostname["address"], 1099), timeout=2):
                new_state = True
                print(f'Server na adrese {hostname["address"]} je dostupný')
        except Exception:
            new_state = False
            print(f'Server na adrese {hostname["address"]} není dostupný')

        if hostname.get("server_status") != new_state:
            hostname["server_status"] = new_state
            update_jmeter_icon_callback(hostname, new_state)  # <- důležité
