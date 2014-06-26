import unittest
from eradate import EraDate

class EraDateTest(unittest.TestCase):
    def setUp(self):
        super(EraDateTest, self).setUp()
        self.dateliteral_bc_lower = "3000-05-20 BC"
        self.dateliteral_bc_higher = "0009-10-19 BC"
        self.dateliteral_ad = "0085-06-03"
        self.date_values_bc_lower = (-3000, 5, 20)

    def test_custom_date_class(self):
        date_bc_lower = EraDate.parse_from_db_literal(self.dateliteral_bc_lower)
        date_bc_higher = EraDate.parse_from_db_literal(self.dateliteral_bc_higher)
        date_ad = EraDate.parse_from_db_literal(self.dateliteral_ad)
        date_bc_lower_from_values = EraDate(*self.date_values_bc_lower)

        # Check coorect object type
        self.assertEqual(type(date_bc_lower), EraDate)

        # Check correct representation
        self.assertEqual(date_bc_lower.as_db_literal(), self.dateliteral_bc_lower)
        self.assertEqual(date_bc_higher.as_db_literal(), self.dateliteral_bc_higher)
        self.assertEqual(date_ad.as_db_literal(), self.dateliteral_ad)
        self.assertEqual(date_bc_lower_from_values.as_db_literal(), self.dateliteral_bc_lower)

        # Check correct comparisons
        self.assertTrue(date_bc_lower < date_bc_higher)
        self.assertTrue(date_bc_higher < date_ad)
        self.assertTrue(date_bc_lower < date_ad)
        self.assertTrue(date_bc_lower_from_values < date_bc_higher)
        self.assertTrue(not (date_bc_lower is date_bc_lower_from_values))
        self.assertTrue(date_bc_lower_from_values == date_bc_lower)
