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

    def edit_product(self):
        try:
            self.list_products()
            pid = int(input("Masukkan ID produk yang ingin diubah: ").strip())
            p = self.find(pid)
            if not p:
                print("Produk tidak ditemukan.")
                return
            new_name = input(f"Nama [{p.name}]: ").strip() or p.name
            if not Validator.is_valid_name(new_name):
                print("Nama tidak valid.")
                return
            new_price = input(f"Harga [{p.price}]: ").strip()
            if new_price and not Validator.is_valid_int(new_price):
                print("Harga tidak valid.")
                return
            new_stock = input(f"Stok [{p.stock}]: ").strip()
            if new_stock and not Validator.is_valid_int(new_stock):
                print("Stok tidak valid.")
                return
            p.name = new_name
            if new_price: p.price = int(new_price)
            if new_stock: p.stock = int(new_stock)
            self._save()
            print("Produk diperbarui.")
        except Exception as e:
            print("Error:", e)

    def delete_product(self):
        try:
            self.list_products()
            pid = int(input("Masukkan ID produk yang ingin dihapus: ").strip())
            p = self.find(pid)
            if not p:
                print("Produk tidak ditemukan.")
                return
            confirm = input(f"Yakin hapus '{p.name}'? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Dibatalkan.")
                return
            self.products = [x for x in self.products if x.id != pid]
            self._save()
            print("Produk dihapus.")
        except Exception as e:
            print("Error:", e)
