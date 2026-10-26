import unittest

from sample_projects.average_bug import calculate_average


class TestCalculateAverage(unittest.TestCase):

    def test_average_of_numbers(self):
        result = calculate_average([10, 20, 30])
        self.assertEqual(result, 20)

    def test_average_with_decimal_result(self):
        result = calculate_average([1, 2])
        self.assertEqual(result, 1.5)

    def test_empty_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_average([])


if __name__ == "__main__":
    unittest.main()