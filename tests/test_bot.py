import unittest

from bot import build_message


class BotTests(unittest.TestCase):
    def test_build_message_contains_name(self):
        self.assertEqual(build_message("Kir"), "Hello, Kir! Your Roblox bot is ready.")


if __name__ == "__main__":
    unittest.main()
