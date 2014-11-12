import unittest
from eradate import EraDate

class EraDateTest(unittest.TestCase):
    def setUp(self):
        super(EraDateTest, self).setUp()
        self.dateliteral_bc_lower = "3000-05-20 BC"
        self.dateliteral_bc_higher = "0009-10-19 BC"
        self.dateliteral_ad = "0085-06-03"
        self.date_values_bc_lower = (-3000, 5, 20)
        self.dateliteral_none = None
        self.dateliteral_broken = "010-1-123"
        self.dateliteral_nonvalid = "1900-40-50"
        self.dateliteral_bc_lower_js = "-003000-05-20"
        self.dateliteral_not_full = "0200-11"
        self.dateliteral_not_full_ref = "0200-11-01"
        self.dateliteral_not_full_bc_db = "0012 BC"
        self.dateliteral_not_full_bc_db_ref = "0012-01-01 BC"
        self.dateliteral_not_full_bc_js = "-000012"
        self.dateliteral_not_full_bc_js_ref = "0012-01-01 BC"

    def test_custom_date_class(self):
        date_bc_lower = EraDate.parse(self.dateliteral_bc_lower)
        date_bc_higher = EraDate.parse(self.dateliteral_bc_higher)
        date_ad = EraDate.parse(self.dateliteral_ad)
        date_bc_lower_from_values = EraDate(*self.date_values_bc_lower)
        date_none = EraDate.parse(self.dateliteral_none)
        date_bc_lower_js = EraDate.parse(self.dateliteral_bc_lower_js)
        date_not_full = EraDate.parse(self.dateliteral_not_full)
        date_not_full_bc_db = EraDate.parse(self.dateliteral_not_full_bc_db)
        date_not_full_bc_js = EraDate.parse(self.dateliteral_not_full_bc_js)

        # Check brokens and non valid
        with self.assertRaises(ValueError):
            EraDate.parse(self.dateliteral_broken)

        with self.assertRaises(ValueError):
            EraDate.parse(self.dateliteral_nonvalid)

        # Check coorect object type
        self.assertEqual(type(date_bc_lower), EraDate)

        # Check correct representation
        self.assertEqual(date_bc_lower.as_db_literal(), self.dateliteral_bc_lower)
        self.assertEqual(date_bc_higher.as_db_literal(), self.dateliteral_bc_higher)
        self.assertEqual(date_ad.as_db_literal(), self.dateliteral_ad)
        self.assertEqual(date_bc_lower_from_values.as_db_literal(), self.dateliteral_bc_lower)
        self.assertEqual(date_none, self.dateliteral_none)
        self.assertEqual(date_bc_lower_js.as_db_literal(), self.dateliteral_bc_lower)
        self.assertEqual(date_not_full.as_db_literal(), self.dateliteral_not_full_ref)
        self.assertEqual(date_not_full_bc_db.as_db_literal(), self.dateliteral_not_full_bc_db_ref)
        self.assertEqual(date_not_full_bc_js.as_db_literal(), self.dateliteral_not_full_bc_js_ref)

        # Check correct comparisons
        self.assertTrue(date_bc_lower < date_bc_higher)
        self.assertTrue(date_bc_higher < date_ad)
        self.assertTrue(date_bc_lower < date_ad)
        self.assertTrue(date_bc_lower_from_values < date_bc_higher)
        self.assertTrue(not (date_bc_lower is date_bc_lower_from_values))
        self.assertTrue(date_bc_lower_from_values == date_bc_lower)
        self.assertFalse(date_bc_lower == None)
        self.assertTrue(date_bc_lower != None)
        self.assertTrue(date_bc_lower_js < date_bc_higher)
        self.assertTrue(date_bc_lower == date_bc_lower_js)
