import unittest

from sample_projects.buggy_example import get_first_item


class TestGetFirstItem(unittest.TestCase):

    def test_returns_first_item(self):
        self.assertEqual(get_first_item([10, 20, 30]), 10)

    def test_negative_number_is_valid_data(self):
        self.assertEqual(get_first_item([-1, 2, 3]), -1)

    def test_empty_list_has_clear_error(self):
        with self.assertRaisesRegex(
            ValueError, "items cannot be empty"
        ):
            get_first_item([])


if __name__ == "__main__":
    unittest.main()