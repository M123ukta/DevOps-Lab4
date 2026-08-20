import unittest
from ICUAllocation import ICU

class ICUAllocationQA(unittest.TestCase):
    def test_critical(self):
        i=ICU(1)
        p=i.admit("P1",60,80,140,70,40,["cardiac"])
        self.assertEqual(p["level"],"CRITICAL")

    def test_normal(self):
        i=ICU(1)
        p=i.admit("P1",30,98,80,120,37)
        self.assertEqual(p["level"],"LOW")

    def test_emergency(self):
        i=ICU(1)
        i.admit("P1",30,98,80,120,37)
        p=i.admit("P2",60,80,140,70,40,["cardiac"],True)
        self.assertTrue(p["bed"])

    def test_no_beds(self):
        i=ICU(0)
        p=i.admit("P1",30,98,80,120,37)
        self.assertFalse(p["bed"])

    def test_duplicate(self):
        i=ICU(1);i.admit("P1",30,98,80,120,37)
        with self.assertRaises(ValueError):i.admit("P1",30,98,80,120,37)

    def test_oxygen(self):
        with self.assertRaises(ValueError):ICU(1).admit("P1",30,101,80,120,37)

    def test_heart(self):
        with self.assertRaises(ValueError):ICU(1).admit("P1",30,98,250,120,37)

    def test_boundary(self):
        i=ICU(1)
        score,level=i.score(90,80,120,37,[])
        self.assertEqual((score,level),(15,"LOW"))

    def test_competing(self):
        i=ICU(1)
        a=i.admit("P1",30,98,80,120,37)
        b=i.admit("P2",30,98,80,120,37)
        self.assertTrue(a["bed"]);self.assertFalse(b["bed"])

if __name__=="__main__":
    unittest.main(verbosity=2)
