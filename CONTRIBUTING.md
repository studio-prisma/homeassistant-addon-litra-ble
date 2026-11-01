# Contributing

Thanks for taking the time. This project is small and maintained in spare time. The rules below exist so a pull request can be reviewed in one sitting.

## Before you open a pull request

- Open an issue first for anything beyond a typo.
- One change per PR. A refactor bundled with a fix is two PRs.
- Security issues never go into a public PR or issue. See [SECURITY.md](SECURITY.md).
- Changes that also make sense for the original project are welcome upstream at [Alevale/litra-ble-mqtt](https://github.com/Alevale/litra-ble-mqtt).

## Development setup

```bash
git clone https://github.com/studio-prisma/homeassistant-addon-litra-ble.git
cd homeassistant-addon-litra-ble
python3 -m pip install pyyaml
```

The Python package lives in `litra_ble_bridge/litra_ble/` so the add-on can build it from its own folder. `pip install .` and `python3 litra.py` still work from the repository root.

## What a change has to pass

```bash
bash tests/run-all.sh
```

CI runs the same checks on every push and pull request, on Python 3.9 and 3.12. The aggregating job is called **Gate**. It is the only status check the branch protection requires, and it is green only when every other job is.

A red pipeline is not mergeable. If a check fails for a reason unrelated to your change, say so in the PR instead of rerunning until it passes.

Unit tests cannot cover Bluetooth or a real light. A change to the HID protocol or to pairing needs a note in the PR on which model and connection you tested it with.

## Code conventions

- Match the surrounding style.
- No new runtime dependency without a reason in the PR description. The image installs exactly one, pinned.
- Nothing is fetched at image build time except that pinned dependency.
- Comments explain *why*, not *what*.
- No real Bluetooth addresses, hostnames or IPs in code, tests or docs. Use `AA:BB:CC:DD:EE:FF`, `example.com`, `192.0.2.0/24`.

## Documentation

- Behaviour change → update `README.md` **and** `README.de.md` in the same PR.
- Add-on option or permission change → update `litra_ble_bridge/DOCS.md` as well.
- New limitation discovered → add it to "Known limitations".

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/), imperative, English:

```
fix(pairing): refuse addresses that are not a MAC
feat(device): recognise a plain Beam over Bluetooth by its HID name
docs(readme): document the per-device hidraw grant
```

## Release process

Maintainer only.

1. `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md`, add a fresh empty `Unreleased` block, and add the same version to `litra_ble_bridge/CHANGELOG.md` (Home Assistant shows that one)
2. bump the version in `litra_ble_bridge/config.yaml` and `pyproject.toml`; the release workflow refuses a tag that disagrees with either
3. `git commit -m "chore(release): vX.Y.Z"`, merge via PR
4. `git tag -a vX.Y.Z -m "vX.Y.Z"` from the merged `main`, push the tag
5. the release workflow publishes the notes from `CHANGELOG.md`

Tags are protected. A wrong tag is corrected with the next patch version, never by overwriting.

## License

By contributing you agree that your contribution is licensed under the [MIT License](LICENSE).
