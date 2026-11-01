## What changes

<!-- One or two sentences. What does this PR do, and why? -->

## Type

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] CI / tooling
- [ ] Refactor (no behaviour change)

## Security impact

- [ ] Touches what reaches `bluetoothctl` (addresses, commands)
- [ ] Touches add-on permissions in `config.yaml` (devices, D-Bus, full access)
- [ ] Touches how the image is built (`Dockerfile`, pinned dependencies)
- [ ] No security-relevant surface touched

If any box above is checked, describe the change to the threat model:

<!-- ... -->

## Verification

- [ ] `tests/run-all.sh` passes locally (state your Python version: ______)
- [ ] Tested against a real light (model and connection: ______)
- [ ] No hardcoded hostnames, Bluetooth addresses, credentials, or absolute paths added

## Related issues

Closes #
