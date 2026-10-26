import unittest

from sample_projects.division_demo import safe_divide


class TestSafeDivide(unittest.TestCase):

    def test_normal_division(self):
        self.assertEqual(safe_divide(10, 2), 5.0)

    def test_decimal_division(self):
        self.assertEqual(safe_divide(7, 2), 3.5)

    def test_zero_denominator_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "division by zero is not allowed",
        ):
            safe_divide(10, 0)


if __name__ == "__main__":
    unittest.main()