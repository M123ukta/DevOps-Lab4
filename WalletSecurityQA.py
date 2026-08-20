import unittest
import threading
from DigitalWallet import DigitalWallet

class WalletSecurityQA(unittest.TestCase):
    def setUp(self):
        self.w = DigitalWallet()
        self.w.create_account("A1","Alice","1234",10000)
        self.w.create_account("A2","Bob","5678",5000)

    def test_normal(self):
        self.w.deposit("A1",500)
        self.assertEqual(self.w.balance("A1"),10500)

    def test_insufficient(self):
        with self.assertRaises(ValueError):
            self.w.withdraw("A1",20000,"1234")

    def test_daily_limit(self):
        with self.assertRaises(ValueError):
            self.w.withdraw("A1",50001,"1234")

    def test_failed_pins(self):
        for p in ["1111","2222","3333"]:
            self.assertFalse(self.w.verify_pin("A1",p))
        self.assertFalse(self.w.verify_pin("A1","1234"))

    def test_suspicious(self):
        for i in range(5):
            self.w.deposit("A1",100,f"T{i}")
        result = self.w.deposit("A1",100,"T5")
        self.assertIn("FREQUENT",result)

    def test_duplicate(self):
        self.w.deposit("A1",100,"X")
        with self.assertRaises(ValueError):
            self.w.deposit("A1",100,"X")

    def test_negative(self):
        with self.assertRaises(ValueError):
            self.w.deposit("A1",-10)

    def test_concurrent(self):
        errors=[]

        def f():
            try:
                self.w.deposit("A1",100,str(threading.get_ident()))
            except Exception as e:
                errors.append(e)

        ts=[threading.Thread(target=f) for _ in range(5)]

        for t in ts:
            t.start()

        for t in ts:
            t.join()

        self.assertFalse(errors)

if __name__=="__main__":
    unittest.main(verbosity=2)
