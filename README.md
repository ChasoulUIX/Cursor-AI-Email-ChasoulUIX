# Cursor Email Authentication Handler

Sistem penanganan autentikasi email untuk Cursor AI dengan fitur pendeteksian email yang diblokir dan sistem whitelist untuk domain yang diizinkan.

## 🚀 Fitur

- ✅ Validasi format email
- 🛡️ Pendeteksian email yang diblokir
- ⚡ Sistem whitelist untuk domain yang diizinkan
- 🔄 Penanganan error policy_denied
- 📝 Sistem appeal otomatis
- 🌐 Dukungan untuk berbagai domain (.com, .ac.id, .co.id, .go.id)

## 📋 Persyaratan

- Python 3.7 atau lebih tinggi
- pip (Python package installer)

## 🛠️ Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/YourUsername/cursor-email-handler.git
cd cursor-email-handler
```

2. Berikan izin eksekusi untuk script Linux (jika menggunakan Linux):
```bash
chmod +x run_linux.sh
```

## 💻 Cara Menjalankan

### Di Windows:
1. Double click pada file `run_windows.bat`

Atau melalui Command Prompt:
```bash
run_windows.bat
```

### Di Linux:
1. Buka terminal di folder proyek
2. Jalankan script:
```bash
./run_linux.sh
```

Script akan secara otomatis:
- Memeriksa instalasi Python
- Membuat virtual environment jika belum ada
- Menginstal semua dependencies
- Menjalankan program

### Menjalankan Manual (Alternatif):

1. Buat virtual environment (opsional tapi direkomendasikan):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan program:
```bash
# Windows
python email_registration_handler.py

# Linux/Mac
python3 email_registration_handler.py
```

## 📝 Contoh Output

```
Testing Cursor Authentication System:
--------------------------------------------------

Mencoba login dengan email: user@gmail.com
Status: Berhasil
Pesan: Autentikasi berhasil! Mengalihkan ke dashboard...
Session ID: 01JRW8HSC5A1AXN4ZVJX508Q8S
Redirect URL: https://cursor.com/dashboard

Mencoba login dengan email: blocked@example.com
Status: Gagal
Error Code: policy_denied
Pesan: Akses ditolak karena kebijakan keamanan...
```

## 🔧 Konfigurasi

Anda dapat mengkonfigurasi domain yang diizinkan dengan mengedit list `allowed_domains` di class `CursorAuthHandler`:

```python
self.allowed_domains = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "company.com",
    "ac.id",
    "co.id",
    "go.id"
]
```

## 📚 API Reference

### `CursorAuthHandler`

#### `handle_auth(email: str, auth_url: str = None) -> AuthResult`
Menangani proses autentikasi email.

Parameters:
- `email`: String email yang akan divalidasi
- `auth_url`: (Opsional) URL autentikasi Cursor

Returns:
- `AuthResult` object dengan informasi status autentikasi

### `EmailValidator`

#### `is_valid_domain(domain: str) -> bool`
Memvalidasi apakah domain email diizinkan.

Parameters:
- `domain`: String domain email

Returns:
- `bool`: True jika domain valid, False jika tidak

## 🤝 Kontribusi

Kontribusi selalu diterima! Berikut langkah-langkah untuk berkontribusi:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 🔍 Troubleshooting

### Windows
- Jika muncul error "python not recognized", pastikan Python sudah diinstall dan ditambahkan ke PATH
- Jika script tidak berjalan, coba jalankan Command Prompt sebagai Administrator

### Linux
- Jika muncul error permission denied, jalankan: `chmod +x run_linux.sh`
- Jika pip atau venv tidak terinstall, script akan mencoba menginstallnya secara otomatis
- Jika diminta password sudo, masukkan password administrator Anda

## 📝 Lisensi

Distributed under the MIT License. Lihat `LICENSE` untuk informasi lebih lanjut.

## 📧 Kontak

Your Name - [@YourTwitter](https://twitter.com/YourTwitter)

Project Link: [https://github.com/YourUsername/cursor-email-handler](https://github.com/YourUsername/cursor-email-handler) 