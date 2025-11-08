from products import ProductManager
from transactions import TransactionManager
from utils import FileHandler

class Menu:
    def __init__(self):
        self.storage = FileHandler(data_dir="data")
        self.product_manager = ProductManager(self.storage)
        self.transaction_manager = TransactionManager(self.storage, self.product_manager)

    def run(self):
        while True:
            print("\n=== GROSIR MANAGER (OOP) ===")
            print("1. Manajemen Produk")
            print("2. Transaksi Penjualan")
            print("3. Riwayat Transaksi")
            print("4. Keluar")
            choice = input("Pilih: ").strip()
            if choice == "1":
                self.product_menu()
            elif choice == "2":
                self.transaction_manager.start_sale()
            elif choice == "3":
                self.transaction_manager.show_history()
            elif choice == "4":
                print("Keluar...")
                break
            else:
                print("Pilihan tidak valid.")

    