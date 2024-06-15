# Anleitung: Fall Detection System

Dieses Projekt implementiert ein Fall Detection System, das über MQTT kommuniziert. Die Zustände werden mittels LEDs und einem Buzzer angezeigt. Es gibt vier mögliche Zustände, die vom System erkannt und dargestellt werden:

- **0: Everything okay** - Das System zeigt an, dass alles in Ordnung ist.
- **1: Fall detected** - Das System zeigt an, dass ein Sturz erkannt wurde.
- **2: Fall maybe detected** - Das System zeigt an, dass möglicherweise ein Sturz erkannt wurde.
- **3: Exit** - Beendet das System und schaltet alle Anzeigen ab.

## Installation und Ausführung

### Voraussetzungen

- Docker
- Docker Compose

### Schritte zur Ausführung

1. **Repository klonen und in das Verzeichnis wechseln:**

```sh
git clone <repository-url>
cd <repository-directory>
```

2. **Docker-Container bauen und starten:**
```sh
sudo docker-compose build
```
```sh
sudo docker-compose up -d
```
3. **Shell in den Containern öffnen und Skripte manuell ausführen:**

Öffnen Sie zwei separate Terminals.

Terminal 1: fall_detection_pub
```sh
sudo docker exec -it fall_detection_pub /bin/bash
```

Führen Sie dann das Skript manuell aus:
```sh
python3 pub.py 0
```

Terminal 2: fall_detection_alarm

```sh
sudo docker exec -it fall_detection_alarm /bin/bash
```

Führen Sie dann das Skript manuell aus:
```sh
python3 alarm.py
```

Zustände ändern
Während das Skript pub.py läuft, können Sie die Zustände ändern, indem Sie die entsprechenden Zahlen (0, 1, 2 oder 3) eingeben und sehr schnell dannach auf enter drücken. Der Zustand wird an das System gesendet und die Anzeigen werden entsprechend aktualisiert.