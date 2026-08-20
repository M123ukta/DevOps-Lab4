import unittest
from CourseRegistration import CourseRegistration

class CourseRegistrationQA(unittest.TestCase):
    def test_valid(self):
        r=CourseRegistration()
        x=r.register("S1","SE",5,["Programming","Networking"],["DBMS","Cloud"])
        self.assertEqual(x["credits"],7)

    def test_prerequisite(self):
        with self.assertRaises(ValueError):
            CourseRegistration().register("S1","SE",5,[],["DBMS"])

    def test_credit_limit(self):
        with self.assertRaises(ValueError):
            CourseRegistration(6).register("S1","SE",5,["Programming","Networking"],["DBMS","Cloud"])

    def test_clash(self):
        with self.assertRaises(ValueError):
            CourseRegistration().register("S1","SE",5,["Programming","Data Structures"],["DBMS","AI"])

    def test_full(self):
        r=CourseRegistration()
        for sid in ["S1","S2"]:r.register(sid,"SE",5,["Programming"],["DBMS"])
        with self.assertRaises(ValueError):r.register("S3","SE",5,["Programming"],["DBMS"])

    def test_duplicate(self):
        r=CourseRegistration()
        r.register("S1","SE",5,["Programming"],["DBMS"])
        with self.assertRaises(ValueError):r.register("S1","SE",5,["Programming"],["Cloud"])

    def test_invalid_course(self):
        with self.assertRaises(ValueError):
            CourseRegistration().register("S1","SE",5,["Programming"],["XYZ"])

    def test_semester(self):
        with self.assertRaises(ValueError):
            CourseRegistration().register("S1","SE",5,["Statistics"],["ML"])

    def test_boundary_credit(self):
        r=CourseRegistration(7)
        x=r.register("S1","SE",5,["Programming","Networking"],["DBMS","Cloud"])
        self.assertEqual(x["credits"],7)

if __name__=="__main__":
    unittest.main(verbosity=2)
