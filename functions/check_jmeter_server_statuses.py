import config
import socket

#zjištění nastartování serveru jmetru, jmeter naslouchá na portu 1099 
def check_jmeter_server_statuses(update_jmeter_icon_callback):
    for hostname, data in config.remotes.items():
        try:
            with socket.create_connection((data["address"], 1099), timeout=2):
                new_state = True
                print(f'Server na adrese {data["address"]} je dostupný')
        except Exception:
            new_state = False
            print(f'Server na adrese {data["address"]} není dostupný')

        if data.get("server_status") != new_state:
            data["server_status"] = new_state
            update_jmeter_icon_callback(hostname, new_state)  # <- důležité
