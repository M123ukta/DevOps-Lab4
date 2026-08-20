import unittest
import threading
from InventoryManagement import Inventory

class InventoryQA(unittest.TestCase):
    def setUp(self):
        self.i=Inventory()
        self.i.add_product("A","P1",100,20)
        self.i.add_product("B","P1",50,20)
        self.i.add_product("C","P2",30,10)

    def test_stock(self):
        self.assertEqual(self.i.stock("A","P1"),100)

    def test_insufficient(self):
        with self.assertRaises(ValueError): self.i.remove_product("A","P1",200)

    def test_transfer(self):
        self.i.transfer("A","B","P1",20)
        self.assertEqual(self.i.stock("A","P1"),80)
        self.assertEqual(self.i.stock("B","P1"),70)

    def test_concurrent(self):
        errors=[]
        def f():
            try:self.i.fulfill("P1",10)
            except Exception as e:errors.append(e)
        ts=[threading.Thread(target=f) for _ in range(5)]
        for t in ts:t.start()
        for t in ts:t.join()
        self.assertFalse(errors)

    def test_reorder(self):
        self.i.remove_product("A","P1",90)
        self.assertTrue(self.i.low_stock())

    def test_invalid(self):
        with self.assertRaises(ValueError): self.i.remove_product("A","XXX",1)

    def test_negative(self):
        with self.assertRaises(ValueError): self.i.add_product("A","P1",-1)

    def test_warehouses(self):
        self.assertIn(self.i.select_warehouse("P1",40),["A","B"])

if __name__=="__main__":
    unittest.main(verbosity=2)
