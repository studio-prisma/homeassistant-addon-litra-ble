# Litra Bluetooth Bridge for Home Assistant

[Deutsch](README.de.md)

Control Logitech Litra lights (Beam, Beam LX, Glow) from Home Assistant over **Bluetooth**, without Logitech's software and without a cloud. Each light appears as a normal Home Assistant light through MQTT discovery.

This is the studio-prisma fork of [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt). It differs in five ways:

- **A plain Litra Beam works over Bluetooth.** The original only knew its USB id, so the light was either not found or sent the Beam LX command set.
- **Colour temperature works.** Values are rounded to 100 K; the light ignores anything else.
- **Protection mode stays on.** Raw HID access is granted per device instead of through full access.
- **The image is built from this repository.** Nothing is fetched at build time except one pinned dependency, and Bluetooth addresses are validated before they reach `bluetoothctl`.
- **Nothing is paired by name alone.** Only lights whose address you list are paired and trusted. The original paired any device in range that advertised as `Litra…`, and a trusted Bluetooth HID device can type on the host.

## Requirements

- Home Assistant OS or Supervised, with Bluetooth on the host in range of the lights. Tested on a Raspberry Pi 4 with its built-in adapter.
- The **Mosquitto broker** add-on (or another MQTT broker) and the MQTT integration. The add-on takes the broker credentials from the Supervisor.
- A Litra Beam, Beam LX or Glow. Tested: **Litra Beam over Bluetooth**. Beam LX and Glow come from the original project and are not re-tested here.

## Installation

1. **Settings → Apps (formerly Add-ons) → App Store → ⋮ → Repositories**, add
   `https://github.com/studio-prisma/homeassistant-addon-litra-ble`.
2. Install **Litra Bluetooth Bridge**. Leave Protection mode on.
3. Remove the light from any other device it is paired with (laptop, phone). A Litra keeps one Bluetooth connection at a time.
4. Add the light's Bluetooth address to `lights` in the add-on configuration. If you don't know it, turn on `auto_discover`, put the light in pairing mode and start the add-on once: the log lists the address of every Litra it sees.
5. Hold the Bluetooth button on the back of the light until it blinks.
6. Start the add-on. It pairs the listed light and publishes it to Home Assistant.

The light shows up as `light.litra_beam_<suffix>_front` (plus `_back` on a Beam LX). After the first pairing it reconnects on its own.

## Configuration

| Option | Default | Meaning |
|---|---|---|
| `lights` | `[]` | Addresses (and optionally names, models) of the lights to pair. Only these are paired. |
| `auto_discover` | `false` | Scan for advertising Litras and log their addresses. Pairs nothing by itself. |
| `pair_discovered` | `false` | Also pair and trust every discovered `Litra…` device (behaviour before 0.5.0). Keyboards and mice are refused. |
| `pair_on_start` | `true` | Pair and trust the listed lights on start. |
| `state_readback` | `false` | Read the light's real state back. Off means Home Assistant shows the last command. |
| `scan_seconds` | `20` | How long to scan for lights in pairing mode. |
| `presence_interval` | `5` | Seconds between availability checks. |

Details: [`litra_ble_bridge/DOCS.md`](litra_ble_bridge/DOCS.md).

## Known limitations

- **State is assumed by default.** With `state_readback` off, a change made on the light's own buttons is not reflected in Home Assistant.
- **Four hidraw slots.** Access is granted to `/dev/hidraw0`–`/dev/hidraw3`. A host with more HID devices than that may put the light on a higher number; the add-on then cannot open it.
- **One connection per light.** While the add-on holds the light, the Logitech app on another device cannot control it.
- **The Beam's Bluetooth product id is not pinned yet.** The light is recognised by its kernel name (`Litra Beam`). A renamed or unusual device name is skipped rather than guessed.

## Standalone bridge and CLI

The bridge also runs outside Home Assistant (systemd on any Linux box with Bluetooth), and there is a `litra` command-line tool. Both are unchanged from the original project; see its [README](https://github.com/Alevale/litra-ble-mqtt#standalone-setup-systemd) and [`docs/MQTT.md`](docs/MQTT.md). From this repository, use `python3 litra.py <command>` or `pip install .`.

## Credits

- [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt): the Bluetooth bridge and Home Assistant add-on this fork is based on.
- [timrogers/litra](https://github.com/timrogers/litra) and [litra-rs](https://github.com/timrogers/litra-rs): the reverse-engineered HID protocol. See [`docs/PROTOCOL.md`](docs/PROTOCOL.md).

## License

MIT, see [LICENSE](LICENSE).
