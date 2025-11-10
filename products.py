import re
from utils import FileHandler, Validator, format_money

class Product:
    def __init__(self, pid:int, name:str, price:int, stock:int):
        self.id = pid
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "stock": self.stock}

class ProductManager:
    def __init__(self, storage: FileHandler):
        self.storage = storage
        self._load()

    def _load(self):
        raw = self.storage.load("products", default=[])
        self.products = [Product(**p) for p in raw]

    def _save(self):
        self.storage.save("products", [p.to_dict() for p in self.products])

    def _next_id(self):
        return max((p.id for p in self.products), default=0) + 1

    def list_products(self):
        if not self.products:
            print("Belum ada produk.")
            return
        print("\nID  | Nama                          | Harga      | Stok")
        print("-"*60)
        for p in self.products:
            print(f"{p.id:<4} | {p.name[:30]:<30} | {format_money(p.price):>10} | {p.stock:>4}")

    def add_product(self):
        name = input("Nama produk: ").strip()
        if not Validator.is_valid_name(name):
            print("Nama tidak valid. Gunakan huruf, angka, spasi, - atau .")
            return
        price = input("Harga (angka): ").strip()
        if not Validator.is_valid_int(price):
            print("Harga harus angka bulat positif.")
            return
        stock = input("Stok awal (angka): ").strip()
        if not Validator.is_valid_int(stock):
            print("Stok harus angka bulat positif.")
            return
        pid = self._next_id()
        prod = Product(pid, name, int(price), int(stock))
        self.products.append(prod)
        self._save()
        print(f"Produk '{name}' ditambahkan dengan ID {pid}.")

    def find(self, pid:int):
        return next((p for p in self.products if p.id == pid), None)
