import unittest
from app.municipalities.schedule_helpers import get_simple_day, get_sublist

class DownTest(unittest.TestCase):

    def test_normal(self):
        days_to_pickup = get_simple_day(1, (0, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (0, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (0, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (0, 0, 0), [2, 4], "DOWN")
        self.assertEqual(days_to_pickup, 1)

    def test_this_week(self):
        days_to_pickup = get_simple_day(1, (1, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 2)

        days_to_pickup = get_simple_day(2, (1, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (3, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (1, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (1, 0, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(3, (1, 0, 0), [2, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

    def test_next_week(self):
        days_to_pickup = get_simple_day(1, (1, 1, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 2)

        days_to_pickup = get_simple_day(2, (1, 1, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(5, (3, 1, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(6, (1, 1, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(5, (1, 1, 0), [2, 3, 4], "DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(6, (1, 1, 0), [4], "DOWN")
        self.assertEqual(days_to_pickup, 6)

class UpTest(unittest.TestCase):

    def test_normal(self):
        days_to_pickup = get_simple_day(1, (0, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (0, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (0, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (0, 0, 0), [2, 4], "UP")
        self.assertEqual(days_to_pickup, 1)

    def test_this_week(self):
        days_to_pickup = get_simple_day(1, (1, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (2, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (3, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (1, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (1, 0, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (4, 0, 0), [2, 4], "UP")
        self.assertEqual(days_to_pickup, 0)

    def test_next_week(self):
        days_to_pickup = get_simple_day(1, (1, 1, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (2, 1, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(5, (3, 1, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(6, (1, 1, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 3)

        days_to_pickup = get_simple_day(5, (1, 2, 0), [2, 3, 4], "UP")
        self.assertEqual(days_to_pickup, 3)

        days_to_pickup = get_simple_day(6, (1, 4, 0), [4], "UP")
        self.assertEqual(days_to_pickup, 4)

class SkipTest(unittest.TestCase):

    def test_normal(self):
        days_to_pickup = get_simple_day(1, (0, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (0, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (0, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (0, 0, 0), [2, 4], "SKIP")
        self.assertEqual(days_to_pickup, 1)

    def test_this_week(self):
        days_to_pickup = get_simple_day(1, (1, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (1, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (3, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (4, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 5)

        days_to_pickup = get_simple_day(5, (1, 0, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (1, 0, 0), [2, 4], "SKIP")
        self.assertEqual(days_to_pickup, 1)

    def test_next_week(self):
        days_to_pickup = get_simple_day(1, (1, 1, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (1, 1, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (3, 2, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 5)

        days_to_pickup = get_simple_day(6, (1, 3, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 3)

        days_to_pickup = get_simple_day(5, (1, 1, 0), [2, 3, 4], "SKIP")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(6, (1, 1, 0), [4], "SKIP")
        self.assertEqual(days_to_pickup, 5)

class SkipDownTest(unittest.TestCase):

    def test_normal(self):
        days_to_pickup = get_simple_day(1, (0, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (0, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (0, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (0, 0, 0), [2, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 1)

    def test_this_week(self):
        days_to_pickup = get_simple_day(1, (1, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (1, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (2, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(4, (1, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (4, 0, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (1, 0, 0), [2, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 1)

    def test_next_week(self):
        days_to_pickup = get_simple_day(1, (4, 1, 0), [4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 10)

        days_to_pickup = get_simple_day(1, (4, 4, 0), [4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(5, (3, 1, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(6, (1, 1, 0), [2, 3, 4], "SKIP_DOWN")
        self.assertEqual(days_to_pickup, 3)

        with self.assertRaises(ValueError): 
            days_to_pickup = get_simple_day(6, (4, 4, 4), [4], "SKIP_DOWN")

class InnerTest(unittest.TestCase):

    def test_normal(self):
        days_to_pickup = get_simple_day(1, (0, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(2, (0, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (0, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (0, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 4)

        days_to_pickup = get_simple_day(3, (0, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 1)

        with self.assertRaises(ValueError): 
            days_to_pickup = get_simple_day(3, (1, 0, 0), [2, 3, 4], "INNER")

        with self.assertRaises(ValueError): 
            days_to_pickup = get_simple_day(3, (0, 0, 0), [2, 3, 4], "INNER")

    def test_this_week(self):
        days_to_pickup = get_simple_day(1, (1, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 2)

        days_to_pickup = get_simple_day(2, (1, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 1)

        days_to_pickup = get_simple_day(2, (3, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(4, (1, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(5, (4, 0, 0), [4, 5], "INNER")
        self.assertEqual(days_to_pickup, 0)

        days_to_pickup = get_simple_day(3, (1, 0, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 0)

    def test_next_week(self):
        days_to_pickup = get_simple_day(1, (1, 1, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 2)

        days_to_pickup = get_simple_day(5, (1, 1, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 5)

        days_to_pickup = get_simple_day(5, (0, 1, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 5)

        days_to_pickup = get_simple_day(6, (1, 4, 0), [2, 4], "INNER")
        self.assertEqual(days_to_pickup, 3)

        days_to_pickup = get_simple_day(5, (1, 2, 0), [1, 2, 4], "INNER")
        self.assertEqual(days_to_pickup, 3)

        days_to_pickup = get_simple_day(6, (1, 1, 0), [4], "INNER")
        self.assertEqual(days_to_pickup, 5)

class SublistTest(unittest.TestCase):

    def test_sublist(self):
        sublist = get_sublist(3, [1, 2, 3, 4, 5, 6], "LT")
        self.assertEqual(sublist, [1, 2])
        sublist = get_sublist(3, [1, 2, 3, 4, 5, 6], "LE")
        self.assertEqual(sublist, [1, 2, 3])

        sublist = get_sublist(3, [1, 2, 3, 4, 5, 6], "GE")
        self.assertEqual(sublist, [3, 4, 5, 6])

        sublist = get_sublist(3, [1, 2, 3, 4, 5, 6], "GT")
        self.assertEqual(sublist, [4, 5, 6])

        sublist = get_sublist(3, [1, 2, 3, 4, 5, 6], "gt")
        self.assertEqual(sublist, [4, 5, 6])

        sublist = get_sublist(3, [], "GT")
        self.assertEqual(sublist, [])

        sublist = get_sublist(3, [1, 2, 3], "GT")
        self.assertEqual(sublist, [])

        with self.assertRaises(ValueError):
            sublist = get_sublist(3, [1, 2, 3], "EQ")

if __name__ == '__main__':
    unittest.main()
