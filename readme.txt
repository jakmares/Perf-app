## 🔧 Požadavky

- Python 3.12 nebo novější
- Git
- pip (součást Pythonu)

Instalace
1. Naklonuj repozitář:

   ```bash
   git clone git@github.com:tvoje-jmeno/Perf-app.git
   cd Perf-app

2. Vytvoř virutální prostředí
win
python -m venv venv
source venv/Scripts/activate

linus 
python3 -m venv venv
source venv/bin/activate

3. Nainstaluj závislosti
pip install -r requirements.txt

případně přes proxy 
pip install -r requirements.txt --proxy http://proxy.firma.cz:8080 - pokud ji neznáš tak si ji zjisti sem ji psát nebudu :) 

4. Spusť aplikaci 
python main.py