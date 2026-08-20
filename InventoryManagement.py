from threading import Lock

class Inventory:
    def __init__(self):
        self.w = {"A":{},"B":{},"C":{}}
        self.threshold = {}
        self.locks = {x:Lock() for x in self.w}

    def add_product(self, wh, product, qty, threshold=10):
        if qty < 0 or wh not in self.w: raise ValueError("Invalid")
        with self.locks[wh]:
            self.w[wh][product] = self.w[wh].get(product,0) + qty
            self.threshold[product] = threshold

    def remove_product(self, wh, product, qty):
        if qty <= 0 or self.w[wh].get(product,0) < qty:
            raise ValueError("Insufficient inventory")
        with self.locks[wh]: self.w[wh][product] -= qty

    def transfer(self, a, b, product, qty):
        self.remove_product(a,product,qty)
        self.add_product(b,product,qty,self.threshold.get(product,10))

    def select_warehouse(self, product, qty):
        options=[(v,wh) for wh,d in self.w.items() if (v:=d.get(product,0))>=qty]
        if not options: raise ValueError("No stock")
        return min(options)[1]

    def fulfill(self, product, qty):
        wh=self.select_warehouse(product,qty)
        self.remove_product(wh,product,qty)
        return wh

    def reorder(self, wh, product, qty):
        self.add_product(wh,product,qty,self.threshold.get(product,10))

    def low_stock(self):
        return [(wh,p,q) for wh,d in self.w.items() for p,q in d.items()
                if q<=self.threshold.get(p,10)]

    def stock(self, wh, product):
        return self.w[wh].get(product,0)

    def add_supplier(self, sid, name):
        if not hasattr(self,"suppliers"): self.suppliers={}
        self.suppliers[sid]=name

if __name__ == "__main__":
    i=Inventory()
    i.add_supplier("S1","ABC")
    i.add_product("A","P1",100,20)
    i.add_product("B","P1",50,20)
    print(i.fulfill("P1",30))
