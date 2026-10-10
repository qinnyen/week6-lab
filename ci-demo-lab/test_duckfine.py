import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_initial_state(self):
        fine = DuckFine("member-42")

        self.assertEqual(fine.member_id, "member-42")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_within_grace_period_is_zero(self):
        fine = DuckFine("member-42")

        result = fine.charge(2)

        self.assertEqual(result, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_after_grace_period_uses_daily_fee(self):
        fine = DuckFine("member-42")

        result = fine.charge(5)

        self.assertEqual(result, 1.5)
        self.assertEqual(fine.total_owed, 0.0)

    def test_deluxe_charge_doubles_fee_before_capping(self):
        fine = DuckFine("member-42")

        result = fine.charge(20, deluxe=True)

        self.assertEqual(result, 5.0)
        self.assertEqual(fine.total_owed, 5.0)

    def test_negative_days_raise_value_error(self):
        fine = DuckFine("member-42")

        with self.assertRaises(ValueError):
            fine.charge(-1)

    def test_deluxe_charge_accumulates_total_owed(self):
        fine = DuckFine("member-42")

        first = fine.charge(3, deluxe=True)
        second = fine.charge(5, deluxe=True)

        self.assertEqual(first, 1.0)
        self.assertEqual(second, 3.0)
        self.assertEqual(fine.total_owed, 4.0)


if __name__ == "__main__": # pragma: no cover
    unittest.main()
