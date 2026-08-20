import unittest
from datetime import datetime
from RideBooking import RideBooking

class RideBookingQA(unittest.TestCase):
    def setUp(self):
        self.r=RideBooking()
        for x in [("D1","Bike"),("D2","Sedan"),("D3","SUV"),("D4","Premium")]:
            self.r.add_driver(*x)

    def test_normal(self):
        self.assertGreater(self.r.fare(10,2,"Sedan",datetime(2026,8,20,14)),0)

    def test_peak(self):
        a=self.r.fare(10,1,"Sedan",datetime(2026,8,20,14))
        b=self.r.fare(10,1,"Sedan",datetime(2026,8,20,18))
        self.assertGreater(b,a)

    def test_night(self):
        a=self.r.fare(10,1,"Sedan",datetime(2026,8,20,14))
        b=self.r.fare(10,1,"Sedan",datetime(2026,8,20,23))
        self.assertGreater(b,a)

    def test_distance(self):
        with self.assertRaises(ValueError):self.r.fare(0,1,"Sedan",datetime.now())

    def test_passengers(self):
        with self.assertRaises(ValueError):self.r.fare(10,10,"Sedan",datetime.now())

    def test_driver(self):
        self.r.driver("Sedan")
        with self.assertRaises(ValueError):self.r.driver("Sedan")

    def test_discount(self):
        a=self.r.fare(10,1,"SUV",datetime(2026,8,20,14),.3)
        b=self.r.fare(10,1,"SUV",datetime(2026,8,20,14),.8)
        self.assertEqual(a,b)

    def test_vehicles(self):
        for v in self.r.vehicles:
            self.assertGreater(self.r.fare(1,1,v,datetime.now()),0)

    def test_boundary(self):
        self.assertEqual(self.r.fare(1,1,"Bike",datetime(2026,8,20,14)),48)

    def test_allocation(self):
        self.assertEqual(self.r.driver("SUV"),"D3")

if __name__=="__main__":
    unittest.main(verbosity=2)
