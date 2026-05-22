# Taschengeld-Verwaltung (Desktop Starter)

Dieses Repository enthält ein kleines Desktop-Starterprojekt zur Verwaltung des Taschengelds deiner Kinder.

Funktionen (MVP):
- Kinder anlegen (Name, Alter, Kontostand)
- Aufgaben anlegen (Titel, Beschreibung, Betrag)
- Aufgaben als erledigt markieren (Eltern bestätigen → Auszahlung)
- SQLite-Datenbank (`data.db`) im Projektordner

Schnellstart
1. Stelle sicher, dass Python 3.8+ installiert ist.
2. Starte die App:

```bash
python main.py
```

Einfacher Start (automatisiert)

- Linux / macOS:

```bash
./run.sh
```

- Windows:

```powershell
.\run.bat
```

Das Skript erstellt bei Bedarf ein virtuelles Environment, installiert Abhängigkeiten und startet die App. `run.sh` versucht bei fehlendem DISPLAY automatisch `xvfb-run` zu verwenden.


Dateien
- `main.py`: App-Entrypoint
- `db.py`: SQLite-Initialisierung
- `models.py`: CRUD-Operationen und Geschäftslogik
- `gui.py`: Einfache Tkinter-Oberfläche

Nächste Schritte (optional):
- CSV-Export, Benutzer-Authentifizierung, wiederkehrende Aufgaben, bessere UI (z.B. mit Electron oder Qt)

Packaging / Executable mit PyInstaller

1. Stelle sicher, dass `pyinstaller` installiert ist (oder benutze `build.sh`):

```bash
pip install pyinstaller
```

2. Erstelle ein distributables Verzeichnis (`--onedir` empfohlen, damit `data.db` neben der App liegt):

```bash
pyinstaller --noconfirm --onedir --windowed --name TaschengeldApp main.py
```

3. Ergebnis liegt in `dist/TaschengeldApp/` — dort findest du die ausführbare App und kannst sie an Eltern auf anderen Rechnern weitergeben. Beachte: `data.db` wird beim ersten Start im Arbeitsverzeichnis angelegt.

Alternativ: Script ausführen

```bash
./build.sh
```

