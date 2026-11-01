# Litra Bluetooth Bridge für Home Assistant

[English](README.md)

Steuert Logitech-Litra-Lampen (Beam, Beam LX, Glow) aus Home Assistant per **Bluetooth**, ohne Logitech-Software und ohne Cloud. Jede Lampe erscheint über MQTT-Discovery als normales Licht in Home Assistant.

Das ist der studio-prisma-Fork von [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt). Er unterscheidet sich in vier Punkten:

- **Eine normale Litra Beam funktioniert per Bluetooth.** Das Original kannte nur ihre USB-Kennung. Die Lampe wurde deshalb nicht gefunden oder bekam die Befehle der Beam LX.
- **Die Farbtemperatur funktioniert.** Werte werden auf 100 K gerundet, andere ignoriert die Lampe.
- **Der Schutzmodus bleibt an.** Der Zugriff auf die HID-Geräte wird gezielt pro Gerät freigegeben statt über vollen Gerätezugriff.
- **Das Image wird aus diesem Repository gebaut.** Beim Build wird außer einer festgelegten Abhängigkeit nichts nachgeladen, und Bluetooth-Adressen werden geprüft, bevor sie `bluetoothctl` erreichen.

## Voraussetzungen

- Home Assistant OS oder Supervised, mit Bluetooth auf dem Host in Reichweite der Lampen. Getestet auf einem Raspberry Pi 4 mit eingebautem Adapter.
- Das Add-on **Mosquitto broker** (oder ein anderer MQTT-Broker) und die MQTT-Integration. Die Zugangsdaten zum Broker holt sich das Add-on vom Supervisor.
- Eine Litra Beam, Beam LX oder Glow. Getestet: **Litra Beam per Bluetooth**. Beam LX und Glow stammen aus dem Original-Projekt und sind hier nicht erneut getestet.

## Installation

1. **Einstellungen → Apps (früher Add-ons) → App Store → ⋮ → Repositories**, hinzufügen:
   `https://github.com/studio-prisma/homeassistant-addon-litra-ble`.
2. **Litra Bluetooth Bridge** installieren. Den Schutzmodus anlassen.
3. Die Lampe an allen anderen Geräten entkoppeln (Laptop, Handy). Eine Litra hält immer nur eine Bluetooth-Verbindung.
4. Die Bluetooth-Taste auf der Rückseite gedrückt halten, bis die Lampe blinkt.
5. Das Add-on starten. Es sucht 20 Sekunden lang, koppelt die Lampe und meldet sie an Home Assistant.

Die Lampe erscheint als `light.litra_beam_<kürzel>_front` (bei der Beam LX zusätzlich `_back`). Nach der ersten Kopplung verbindet sie sich von selbst neu.

## Einstellungen

| Option | Standard | Bedeutung |
|---|---|---|
| `auto_discover` | `true` | Beim Start jedes Gerät in der Nähe koppeln, das sich als `Litra…` meldet. |
| `lights` | `[]` | Adressen, Namen oder Modelle fest vorgeben statt automatischer Suche. |
| `pair_on_start` | `true` | Konfigurierte oder gefundene Lampen beim Start koppeln und als vertrauenswürdig markieren. |
| `state_readback` | `false` | Den echten Zustand der Lampe zurücklesen. Aus heißt: Home Assistant zeigt den zuletzt gesendeten Befehl. |
| `scan_seconds` | `20` | Wie lange nach Lampen im Kopplungsmodus gesucht wird. |
| `presence_interval` | `5` | Sekunden zwischen den Verfügbarkeitsprüfungen. |

Details: [`litra_ble_bridge/DOCS.md`](litra_ble_bridge/DOCS.md).

## Bekannte Grenzen

- **Der Zustand ist standardmäßig angenommen.** Mit `state_readback` aus sieht Home Assistant nicht, wenn die Lampe über ihre eigenen Tasten geschaltet wird.
- **Vier hidraw-Plätze.** Freigegeben sind `/dev/hidraw0` bis `/dev/hidraw3`. Hat der Host mehr HID-Geräte, kann die Lampe eine höhere Nummer bekommen. Dann kann das Add-on sie nicht öffnen.
- **Eine Verbindung pro Lampe.** Solange das Add-on die Lampe hält, kann die Logitech-App auf einem anderen Gerät sie nicht steuern.
- **Die Bluetooth-Produktkennung der Beam ist noch nicht fest hinterlegt.** Erkannt wird die Lampe über ihren Kernel-Namen (`Litra Beam`). Ein umbenanntes oder ungewöhnliches Gerät wird übersprungen statt geraten.

## Eigenständige Bridge und Kommandozeile

Die Bridge läuft auch außerhalb von Home Assistant (systemd auf jedem Linux-Rechner mit Bluetooth), und es gibt das Kommandozeilen-Werkzeug `litra`. Beides ist unverändert aus dem Original-Projekt, siehe dessen [README](https://github.com/Alevale/litra-ble-mqtt#standalone-setup-systemd) und [`docs/MQTT.md`](docs/MQTT.md). Aus diesem Repository: `python3 litra.py <befehl>` oder `pip install .`.

## Danksagung

- [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt): die Bluetooth-Bridge und das Home-Assistant-Add-on, auf denen dieser Fork aufbaut.
- [timrogers/litra](https://github.com/timrogers/litra) und [litra-rs](https://github.com/timrogers/litra-rs): das nachgebaute HID-Protokoll. Siehe [`docs/PROTOCOL.md`](docs/PROTOCOL.md).

## Lizenz

MIT, siehe [LICENSE](LICENSE).
