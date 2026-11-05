import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Standard service (existing behaviour preserved)
    # ------------------------------------------------------------------

    def test_standard_local(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)

    def test_standard_regional(self):
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit_service(self):
        """Passing service='standard' explicitly must match the default."""
        self.assertEqual(
            shipping_quote(2, "local", service="standard"),
            shipping_quote(2, "local"),
        )

    # ------------------------------------------------------------------
    # Express service (+$7 surcharge)
    # ------------------------------------------------------------------

    def test_express_local(self):
        # 5.0 + 1.5*2 + 7.0 = 15.0
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)

    def test_express_regional(self):
        # 8.0 + 1.5*2 + 7.0 = 18.0
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_surcharge_is_seven(self):
        """Express must be exactly $7 more than standard for every combination."""
        for zone in ("local", "regional"):
            for weight in (1, 5, 10.5):
                std = shipping_quote(weight, zone, service="standard")
                exp = shipping_quote(weight, zone, service="express")
                self.assertAlmostEqual(exp - std, 7.0, places=10,
                                       msg=f"zone={zone}, weight={weight}")

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "intergalactic")

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", service="overnight")
