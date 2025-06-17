"""Perf Test Control Panel
========================
GUI aplikace pro správu a monitoring vzdálených uzlů se spuštěnými JMeter servery.
Tento soubor obsahuje přidané komentáře, aby byl kód snadno čitelný a srozumitelný.
"""

# ---------- Importy knihoven ----------
import tkinter as tk                    # Standardní GUI toolkit dodávaný s Pythonem
from PIL import ImageTk                 # Práce s obrázky (Pillow)
import webbrowser                       # Otevírání URL ve výchozím prohlížeči

import config                           # Vlastní modul s konfigurací uzlů
import functions                        # Vlastní modul s funkční logikou (ping, restart…)
from functions import updaters          # Plánovač periodických úloh pro GUI

# ---------- Konstanty vizuálu ----------
BG_COLOR = "#1e1e1e"          # Barva pozadí celé aplikace
FONT_COLOR_TEXT = "#F7F2E8"   # Barva standardního textu
BUTTON_BG_COLOR = "#444444"    # Barva tlačítek

REFRESH_TIME = 60_000          # Interval kontroly stavů (v milisekundách) → 60 s

# ---------- Inicializace hlavního okna ----------
root = tk.Tk()
root.title("Perf test control panel")

# ---------- Hlavní rámec (parent container) ----------
mainFrame = tk.Frame(root, width=1000, height=600, bg=BG_COLOR)
mainFrame.grid(row=0, column=0)  # Umístění na grid (0,0)
mainFrame.pack_propagate(False)  # Zabrání automatickému přizpůsobení velikosti obsahu

# ---------- Logo společnosti / projektu ----------
logo_img = ImageTk.PhotoImage(file="img/logo.png")
logo_widget = tk.Label(mainFrame, image=logo_img, bg=BG_COLOR)
logo_widget.image = logo_img       # Uložení reference na obrázek, aby jej GC nesmazal
logo_widget.pack(pady=10)          # Vykreslení s odstupem 10 px

# ---------- Přednačtení ikon pro stav OK / NOK ----------
ok_img = ImageTk.PhotoImage(file="img/ok.png")   # Zelená fajfka
nok_img = ImageTk.PhotoImage(file="img/nok.png") # Červený křížek

# ---------- Nadpis sekce se vzdálenými uzly ----------
tk.Label(
    mainFrame,
    text="Remotes",
    bg=BG_COLOR,
    fg=FONT_COLOR_TEXT,
    font=("tkMenuFont", 14)
).pack()

# ---------- Rámec pro tabulku ----------
# Používáme samostatný frame, aby se tabulka dala stylovat odděleně od zbytku GUI

table_frame = tk.Frame(mainFrame, bg=BG_COLOR)
table_frame.pack(pady=10)

# ---------- Hlavička tabulky ----------
headers = [
    "Hostname",     # Název stroje
    "IP adresa",    # IPv4/IPv6
    "MAC",          # MAC adresa síťového rozhraní
    "Last State",   # Poslední stav pingu
    "Jmeter Server",# Stav JMeter serveru
    #"Action"        # Sloupec pro tlačítka
]

for col, header in enumerate(headers):
    tk.Label(
        table_frame,
        text=header,
        bg=BG_COLOR,
        fg=FONT_COLOR_TEXT,
        font=("tkMenuFont", 12, "bold"),
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=3
    ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

# Slovníky pro ukládání widgetů ikon (budou se dynamicky měnit)
status_labels: dict[str, tk.Label] = {}   # hostname → Label pro ping status
server_status: dict[str, tk.Label] = {}   # hostname → Label pro JMeter status

# ---------- Naplnění tabulky daty z config.remotes ----------
for row, (hostname, data) in enumerate(config.remotes.items(), start=1):
    # --- 1) Textové sloupce (hostname, IP, MAC) ---
    values = [hostname, data["address"], data["mac"]]
    for col, value in enumerate(values):
        tk.Label(
            table_frame,
            text=value,
            bg=BG_COLOR,
            fg=FONT_COLOR_TEXT,
            font=("tkMenuFont", 11),
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=3
        ).grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    # --- 2) Sloupec "Last State" – ikona podle posledního pingu ---
    state_icon = ok_img if data["last_state"] else nok_img
    state_label = tk.Label(
        table_frame,
        image=state_icon,
        bg=BG_COLOR,
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=3
    )
    state_label.image = state_icon  # Udržení reference na obrázek
    state_label.grid(row=row, column=3, padx=1, pady=1)
    status_labels[hostname] = state_label  # Uložení pro pozdější aktualizaci

    # --- 3) Sloupec "Jmeter Server" – ikona podle stavu serveru ---
    server_state_icon = ok_img if data["server_status"] else nok_img
    server_state_label = tk.Label(
        table_frame,
        image=server_state_icon,
        bg=BG_COLOR,
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=3
    )
    server_state_label.image = server_state_icon
    server_state_label.grid(row=row, column=4, padx=1, pady=1)
    server_status[hostname] = server_state_label  # Uložení pro pozdější aktualizaci

    # --- 4) Akční tlačítko "Restart" ---
    tk.Button(
        table_frame,
        text="Restart",
        font=("TkHeadingFont", 11),
        bg=BUTTON_BG_COLOR,
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        # Použijeme lambda, aby se IP adresa svázala se správným řádkem
        command=lambda ip=data["address"]: functions.confirm_and_restart(ip)
    ).grid(row=row, column=5, padx=1, pady=1)

    # Tlačítko Refresh (col 6)
    refresh_callback = lambda _unused, st, h=hostname: updaters.update_icon(
        h, st, status_labels, ok_img, nok_img
    )
    refresh_jmeter_callback = lambda _unused, st, h=hostname: updaters.update_jmeter_icon(h, st, server_status, ok_img, nok_img)

    tk.Button(table_frame, text="Refresh", font=("TkHeadingFont", 11), bg=BUTTON_BG_COLOR,
              fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black",
              command=lambda d=data, cb=refresh_callback, cb1=refresh_jmeter_callback: functions.ping_single(d, cb, cb1)
              ).grid(row=row, column=6, padx=1, pady=1)

# ---------- Obrázek fungující jako tlačítko pod tabulkou ----------
elastic_img = ImageTk.PhotoImage(file="img/elastic.png")

elastic_button = tk.Label(
    mainFrame,
    image=elastic_img,
    bg=BG_COLOR,
    cursor="hand2",           # Změna kurzoru při najetí
    )
# Udržíme referenci, aby obrázek nezmizel ze vstupů GC
elastic_button.image = elastic_img
# Kliknutím otevře defaultní prohlížeč
elastic_button.bind("<Button-1>", lambda e: webbrowser.open(config.elastic_url))
# Umístíme pod tabulku s pěkným odsazením
elastic_button.place(x=130, y=390)

confluence_img = ImageTk.PhotoImage(file="img/confluence.png")

confluence_button = tk.Label(
    mainFrame,
    image=confluence_img,
    bg=BG_COLOR,
    cursor="hand2",           # Změna kurzoru při najetí
    )
# Udržíme referenci, aby obrázek nezmizel ze vstupů GC
confluence_button.image = confluence_img
# Kliknutím otevře defaultní prohlížeč
confluence_button.bind("<Button-1>", lambda e: webbrowser.open(config.confluence_url))
# Umístíme pod tabulku s pěkným odsazením
confluence_button.place(x=250, y=390)

per_mon_img = ImageTk.PhotoImage(file="img/remotes_mon.png")

per_mon_button = tk.Label(
    mainFrame,
    image=per_mon_img,
    bg=BG_COLOR,
    cursor="hand2",           # Změna kurzoru při najetí
    )
# Udržíme referenci, aby obrázek nezmizel ze vstupů GC
per_mon_img.image = per_mon_img
# Kliknutím otevře defaultní prohlížeč
per_mon_button.bind("<Button-1>", lambda e: webbrowser.open(config.perf_monitor_url))
# Umístíme pod tabulku s pěkným odsazením
per_mon_button.place(x=370, y=390)

# ---------- Periodické kontroly (ping + stav JMeter serveru) ----------
# Zdrojové funkce (ping_all, check_jmeter_server_statuses) vracejí slovník {hostname: bool}
# Updaters obsahují obálku, která po každém intervalu zavolá callback a případně aktualizuje GUI.
development = False

if development == False: 
    updaters.schedule_ping(
        root,
        REFRESH_TIME,
        functions.ping_all,
        # Callback, který dle výsledku přepíná ikonu v tabulce
        lambda h, s: updaters.update_icon(h, s, status_labels, ok_img, nok_img)
    )

    updaters.schedule_jmeter_check(
        root,
        REFRESH_TIME,
        functions.check_jmeter_server_statuses,
        # Callback pro JMeter ikonky
        lambda h, s: updaters.update_jmeter_icon(h, s, server_status, ok_img, nok_img)
    )

# ---------- Spuštění hlavní smyčky Tkinter ----------
root.mainloop()  # Blokuje vlákno a čte události GUI