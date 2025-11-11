from abc import ABC, abstractmethod

class PaymentBase(ABC):
    @abstractmethod
    def pay(self, amount:int):
        pass

class CashPayment(PaymentBase):
    def pay(self, amount:int):
        while True:
            try:
                paid = int(input(f"Bayar tunai (Rp{amount}): ").strip())
                if paid < amount:
                    print("Uang tidak cukup. Masukkan lagi.")
                    continue
                return {"method":"tunai", "paid": paid, "change": paid-amount}
            except ValueError:
                print("Masukkan angka yang valid.")

class CardPayment(PaymentBase):
    def pay(self, amount:int):
        print("Memproses pembayaran kartu... (dianggap sukses)")
        return {"method":"kartu", "paid": amount, "change": 0}
