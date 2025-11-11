import time, os
from discounts import PercentDiscount, NominalDiscount, DiscountBase
from payments import CashPayment, CardPayment
from utils import FileHandler, format_money

RECEIPT_DIR = "receipts"

class Transaction:
    def __init__(self, items:list, subtotal:int, discount:int, total:int, payment_info:dict, timestamp:str, tx_id:int):
        self.items = items
        self.subtotal = subtotal
        self.discount = discount
        self.total = total
        self.payment_info = payment_info
        self.timestamp = timestamp
        self.id = tx_id

    def to_dict(self):
        return {"id": self.id, "timestamp": self.timestamp, "items": self.items, "subtotal": self.subtotal, "discount": self.discount, "total": self.total, "payment": self.payment_info}

class TransactionManager:
    def __init__(self, storage: FileHandler, product_manager):
        self.storage = storage
        self.pm = product_manager
        os.makedirs(RECEIPT_DIR, exist_ok=True)
        self._load()

    def _load(self):
        self.transactions = self.storage.load("transactions", default=[])

    def _save(self):
        self.storage.save("transactions", self.transactions)

    def _next_id(self):
        return max((t.get("id",0) for t in self.transactions), default=0) + 1

    def start_sale(self):
        cart = []
        while True:
            self.pm.list_products()
            cmd = input("Masukkan ID produk (atau 'done' untuk selesai, 'cancel' untuk batal): ").strip()
            if cmd.lower() == 'done': break
            if cmd.lower() == 'cancel':
                print("Transaksi dibatalkan."); return
            try:
                pid = int(cmd)
            except ValueError:
                print("ID harus angka."); continue
            prod = self.pm.find(pid)
            if not prod:
                print("Produk tidak ditemukan."); continue
            try:
                qty = int(input("Kuantitas: ").strip())
            except ValueError:
                print("Kuantitas harus angka."); continue
            if qty <= 0:
                print("Kuantitas minimal 1."); continue
            if qty > prod.stock:
                print(f"Stok tidak mencukupi. Stok: {prod.stock}"); continue
            # add or update
            existing = next((c for c in cart if c['product_id']==pid), None)
            if existing:
                if existing['qty'] + qty > prod.stock:
                    print("Jumlah melebihi stok."); continue
                existing['qty'] += qty
                existing['subtotal'] = existing['qty']*prod.price
            else:
                cart.append({'product_id': pid, 'name': prod.name, 'price': prod.price, 'qty': qty, 'subtotal': qty*prod.price})
            print(f"Menambahkan {qty} x {prod.name} ke keranjang.")

        if not cart:
            print("Keranjang kosong."); return

        subtotal = sum(c['subtotal'] for c in cart)
        print(f"Subtotal: {format_money(subtotal)}")

        # discount
        d_in = input("Diskon? ('%' untuk persen, 'nominal' untuk nominal, enter untuk skip): ").strip()
        discount_obj = None
        discount_amount = 0
        if d_in == '%':
            try:
                pct = int(input('Masukkan persen diskon (contoh 10): ').strip())
                discount_obj = PercentDiscount(pct)
                discount_amount = discount_obj.calculate(subtotal)
            except Exception:
                print('Input persen tidak valid.')
        elif d_in.lower() == 'nominal':
            try:
                amt = int(input('Masukkan nominal potongan: ').strip())
                discount_obj = NominalDiscount(amt)
                discount_amount = discount_obj.calculate(subtotal)
            except Exception:
                print('Nominal tidak valid.')

        total = max(0, subtotal - discount_amount)
        print(f"Total setelah diskon: {format_money(total)}")

        # payment
        pmode = input("Metode pembayaran ('tunai' atau 'kartu'): ").strip().lower()
        payment_info = None
        if pmode == 'tunai':
            payment = CashPayment()
            payment_info = payment.pay(total)
        elif pmode == 'kartu':
            payment = CardPayment()
            payment_info = payment.pay(total)
        else:
            print('Metode tidak dikenal. Batalkan transaksi.'); return

        # reduce stock and save products
        for c in cart:
            prod = self.pm.find(c['product_id'])
            prod.stock -= c['qty']
        self.pm._save()

        tx_id = self._next_id()
        tx = Transaction(cart, subtotal, discount_amount, total, payment_info, time.strftime('%Y-%m-%d %H:%M:%S'), tx_id)
        self.transactions.append(tx.to_dict())
        self._save()
        self._print_and_save_receipt(tx)
        print('Transaksi berhasil.')

    def _print_and_save_receipt(self, tx: Transaction):
        lines = []
        lines.append('*** TOKO GROSIR OOP ***')
        lines.append(f"Transaksi ID: {tx.id}")
        lines.append(f"Waktu: {tx.timestamp}")
        lines.append('-'*40)
        for i, it in enumerate(tx.items, 1):
            lines.append(f"{i}. {it['name']} x{it['qty']} = {format_money(it['subtotal'])}")
        lines.append('-'*40)
        lines.append(f"Subtotal: {format_money(tx.subtotal)}")
        lines.append(f"Diskon  : {format_money(tx.discount)}")
        lines.append(f"Total   : {format_money(tx.total)}")
        lines.append(f"Metode  : {tx.payment_info.get('method')}")
        lines.append(f"Bayar   : {format_money(tx.payment_info.get('paid'))}")
        lines.append(f"Kembali : {format_money(tx.payment_info.get('change'))}")
        lines.append('-'*40)
        lines.append('Terima kasih!')
        text = '\n'.join(lines)
        print('\n' + text)
        fname = os.path.join('receipts', f"receipt_{tx.id}_{time.strftime('%Y%m%d_%H%M%S')}.txt")
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Struk tersimpan: {fname}")
        except Exception as e:
            print('Gagal simpan struk:', e)

    def show_history(self):
        if not self.transactions:
            print('Belum ada transaksi.')
            return
        print('\n=== RIWAYAT TRANSAKSI ===')
        for t in self.transactions:
            print(f"ID {t.get('id')} | {t.get('timestamp')} | Total: {format_money(t.get('total'))} | Metode: {t.get('payment').get('method')}")
