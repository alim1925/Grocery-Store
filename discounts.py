from abc import ABC, abstractmethod

class DiscountBase(ABC):
    @abstractmethod
    def calculate(self, subtotal:int) -> int:
        pass

class PercentDiscount(DiscountBase):
    def __init__(self, percent:int):
        self.percent = percent

    def calculate(self, subtotal:int) -> int:
        return int(subtotal * self.percent / 100)

class NominalDiscount(DiscountBase):
    def __init__(self, amount:int):
        self.amount = amount

    def calculate(self, subtotal:int) -> int:
        return min(self.amount, subtotal)
