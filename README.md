**Grocery-Store**
Program Grocery Store adalah aplikasi manajemen toko grosir berbasis Python yang dibuat dengan pendekatan Object-Oriented Programming (OOP).
Program ini dirancang untuk membantu pengelolaan toko secara efisien melalui Command Line (CMD), dengan fitur-fitur utama seperti:

- Manajemen produk dan stok
- Transaksi penjualan
- Penerapan diskon
- Metode pembayaran dan kembalian
- Pencetakan struk transaksi
- Riwayat transaksi
Selain itu, sistem ini sudah dilengkapi dengan error handling, validasi menggunakan regex, dan penyimpanan data berbasis file JSON.

⚙️ Fitur Utama

🛍️ 1. Manajemen Produk
Tambah, ubah, hapus, dan lihat data produk.
Setiap produk memiliki atribut: nama, harga, dan stok.
Data tersimpan otomatis dalam file products.json.

📦 2. Manajemen Stok
Stok produk berkurang secara otomatis saat transaksi berlangsung.
Transaksi tidak bisa dilakukan jika stok tidak mencukupi.

💰 3. Transaksi Penjualan
Dapat menambahkan beberapa item ke keranjang belanja.
Validasi otomatis terhadap harga dan stok.
Data transaksi tersimpan ke file transactions.json.

🎟️ 4. Diskon
Mendukung dua tipe diskon:
Persentase (%): Misal 10% dari total harga.
Nominal (Rp): Misal potongan Rp10.000.
Dikelola dengan konsep inheritance dan polymorphism dari class DiscountBase.

💳 5. Pembayaran dan Kembalian
Metode pembayaran: Tunai (Cash) dan Kartu (Card).
Menggunakan polymorphism untuk memproses metode pembayaran yang berbeda.
Hitung otomatis total harga, jumlah bayar, dan kembalian.

🧾 6. Cetak Struk
Menampilkan struk transaksi langsung di terminal.
Menyimpan salinan struk di folder receipts/ dengan nama sesuai waktu transaksi.

📚 7. Riwayat Transaksi
Semua transaksi tercatat di file transactions.json.
Riwayat bisa ditampilkan kembali lewat menu utama.

Struktur Folder
grocery_store/
│
├── main.py              # Titik awal program
├── menu.py              # Class Menu (navigasi dan kontrol utama)
├── products.py          # Class Product & ProductManager (CRUD produk)
├── transactions.py      # Class Transaction & TransactionManager
├── discounts.py         # Class DiscountBase, PercentDiscount, NominalDiscount
├── payments.py          # Class PaymentBase, CashPayment, CardPayment
├── utils.py             # FileHandler, Validator, helper umum
│
├── data/
│   ├── products.json        # Penyimpanan data produk
│   └── transactions.json    # Penyimpanan riwayat transaksi
│
└── receipts/
    └── ... (file struk transaksi)

| Konsep             | Implementasi                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Class & Object** | Setiap entitas (Produk, Transaksi, Diskon, Pembayaran) dibuat sebagai class.                                             |
| **Encapsulation**  | Atribut objek disembunyikan dan diakses melalui method.                                                                  |
| **Inheritance**    | `PercentDiscount` dan `NominalDiscount` mewarisi `DiscountBase`; `CashPayment` dan `CardPayment` mewarisi `PaymentBase`. |
| **Polymorphism**   | Metode `apply_discount()` dan `process_payment()` memiliki implementasi berbeda di tiap subclass.                        |
| **Abstraction**    | Class dasar (`DiscountBase`, `PaymentBase`) memberikan struktur umum tanpa implementasi langsung.                        |

1. Pastikan sudah menginstal Python 3.8+
2. Ekstrak folder proyek grocery_store
3. Buka CMD atau Terminal di dalam folder
4. Jalankan perintah berikut:
   python main.py
5. Ikuti menu yang tampil untuk mengelola produk, transaksi, dan pembayaran.

Modul yang Digunakan
re — validasi input menggunakan Regular Expression
time — menampilkan waktu transaksi
json — penyimpanan data produk dan transaksi
os, sys — pengelolaan file dan terminal
