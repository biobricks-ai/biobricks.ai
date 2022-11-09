import unittest

class TestDie(unittest.TestCase):
    def setUp(self):
        self.die = 2

    def test_upper(self):
        self.assertEqual(self.die, 2)