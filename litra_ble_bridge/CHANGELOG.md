# Changelog

## 0.4.0

Fork by studio-prisma of [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt) 0.3.2.

- The add-on image is built from the reviewed code in this folder. It no longer
  runs `pip install git+…@main` at build time, so a rebuild can't pull in
  unreviewed upstream changes. `paho-mqtt` is pinned to 2.1.0.
- Bluetooth addresses are validated as MAC addresses before they reach the
  interactive `bluetoothctl` session; anything else is refused instead of being
  written to its stdin.
- Auto-discovery only accepts devices whose advertised name starts with
  "Litra".
- A plain Litra Beam over Bluetooth is now recognised by its kernel HID name and
  driven with the Beam profile. Before, its unknown product id was either
  skipped or fell back to the Beam LX profile and its wrong feature index.
- Add-on renamed to "Litra Bluetooth Bridge" (slug `litra_ble_bridge`); the
  Python package moved into the add-on folder so the local build has it.

## 0.3.2

- Wait for the kernel hidraw node to appear after bonding (it can lag a few
  seconds behind connect) instead of giving up immediately.
- When a light bonds but no HID device shows up, log diagnostics (bluetoothctl
  info + hidraw/sys state) to pinpoint the cause.

## 0.3.1

- More reliable pairing: keep the BLE scan running *through* the pair attempt
  (turning it off first could drop the device and fail the bond), retry a
  couple of times, and longer waits — BLE bonding over a rotating random
  address is flaky.
- Default scan time raised 8s → 20s (configurable up to 60s).
- On a failed pairing, the relevant `bluetoothctl` output is now logged so the
  cause (e.g. AuthenticationFailed, out of range) is visible.

## 0.3.0

- **Auto-discovery**: with `auto_discover` on (default), the add-on scans for
  Litra lights in pairing mode, bonds them, and exposes every connected Litra
  with its model detected automatically — no need to find or type MAC addresses.
- The `lights` list is now optional (use it only to pin names/models or to
  control exactly which lights are exposed).

## 0.2.0

- Initial add-on release.
- Multi-light support: configure any number of Litra lights by Bluetooth address.
- Litra Beam LX front light (brightness + colour temperature) and 7-zone back
  RGB strip as separate Home Assistant light entities.
- Older models (`beam`, `glow`) supported as front-light-only.
- Automatic pairing/trusting of configured lights on startup.
- MQTT broker details obtained from the Supervisor (no manual credentials).
- Per-light availability with bridge-wide last-will for crash detection.
