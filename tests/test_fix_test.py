import unittest

from sample_projects.fix_test import get_first_item


class TestFixExample(unittest.TestCase):

    def test_returns_first_item(self):
        self.assertEqual(get_first_item([10, 20, 30]), 10)

    def test_empty_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_first_item([])


if __name__ == "__main__":
    unittest.main()