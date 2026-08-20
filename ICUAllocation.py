class ICU:
    def __init__(self,beds):
        if beds<0:raise ValueError("Invalid beds")
        self.beds=beds
        self.patients={}
        self.waiting=[]

    def score(self,o,h,b,t,conditions):
        s=0
        if o<85:s+=40
        elif o<90:s+=30
        elif o<94:s+=15
        if h>130 or h<45:s+=25
        elif h>110 or h<55:s+=15
        if b<80 or b>180:s+=20
        elif b<90 or b>160:s+=10
        if t>=40 or t<=34:s+=15
        elif t>=39 or t<=35:s+=8
        s+=min(15,len(conditions)*5)
        return s,"CRITICAL" if s>=60 else "HIGH" if s>=40 else "MEDIUM" if s>=20 else "LOW"

    def admit(self,pid,age,o,h,b,t,conditions=None,emergency=False):
        conditions=conditions or []
        if pid in self.patients or not 0<=o<=100 or not 30<=h<=220:
            raise ValueError("Invalid patient")
        if age<0 or age>120 or t<25 or t>45 or b<=0:raise ValueError("Invalid data")
        score,level=self.score(o,h,b,t,conditions)
        p={"score":score,"level":level,"emergency":emergency,"bed":False}
        self.patients[pid]=p
        self.allocate(pid)
        return p

    def allocate(self,pid):
        p=self.patients[pid]
        if self.beds:
            self.beds-=1;p["bed"]=True;return
        if p["emergency"]:
            active=[(k,v) for k,v in self.patients.items() if v["bed"] and not v["emergency"]]
            if active:
                k,v=min(active,key=lambda x:x[1]["score"])
                v["bed"]=False;self.waiting.append(k);p["bed"]=True;return
        self.waiting.append(pid)

    def discharge(self,pid):
        if self.patients[pid]["bed"]:
            self.patients[pid]["bed"]=False
            self.beds+=1
            if self.waiting:
                self.allocate(self.waiting.pop(0))

if __name__=="__main__":
    i=ICU(2)
    print(i.admit("P1",60,80,140,70,40,["cardiac"]))
