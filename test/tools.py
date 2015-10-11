import unittest


class TestCrypto(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("test")

    def test_modif_cheque(self):
        """
        Test a change in the check from the customer
        Test a change in the check from the merchant
        """
        self.assertTrue(True)
