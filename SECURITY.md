# Security Policy

## Supported Versions

Only the latest minor release receives security fixes.

| Version | Supported |
|---|---|
| `0.4.x` | yes |
| everything older | no |

## Reporting a Vulnerability

Use **[GitHub Security Advisories](https://github.com/studio-prisma/homeassistant-addon-litra-ble/security/advisories/new)**, which are private by default. Do not open a public issue for a suspected vulnerability.

Include:

- add-on version, Home Assistant version and host platform
- what an attacker gains, not only what misbehaves
- reproduction steps, ideally against a clean install

Expected response: an acknowledgement within 7 days, an assessment within 30. This is a spare-time project, not a vendor with an on-call rotation.

## What the add-on can reach

Knowing the surface helps decide whether something is a finding:

- **Host BlueZ over D-Bus** (`host_dbus`), used to pair, trust and connect lights.
- **`/dev/hidraw0`–`/dev/hidraw3`**, granted per device, so Protection mode stays on. Any HID device the kernel puts on those nodes is reachable, not only a Litra.
- **The MQTT broker**, with credentials the Supervisor provides.
- No inbound network port, no web UI, no cloud connection.

## In Scope

- text reaching the interactive `bluetoothctl` session that is not a validated MAC address (command injection into BlueZ)
- MQTT payloads that crash the bridge or make it write HID reports other than the documented power, brightness, temperature and colour commands
- auto-discovery pairing a device whose advertised name does not start with `Litra`
- the image build fetching code that is not in this repository, other than the pinned `paho-mqtt`
- MQTT credentials leaking into logs

## Out of Scope

Documented design decisions are not findings.

- **Bluetooth security of the light itself.** Pairing uses `NoInputNoOutput` (Just Works); the light offers nothing stronger.
- **Anyone who can publish to the MQTT command topics can switch the light.** Access control belongs to the broker.
- **Auto-discovery pairs any nearby device that advertises as `Litra…` while the add-on starts.** Turn `auto_discover` off and list addresses if that matters in your environment.
- other HID devices on `hidraw0`–`3` being reachable by the add-on (see above)
- issues in Home Assistant, the Supervisor or BlueZ: report those upstream
- anything that requires an already-compromised host or admin account

## Handling of Secrets

No credentials belong in this repository: not in tests, not commented out, not in fixtures. A secret that reached a commit is rotated first and removed second.

## Disclosure

Coordinated. A fix ships first, the advisory follows once a patched release is available. Reporters are credited unless they ask not to be.
