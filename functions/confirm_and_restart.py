from tkinter import messagebox
import subprocess

def confirm_and_restart(ip_address):
    result = messagebox.askyesno(
        "Potvrzení",
        f"Opravdu chceš restartovat {ip_address}?"
    )
    if result:
        print(f'Restartuji {ip_address}')
        cmd = [
                "shutdown",
                "/m", f"\\\\{ip_address}",
                "/r",            # restart
                "/f",            # vynuceně zavřít aplikace
                "/t", "0",       # zpoždění 0 sekund
                "/c", "\"Restartujem sa!\""
            ]
        subprocess.run(cmd, shell=True)