"""Unit tests for the logic this fork changed. No Bluetooth or MQTT needed."""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "litra_ble_bridge"))

from litra_ble import device, pairing  # noqa: E402


class ValidAddressTest(unittest.TestCase):
    def test_accepts_mac_in_either_case(self):
        self.assertTrue(pairing.valid_address("AA:BB:CC:DD:EE:FF"))
        self.assertTrue(pairing.valid_address("aa:bb:cc:dd:ee:ff"))

    def test_rejects_anything_that_could_reach_bluetoothctl_stdin(self):
        for bad in ("", None, "AA:BB:CC:DD:EE", "AA:BB:CC:DD:EE:FF\nremove all",
                    "AA:BB:CC:DD:EE:FF ", "pair AA:BB:CC:DD:EE:FF"):
            self.assertFalse(pairing.valid_address(bad), repr(bad))

    def test_pair_refuses_invalid_address_without_calling_bluetoothctl(self):
        with mock.patch.object(pairing, "_oneshot") as oneshot, \
                mock.patch.object(pairing, "_Session") as session:
            self.assertFalse(pairing.pair("not-a-mac\nremove all"))
            oneshot.assert_not_called()
            session.assert_not_called()


CONFIGURED = "AA:BB:CC:DD:EE:01"
FOUND = "AA:BB:CC:DD:EE:02"


class SelectPairTargetsTest(unittest.TestCase):
    """LI-1: only configured lights are paired unless the user opts in."""

    def select(self, configured, discovered, pair_on_start=True,
               pair_discovered=False, is_input=lambda a: False):
        return pairing.select_pair_targets(
            configured, discovered, pair_on_start=pair_on_start,
            pair_discovered=pair_discovered, is_input_device=is_input)

    def test_discovered_device_is_not_paired_by_default(self):
        self.assertEqual(self.select([], [FOUND]), [])

    def test_only_the_configured_address_is_paired(self):
        self.assertEqual(self.select([CONFIGURED], [FOUND]), [CONFIGURED])

    def test_pair_on_start_off_pairs_nothing(self):
        self.assertEqual(self.select([CONFIGURED], [FOUND], pair_on_start=False), [])

    def test_opt_in_pairs_discovered_devices(self):
        self.assertEqual(self.select([CONFIGURED], [FOUND], pair_discovered=True),
                         [CONFIGURED, FOUND])

    def test_opt_in_still_refuses_keyboards(self):
        self.assertEqual(self.select([], [FOUND], pair_discovered=True,
                                     is_input=lambda a: True), [])

    def test_invalid_addresses_never_become_targets(self):
        bad = "AA:BB:CC:DD:EE:FF\nremove all"
        self.assertEqual(self.select([bad], [bad], pair_discovered=True), [])


class AnnouncesInputDeviceTest(unittest.TestCase):
    def check(self, info):
        with mock.patch.object(pairing, "_oneshot", return_value=info):
            return pairing.announces_input_device(FOUND)

    def test_keyboard_appearance_and_icon(self):
        self.assertTrue(self.check("\tAppearance: 0x03c1\n"))
        self.assertTrue(self.check("\tIcon: input-keyboard\n"))
        self.assertTrue(self.check("\tIcon: input-mouse\n"))

    def test_light_or_unknown_is_not_flagged(self):
        self.assertFalse(self.check("\tName: Litra Beam LX\n\tPaired: no\n"))
        self.assertFalse(self.check("\tAppearance: 0x03c0\n"))
        self.assertFalse(self.check("\tAppearance: garbage\n"))
        self.assertFalse(self.check(""))


class AddonOptionsTest(unittest.TestCase):
    """LI-3: addresses are validated when the options are loaded."""

    def load(self, options):
        from litra_ble import config
        with mock.patch.object(config, "_supervisor_mqtt", return_value=None):
            return config._from_addon(options)

    def test_defaults_pair_nothing_discovered(self):
        cfg = self.load({})
        self.assertFalse(cfg.auto_discover)
        self.assertFalse(cfg.pair_discovered)

    def test_invalid_address_is_rejected(self):
        with self.assertLogs("litra-mqtt.config", level="ERROR"):
            cfg = self.load({"lights": [{"address": "AA:BB:CC:DD:EE:01\nremove all"},
                                        {"address": "not-a-mac"}]})
        self.assertEqual(cfg.lights, [])

    def test_valid_address_is_kept_and_normalised(self):
        cfg = self.load({"lights": [{"address": " aa:bb:cc:dd:ee:01 "}]})
        self.assertEqual([l.address for l in cfg.lights], [CONFIGURED])


class ModelFromNameTest(unittest.TestCase):
    def test_known_models(self):
        self.assertEqual(device._model_from_name("Litra Beam LX"), "beam_lx")
        self.assertEqual(device._model_from_name("Litra Beam"), "beam")
        self.assertEqual(device._model_from_name("Litra Glow"), "glow")

    def test_unknown_names_are_skipped_not_guessed(self):
        self.assertIsNone(device._model_from_name("Litra Something"))
        self.assertIsNone(device._model_from_name("Keyboard"))
        self.assertIsNone(device._model_from_name(""))


class TemperatureTest(unittest.TestCase):
    def sent_kelvin(self, kelvin):
        light = device.LitraLight(model="beam")
        with mock.patch.object(light, "_write") as write:
            light.front_temperature(kelvin)
        payload = write.call_args.args
        self.assertEqual(payload[:4], (0x11, 0xFF, 0x04, 0x9C))
        return (payload[4] << 8) | payload[5]

    def test_rounds_to_100_k(self):
        # Values Home Assistant produces after its mired round-trip.
        self.assertEqual(self.sent_kelvin(2702), 2700)
        self.assertEqual(self.sent_kelvin(6494), 6500)
        self.assertEqual(self.sent_kelvin(4049), 4000)

    def test_clamps_to_range(self):
        self.assertEqual(self.sent_kelvin(1000), 2700)
        self.assertEqual(self.sent_kelvin(9000), 6500)


if __name__ == "__main__":
    unittest.main()
