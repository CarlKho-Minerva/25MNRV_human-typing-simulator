import unittest
from src.utils import generate_delay

class TestUtils(unittest.TestCase):
    def test_generate_delay_typical(self):
        delay = generate_delay(300, 30, 100)
        self.assertTrue(delay > 0)
        self.assertIsInstance(delay, float)

    def test_generate_delay_ultrafast(self):
        delay = generate_delay(2_000_000, 0, 100)
        self.assertAlmostEqual(delay, 0.001)

if __name__ == "__main__":
    unittest.main()
