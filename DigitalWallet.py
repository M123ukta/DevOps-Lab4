from datetime import datetime, timedelta
from threading import Lock

class DigitalWallet:
    def __init__(self):
        self.accounts, self.history = {}, {}
        self.failed, self.locks = {}, {}
        self.limit = 50000

    def create_account(self, aid, name, pin, balance=0):
        if aid in self.accounts or len(str(pin)) != 4 or balance < 0:
            raise ValueError("Invalid account")
        self.accounts[aid] = {"name": name, "pin": str(pin), "balance": balance, "daily": 0}
        self.history[aid], self.failed[aid], self.locks[aid] = [], 0, Lock()

    def verify_pin(self, aid, pin):
        if aid not in self.accounts or self.failed[aid] >= 3:
            return False
        if str(pin) == self.accounts[aid]["pin"]:
            self.failed[aid] = 0
            return True
        self.failed[aid] += 1
        return False

    def fraud(self, aid, amount):
        now = datetime.now()
        recent = [x for x in self.history[aid] if now-x["time"] <= timedelta(minutes=10)]
        reasons = []
        if len(recent) >= 5: reasons.append("FREQUENT")
        if amount >= 25000: reasons.append("LARGE")
        amounts = [x["amount"] for x in self.history[aid]]
        if amounts and amount > 5 * sum(amounts) / len(amounts): reasons.append("UNUSUAL")
        if self.failed[aid] >= 3: reasons.append("PIN")
        return reasons

    def deposit(self, aid, amount, ref="D"):
        if amount <= 0: raise ValueError("Invalid amount")
        with self.locks[aid]:
            if self.accounts[aid]["daily"] + amount > self.limit: raise ValueError("Daily limit")
            if any(x["ref"] == ref for x in self.history[aid]): raise ValueError("Duplicate")
            r = self.fraud(aid, amount)
            self.accounts[aid]["balance"] += amount
            self.accounts[aid]["daily"] += amount
            self.history[aid].append({"type":"deposit","amount":amount,"ref":ref,"time":datetime.now(),"fraud":r})
            return r

    def withdraw(self, aid, amount, pin, ref="W"):
        if amount <= 0 or not self.verify_pin(aid, pin): raise ValueError("Invalid transaction")
        with self.locks[aid]:
            if self.accounts[aid]["balance"] < amount: raise ValueError("Insufficient balance")
            if self.accounts[aid]["daily"] + amount > self.limit: raise ValueError("Daily limit")
            if any(x["ref"] == ref for x in self.history[aid]): raise ValueError("Duplicate")
            r = self.fraud(aid, amount)
            self.accounts[aid]["balance"] -= amount
            self.accounts[aid]["daily"] += amount
            self.history[aid].append({"type":"withdraw","amount":amount,"ref":ref,"time":datetime.now(),"fraud":r})
            return r

    def transfer(self, a, b, amount, pin, ref="T"):
        if amount <= 0 or not self.verify_pin(a, pin): raise ValueError("Invalid transaction")
        with self.locks[a]:
            if self.accounts[a]["balance"] < amount: raise ValueError("Insufficient balance")
            if self.accounts[a]["daily"] + amount > self.limit: raise ValueError("Daily limit")
            if any(x["ref"] == ref for x in self.history[a]): raise ValueError("Duplicate")
            r = self.fraud(a, amount)
            self.accounts[a]["balance"] -= amount
            self.accounts[b]["balance"] += amount
            self.accounts[a]["daily"] += amount
            self.history[a].append({"type":"transfer","amount":amount,"ref":ref,"time":datetime.now(),"fraud":r})
            return r

    def balance(self, aid):
        return self.accounts[aid]["balance"]

    def transactions(self, aid):
        return self.history[aid]

if __name__ == "__main__":
    w = DigitalWallet()
    w.create_account("A1","Alice","1234",10000)
    w.create_account("A2","Bob","5678",5000)
    w.deposit("A1",1000)
    w.transfer("A1","A2",500,"1234")
    print(w.balance("A1"))
