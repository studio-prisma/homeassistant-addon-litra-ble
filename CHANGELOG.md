# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/). Versions up to 0.3.2 are from the
original project, [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt).

## [Unreleased]

## [0.4.2] - 2026-11-01

### Changed

- Protection mode can stay on. `full_access` is replaced by a per-device grant
  for `/dev/hidraw0`–`/dev/hidraw3`. The Supervisor skips the ones that don't
  exist and grants a node that appears later through its hot-plug listener.

## [0.4.1] - 2026-11-01

### Fixed

- Colour temperature had no effect: the light ignores values that are not a
  multiple of 100 K, and Home Assistant's mired conversion produces them
  (2702 K, 6494 K). Values are now rounded to the nearest 100 K.

## [0.4.0] - 2026-11-01

First release of the studio-prisma fork, based on 0.3.2.

### Added

- A plain Litra Beam over Bluetooth is recognised by its kernel HID name and
  driven with the Beam profile.
- Unit tests for address validation, model detection and temperature rounding.

### Changed

- The add-on image is built from the code in this repository. It no longer runs
  `pip install git+…@main` at build time, so a rebuild cannot pull in
  unreviewed upstream changes. `paho-mqtt` is pinned to 2.1.0.
- Auto-discovery only accepts devices whose advertised name starts with `Litra`.
- Add-on renamed to "Litra Bluetooth Bridge" (slug `litra_ble_bridge`). The
  Python package moved into the add-on folder so the local build has it.

### Fixed

- Bluetooth addresses are validated as MAC addresses before they reach the
  interactive `bluetoothctl` session. Before, a value with a newline could
  inject further `bluetoothctl` commands.
- A plain Beam over Bluetooth was either not found at all or driven with the
  Beam LX feature index, so commands had no effect.

[Unreleased]: https://github.com/studio-prisma/homeassistant-addon-litra-ble/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/studio-prisma/homeassistant-addon-litra-ble/releases/tag/v0.4.2
[0.4.1]: https://github.com/studio-prisma/homeassistant-addon-litra-ble/commit/447028a
[0.4.0]: https://github.com/studio-prisma/homeassistant-addon-litra-ble/compare/8f5f9a0...c20fc12
