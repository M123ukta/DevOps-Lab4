class CourseRegistration:
    def __init__(self,limit=20):
        self.limit=limit
        self.courses={
            "DBMS":{"c":4,"p":"Programming","cap":2,"sem":5,"time":"MON10"},
            "AI":{"c":4,"p":"Data Structures","cap":2,"sem":5,"time":"MON10"},
            "ML":{"c":3,"p":"Statistics","cap":2,"sem":6,"time":"TUE10"},
            "Cloud":{"c":3,"p":"Networking","cap":2,"sem":5,"time":"WED10"}
        }
        self.students={}

    def register(self,sid,program,sem,completed,selected):
        if sid in self.students:raise ValueError("Duplicate registration")
        if len(selected)!=len(set(selected)):raise ValueError("Duplicate course")
        total=0;times=[]
        for c in selected:
            if c not in self.courses:raise ValueError("Invalid course")
            d=self.courses[c]
            if d["sem"]!=sem:raise ValueError("Semester restriction")
            if d["p"] not in completed:raise ValueError("Missing prerequisite")
            if sum(c in x["courses"] for x in self.students.values())>=d["cap"]:
                raise ValueError("Course full")
            total+=d["c"]
            if d["time"] in times:raise ValueError("Timetable conflict")
            times.append(d["time"])
        if total>self.limit:raise ValueError("Credit limit")
        self.students[sid]={"program":program,"semester":sem,"courses":selected,"credits":total}
        return self.students[sid]

    def credits(self,sid):
        return self.students[sid]["credits"]

    def seats(self,c):
        if c not in self.courses:raise ValueError("Invalid course")
        return self.courses[c]["cap"]-sum(c in x["courses"] for x in self.students.values())

if __name__=="__main__":
    r=CourseRegistration()
    print(r.register("S1","SE",5,["Programming","Networking"],["DBMS","Cloud"]))
