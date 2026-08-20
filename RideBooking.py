from datetime import datetime

class RideBooking:
    vehicles={
        "Bike":(40,8,1),
        "Sedan":(80,14,4),
        "SUV":(120,18,6),
        "Premium":(200,30,4)
    }

    def __init__(self):
        self.drivers=[]

    def add_driver(self,did,vehicle,available=True):
        self.drivers.append([did,vehicle,available])

    def driver(self,vehicle):
        for d in self.drivers:
            if d[1]==vehicle and d[2]:
                d[2]=False
                return d[0]
        raise ValueError("Driver unavailable")

    def fare(self,distance,passengers,vehicle,time,discount=0):
        if distance<=0 or vehicle not in self.vehicles:
            raise ValueError("Invalid booking")
        base,km,maxp=self.vehicles[vehicle]
        if passengers<1 or passengers>maxp or not isinstance(time,datetime):
            raise ValueError("Invalid booking")
        f=base+distance*km
        if 8<=time.hour<10 or 17<=time.hour<20:f*=1.25
        if time.hour>=22 or time.hour<6:f*=1.20
        f+=(passengers-1)*20
        f*=1-min(discount,.30)
        return round(f,2)

    def book(self,cid,pickup,drop,distance,passengers,vehicle,time,discount=0):
        f=self.fare(distance,passengers,vehicle,time,discount)
        return {"customer":cid,"pickup":pickup,"drop":drop,
                "vehicle":vehicle,"driver":self.driver(vehicle),"fare":f}

if __name__=="__main__":
    r=RideBooking()
    r.add_driver("D1","Sedan")
    print(r.book("C1","A","B",10,2,"Sedan",datetime(2026,8,20,14)))
