# 🏠 Meine Home Assistant Konfiguration

Meine persönliche Home Assistant Konfiguration mit Fokus auf Solarenergie-Monitoring, intelligente Automatisierungen und benutzerfreundliche Dashboards.

## 📋 Inhaltsverzeichnis

- [🎯 Überblick](#-überblick)
- [🏗️ Struktur](#️-struktur)
- [⚡ Features](#-features)
- [📁 Dateiübersicht](#-dateiübersicht)
- [🚀 Installation](#-installation)
- [⚙️ Konfiguration](#️-konfiguration)
- [📊 Dashboard-Templates](#-dashboard-templates)
- [🔧 Wartung](#-wartung)

## 🎯 Überblick

Meine persönliche Home Assistant Konfiguration bietet:

- **📊 Solar-Monitoring**: Überwachung mehrerer Solaranlagen (Garage + Dach) mit MQTT-Integration
- **📈 Energieverwaltung**: Utility Meter für detaillierte Verbrauchsanalysen
- **🤖 Intelligente Automatisierungen**: Automatisierte Abläufe für verschiedene Szenarien
- **🎨 Angepasste Templates**: Erweiterte Sensoren für Dashboard-Darstellung
- **📡 MQTT-Integration**: Echtzeit-Datenübertragung von externen Geräten

## 🏗️ Struktur

```
📂 homeassistant/
├── 📄 configuration.yaml     # Hauptkonfiguration
├── 📄 automations.yaml      # Automatisierungsregeln
├── 📄 scripts.yaml          # Wiederverwendbare Skripte
├── 📄 scenes.yaml           # Vordefinierte Szenen
├── 📄 customize.yaml        # UI-Anpassungen
├── 📄 mqtt.yaml             # MQTT-Sensoren (Solar)
├── 📄 utility_meters.yaml   # Energieverbrauchsmessungen
└── 📂 templates/            # Template-Sensoren
    ├── 📄 dashboard_templates.yaml
    ├── 📄 general_templates.yaml
    └── 📄 solar_templates.yaml
```

## ⚡ Features

### 🌞 Solar-Monitoring
- **Dual-Anlagen-Support**: Überwachung von Garage- und Dach-Solaranlagen
- **Echtzeit-Daten**: Live-Leistungswerte über MQTT (Hoymiles-DTU)
- **Aggregierte Werte**: Gesamtleistung und kombinierte Erträge
- **Historische Daten**: Tages-, Monats- und Jahreserträge

### 📊 Template-Sensoren
- **Solar Templates**: Berechnung von Gesamtleistung und Effizienzwerten
- **Dashboard Templates**: Aufbereitete Daten für die UI-Darstellung
- **General Templates**: Allgemeine Hilfssensoren

### 🔌 MQTT-Integration
- **Hoymiles-DTU**: Direktanbindung der Solar-Wechselrichter
- **Echtzeit-Updates**: Automatische Datenaktualisierung
- **Fehlerbehandlung**: Robuste Behandlung von Verbindungsabbrüchen

### 📈 Utility Meter
- **Energieverbrauch**: Detaillierte Verbrauchsmessungen
- **Zeitbasierte Auswertungen**: Stunden-, Tages-, Monats- und Jahreswerte
- **Kostenberechnung**: Automatische Berechnung von Energiekosten

## 📁 Dateiübersicht

| Datei | Beschreibung |
|-------|-------------|
| `configuration.yaml` | Hauptkonfiguration mit allen Integrationen |
| `automations.yaml` | Automatisierungsregeln für Smart Home Abläufe |
| `scripts.yaml` | Wiederverwendbare Aktionsskripte |
| `scenes.yaml` | Vordefinierte Gerätekombinationen |
| `customize.yaml` | UI-Anpassungen und Entity-Konfigurationen |
| `mqtt.yaml` | MQTT-Sensoren für Solar-Datenübertragung |
| `utility_meters.yaml` | Energieverbrauchsmessungen und -auswertungen |

### 📂 Templates Ordner

| Template | Zweck |
|----------|-------|
| `solar_templates.yaml` | Solar-spezifische Berechnungen und Aggregationen |
| `dashboard_templates.yaml` | UI-optimierte Sensoren für Dashboards |
| `general_templates.yaml` | Allgemeine Hilfssensoren und Berechnungen |

## 🚀 Installation

1. **Repository klonen**:
   ```bash
   git clone https://github.com/Jensbe1337/homeassistant.git
   cd homeassistant
   ```

2. **Home Assistant vorbereiten**:
   - Stoppen Sie Home Assistant
   - Sichern Sie Ihre bestehende Konfiguration
   - Kopieren Sie die Dateien in Ihr Home Assistant config-Verzeichnis

3. **Anpassungen vornehmen**:
   - Passen Sie `configuration.yaml` an Ihre Umgebung an
   - Konfigurieren Sie MQTT-Broker-Einstellungen
   - Überprüfen Sie alle Entity-IDs in den Templates

4. **Home Assistant starten**:
   - Starten Sie Home Assistant neu
   - Überprüfen Sie die Logs auf Fehler
   - Testen Sie alle Sensoren und Automatisierungen

## ⚙️ Konfiguration

### 🔧 MQTT-Setup

Stellen Sie sicher, dass Ihr MQTT-Broker konfiguriert ist:

```yaml
mqtt:
  broker: YOUR_MQTT_BROKER_IP
  port: 1883
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```

### 🌞 Solar-Konfiguration

Passen Sie die MQTT-Topics in `mqtt.yaml` an Ihre Hoymiles-DTU an:

```yaml
sensor:
  - name: "Solar Leistung Garage aktuell"
    state_topic: "Garage-Solar/Garage/ch0/P_AC"  # Anpassen!
```

### 📊 Template-Anpassungen

Überprüfen Sie die Entity-IDs in den Template-Dateien und passen Sie diese an Ihre Sensoren an.

## 📊 Dashboard-Templates

Die Template-Sensoren bieten aufbereitete Daten für:

- **Solar-Übersicht**: Gesamtleistung, Effizienz, Tageserträge
- **Energiebilanz**: Verbrauch vs. Erzeugung
- **Historische Daten**: Trends und Vergleichswerte
- **Status-Indikatoren**: Betriebszustände und Alarme

## 🔧 Wartung

### 📝 Regelmäßige Aufgaben

- **Logs prüfen**: Überwachen Sie die Home Assistant Logs auf Fehler
- **Backups erstellen**: Regelmäßige Sicherung der Konfiguration
- **Updates**: Halten Sie Home Assistant und Integrationen aktuell
- **Template-Validierung**: Überprüfen Sie Template-Sensoren nach Updates

### 🐛 Fehlerbehebung

1. **Konfiguration validieren**:
   ```bash
   # In Home Assistant UI: Entwicklertools > YAML-Konfiguration prüfen
   ```

2. **Logs analysieren**:
   ```bash
   # Überprüfen Sie die Home Assistant Logs auf Fehler
   ```

3. **Template-Tests**:
   ```bash
   # Entwicklertools > Template-Editor verwenden
   ```

### 📞 Support

Bei Fragen oder Problemen:

- Überprüfen Sie die [Home Assistant Dokumentation](https://www.home-assistant.io/docs/)
- Nutzen Sie die [Community](https://community.home-assistant.io/)
- Erstellen Sie ein Issue in diesem Repository

---

## 📄 Lizenz

Diese Konfiguration wird unter der MIT-Lizenz geteilt. Siehe [LICENSE](LICENSE) für Details.

## 🤝 Beiträge

Verbesserungsvorschläge und Beiträge sind willkommen! Bitte:

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request

---

**Hinweis**: Dies ist meine persönliche Home Assistant Konfiguration, die auf meine spezifische Hardware und Umgebung zugeschnitten ist. Wenn Sie diese Konfiguration verwenden möchten, passen Sie alle Entity-IDs, MQTT-Topics und Hardware-spezifischen Einstellungen an Ihre Installation an.
