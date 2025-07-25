# ==============================================================================
# README - Solarladen Erna Python Script
# ==============================================================================
#
# BESCHREIBUNG:
# Dieses Python-Skript ersetzt die Home Assistant Automation "STR Solarladen Erna"
# und implementiert eine intelligente Solarladung für das Elektrofahrzeug "Erna"
# mit dynamischer Leistungsregelung basierend auf verfügbarer Solarenergie.
#
# FUNKTIONEN:
# - Automatischer Start bei ausreichend Solarüberschuss (< -1500W)
# - Dynamische Anpassung der Ladeleistung je nach Stromverbrauch
# - Stopp bei vollem Akku (> 80%) oder zu hohem Strombezug (> 1000W)
# - Reduzierte Ladeleistung bei geringem Solarüberschuss
# - Intelligente Wiederherstellung der vollen Ladeleistung
# - Automatische Deaktivierung bei zu geringer Wallbox-Leistung (< 50W)
#
# VERWENDUNG:
# 1. Skript in Home Assistant python_scripts Ordner speichern
# 2. Debug-Logging bei Bedarf durch Setzen von DEBUG_LOGGING = False deaktivieren
# 3. Über Automation zeitbasiert aufrufen (empfohlen: jede Minute)
# 4. Oder manuell über Service: python_script.solarladen_erna
#
# BEISPIEL AUTOMATION FÜR ZEITBASIERTE AUSFÜHRUNG:
# automation:
#   - alias: "Solarladen Erna Ausführung"
#     trigger:
#       - platform: time_pattern
#         seconds: 0
#     condition:
#       - condition: state
#         entity_id: input_boolean.solarladen_erna
#         state: 'on'
#     action:
#       - service: python_script.solarladen_erna
#
# BENÖTIGTE ENTITÄTEN:
# - input_boolean.solarladen_erna          : Master-Schalter (on/off)
# - sensor.erna_battery_level               : Batteriestand (0-100%)
# - sensor.stromzaehler_leistung_durchschnitt_10min : Stromzähler Durchschnitt (W)
# - switch.garage_mobile_wallbox_switch_0   : Wallbox Hauptschalter
# - switch.erna_reduced_ac_charging         : Reduzierte Ladeleistung Schalter
# - sensor.garage_mobile_wallbox_switch_0_power : Aktuelle Wallbox Leistung (W)
#
# LOGIK-ABLAUF:
# 1. Prüfung ob Solarladung aktiviert ist
# 2. Stopp-Bedingungen: Akku > 80% ODER Strombezug > 1000W
# 3. Start-Bedingungen: Solarüberschuss < -1500W UND Akku < 80%
# 4. Reduzierung: Strombezug 0-1000W während Ladung aktiv
# 5. Erhöhung: Solarüberschuss < -1000W bei reduzierter Ladung
# 6. Deaktivierung: Wallbox-Leistung < 50W bei eingeschalteter Wallbox (schaltet Wallbox aus und deaktiviert input_boolean)
#
# SCHWELLENWERTE:
# - Akku-Maximum: 80%
# - Stopp-Schwelle: 1000W Strombezug
# - Start-Schwelle: -1500W Solarüberschuss
# - Reduzierungs-Schwelle: 0-1000W Strombezug
# - Erhöhungs-Schwelle: -1000W Solarüberschuss
# - Mindest-Wallbox-Leistung: 50W (für aktive Ladung und Deaktivierungs-Schwelle)
#
# AUTOR: Home Assistant Benutzer
# VERSION: 1.0
# DATUM: Juli 2025
# ==============================================================================

"""
Intelligente Solarladung für Erna mit dynamischer Leistungsregelung.

Dieses Skript ersetzt die Automation "STR Solarladen Erna" und implementiert:
- Start bei genügend Solarüberschuss
- Dynamische Leistungsregelung je nach verfügbarer Solarenergie
- Stopp bei vollem Akku oder zu hohem Strombezug
- Automatische Deaktivierung bei zu geringer Wallbox-Leistung

Entitäten:
- input_boolean.solarladen_erna: Master-Schalter für die Solarladung
- sensor.erna_battery_level: Batteriestand von Erna (%)
- sensor.stromzaehler_leistung_durchschnitt_10min: Durchschnittliche Stromzählerleistung (W)
- switch.garage_mobile_wallbox_switch_0: Wallbox Hauptschalter
- switch.erna_reduced_ac_charging: Reduzierte Ladeleistung
- sensor.garage_mobile_wallbox_switch_0_power: Aktuelle Wallbox-Leistung (W)
"""

# Logging-Test: Skript wurde gestartet
# Konfiguration für Debug-Logging (True = aktiviert, False = deaktiviert)
DEBUG_LOGGING = True

logger.info("=== Solarladen Erna Skript gestartet ===")

# Abrufen der aktuellen Sensordaten mit Fehlerbehandlung
try:
    # Prüfen ob alle benötigten Entitäten verfügbar sind
    solarladen_state = hass.states.get('input_boolean.solarladen_erna')
    battery_state = hass.states.get('sensor.erna_battery_level')
    power_state = hass.states.get('sensor.stromzaehler_leistung_durchschnitt_10min')
    wallbox_power_state = hass.states.get('sensor.garage_mobile_wallbox_switch_0_power')
    wallbox_switch_state_obj = hass.states.get('switch.garage_mobile_wallbox_switch_0')
    reduced_charging_state_obj = hass.states.get('switch.erna_reduced_ac_charging')
    
    # Prüfen ob alle Entitäten existieren
    if not all([solarladen_state, battery_state, power_state, wallbox_power_state, wallbox_switch_state_obj, reduced_charging_state_obj]):
        logger.error("Solarladen Erna - Eine oder mehrere Entitäten sind nicht verfügbar!")
        logger.error(f"Verfügbare Entitäten: solarladen={bool(solarladen_state)}, battery={bool(battery_state)}, power={bool(power_state)}, wallbox_power={bool(wallbox_power_state)}, wallbox_switch={bool(wallbox_switch_state_obj)}, reduced_charging={bool(reduced_charging_state_obj)}")
        exit()
    
    # Werte extrahieren und konvertieren
    solarladen_enabled = solarladen_state.state == 'on'
    battery_level = float(battery_state.state)
    power_avg_10min = float(power_state.state)
    wallbox_power = float(wallbox_power_state.state)
    wallbox_switch_state = wallbox_switch_state_obj.state
    reduced_charging_state = reduced_charging_state_obj.state
    
    logger.info(f"Solarladen Erna - Status: enabled={solarladen_enabled}, battery={battery_level}%, power_avg={power_avg_10min}W, wallbox_power={wallbox_power}W")
    
    if DEBUG_LOGGING:
        logger.debug(f"Solarladen Erna - Detailstatus: wallbox_switch={wallbox_switch_state}, reduced_charging={reduced_charging_state}")
    
except Exception as e:
    logger.error(f"Solarladen Erna - Fehler beim Abrufen der Sensordaten: {e}")
    exit()

# Prüfen ob Solarladung aktiviert ist
if not solarladen_enabled:
    logger.info("Solarladen Erna ist deaktiviert - Skript beendet")
else:
    # Logik für Solarladung
    
    # 1. Stoppe das Laden wenn Akku voll ist oder zu viel Strom bezogen wird
    if battery_level > 80 or power_avg_10min > 1000:
        if wallbox_switch_state == 'on':
            logger.info(f"Stoppe Ladung: Batterie={battery_level}% oder Strombezug={power_avg_10min}W zu hoch")
            hass.services.call('switch', 'turn_off', {'entity_id': 'switch.garage_mobile_wallbox_switch_0'})
        
        if reduced_charging_state == 'on':
            hass.services.call('switch', 'turn_off', {'entity_id': 'switch.erna_reduced_ac_charging'})
    
    # 2. Starte das Laden mit voller Leistung bei hohem Solarüberschuss
    elif power_avg_10min < -1500 and battery_level < 80:
        logger.info(f"Starte Ladung mit voller Leistung: Solarüberschuss={abs(power_avg_10min)}W, Batterie={battery_level}%")
        hass.services.call('switch', 'turn_on', {'entity_id': 'switch.garage_mobile_wallbox_switch_0'})
        hass.services.call('switch', 'turn_off', {'entity_id': 'switch.erna_reduced_ac_charging'})
    
    # 3. Reduziere Ladeleistung wenn während des Ladens Strom bezogen wird
    elif (power_avg_10min > 0 and power_avg_10min < 1000 and 
          battery_level < 80 and wallbox_power > 50):
        if reduced_charging_state == 'off':
            logger.info(f"Reduziere Ladeleistung: Strombezug={power_avg_10min}W während Ladung aktiv")
            hass.services.call('switch', 'turn_on', {'entity_id': 'switch.erna_reduced_ac_charging'})
    
    # 4. Erhöhe Ladeleistung wieder bei ausreichend Solarüberschuss
    elif (power_avg_10min < -1000 and battery_level < 80 and 
          wallbox_power > 50 and reduced_charging_state == 'on'):
        logger.info(f"Erhöhe Ladeleistung: Solarüberschuss={abs(power_avg_10min)}W ausreichend")
        hass.services.call('switch', 'turn_off', {'entity_id': 'switch.erna_reduced_ac_charging'})
    
    # 5. Schalte Wallbox aus und deaktiviere Solarladung bei zu geringer Leistung
    elif wallbox_power < 50 and wallbox_switch_state == 'on':
        logger.info(f"Stoppe Ladung und deaktiviere Solarladung: Wallbox-Leistung zu gering ({wallbox_power}W < 50W)")
        hass.services.call('switch', 'turn_off', {'entity_id': 'switch.garage_mobile_wallbox_switch_0'})
        hass.services.call('input_boolean', 'turn_off', {'entity_id': 'input_boolean.solarladen_erna'})
    
    else:
        if DEBUG_LOGGING:
            logger.debug(f"Keine Aktion erforderlich - Aktueller Status beibehalten")

# Skript erfolgreich beendet
logger.info("=== Solarladen Erna Skript beendet ===")