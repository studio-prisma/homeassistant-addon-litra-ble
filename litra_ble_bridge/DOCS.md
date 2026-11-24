# Litra Bluetooth Bridge

Control one or more Logitech **Litra** lights from Home Assistant over
**Bluetooth** — including the **Litra Beam LX** front light *and* its 7-zone back
RGB strip. Each light shows up as a normal Home Assistant device with light
entities you can use in dashboards, automations, and voice assistants.

This add-on runs on the Home Assistant host's Bluetooth radio, so the host needs
to be within Bluetooth range of the lights.

## Requirements

- The **Mosquitto broker** add-on (or another MQTT broker) installed and started.
  The MQTT integration must be configured (it usually auto-discovers Mosquitto).
  This add-on gets the broker credentials from the Supervisor automatically — you
  do **not** type them anywhere.
- Bluetooth available on the host. The Pi's built-in Bluetooth works; for several
  lights or long range, a dedicated USB Bluetooth dongle is more reliable.
- Protection mode can stay **on**. The add-on is granted `/dev/hidraw0` to
  `/dev/hidraw3` individually; a light that connects after the add-on started
  is granted through the Supervisor's hot-plug listener.
- The light must not be connected to another device (laptop, phone) — a Litra
  keeps one Bluetooth connection at a time.

## Setup

The add-on pairs and trusts only the lights whose address you list. A trusted
Bluetooth HID device can type on the host's console, and any device in radio
range can advertise itself as "Litra…", so nothing is paired by name alone.

1. Find the light's Bluetooth address. Either read it in the Logitech app or on
   another device the light was paired with, or turn on `auto_discover`, put the
   light into pairing mode (hold the Bluetooth button on the back until it
   blinks) and start the add-on: the log lists every Litra it sees, e.g.
   `discovered: Litra Beam LX [AA:BB:CC:DD:EE:01]`.
2. Add the address to `lights`:

   ```yaml
   lights:
     - address: "AA:BB:CC:DD:EE:01"
       name: "Office Litra"
       model: "beam_lx"
   ```

3. Put the light into pairing mode and (re)start the add-on. It pairs, trusts
   and connects it once; after that the light reconnects on its own.

The model (Beam LX / Beam / Glow) is detected automatically when `model` is left
out. Lights that are already bonded but not listed are exposed too, named like
`Litra Beam LX (EE01)` (the suffix is the tail of the address, so two identical
models don't clash). Rename them in Home Assistant to taste.

### Pairing discovered lights automatically (opt-in)

With `auto_discover` **and** `pair_discovered` on, the add-on pairs and trusts
every device that advertises a name starting with "Litra", as versions before
0.5.0 did. Devices that announce themselves as a keyboard or mouse are refused,
but a device can lie about that. Only use it where no stranger is in Bluetooth
range, and turn it off again after the first pairing.

### Upgrading from 0.4.x

Lights that are already paired keep working without any change. To pair a new
light, list its address as above.

Option reference:

| Option | Meaning |
|---|---|
| `lights[].address` | A light's Bluetooth MAC, `AA:BB:CC:DD:EE:FF`. Only listed addresses are paired. |
| `lights[].name` | Friendly name shown in Home Assistant. |
| `lights[].model` | `beam_lx` (front + back RGB), `beam` or `glow` (front only). |
| `auto_discover` | Scan for advertising Litras and log their addresses. Pairs nothing by itself. Default `false`. |
| `pair_discovered` | Also pair and trust what `auto_discover` found. Default `false`. |
| `pair_on_start` | Pair/trust the listed addresses on startup. Leave `true`. |
| `state_readback` | Poll the device for real state (also catches the physical buttons) at the cost of extra Bluetooth traffic. |
| `scan_seconds` | How long to scan for lights. |
| `presence_interval` | Seconds between availability checks. |
| `log_level` | `debug`, `info`, `warning`, `error`. |

## Start it

Start the add-on and watch the log. You're looking for:

```
pairing 1 light(s)...
bridging 1 light(s): Office Litra
connected to MQTT broker
published discovery for Office Litra (front+back)
```

Each light then appears in **Settings → Devices & Services → MQTT** as a device
with **Front** and **Back RGB** light entities.

## Using the lights

The entities are standard Home Assistant lights:

- **Front** — on/off, brightness, colour temperature (2700–6500 K).
- **Back RGB** — on/off, brightness, RGB colour (all 7 zones, changed together).

Use them in automations ("front light to 4500 K at 30% on weekday mornings"),
dashboards, or voice ("turn on the Office Litra").

## Troubleshooting

- **A light won't pair:** make sure its address is listed in `lights`, and that
  it's in pairing mode (blinking) and in range the first time you start the
  add-on. Increase `scan_seconds`. A log line *not pairing … discovered
  device(s)* means the light was seen but isn't listed. Check the log
  with `log_level: debug` for the `bluetoothctl` transcript.
- **Entity shows "unavailable":** the light is asleep/out of range, or the bond
  dropped. It returns automatically when the light reconnects.
- **No entities at all:** confirm the Mosquitto add-on is running and the MQTT
  integration is set up; the log should say *connected to MQTT broker*.
- **Bluetooth conflicts:** if you also use Home Assistant's Bluetooth integration
  on the same adapter and see instability, add a dedicated USB Bluetooth dongle
  for the lights.

## How it works

The Litra speaks a Logitech vendor HID protocol over Bluetooth (HID-over-GATT).
Once bonded, the kernel exposes each light as a `/dev/hidraw` device; the add-on
writes 20-byte control reports to it and publishes/subscribes MQTT topics that
Home Assistant understands via MQTT discovery. Protocol credit:
[timrogers/litra](https://github.com/timrogers/litra) (USB); this project
re-applies it over Bluetooth.
