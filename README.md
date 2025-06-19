# Aplikasi Grafis 2D

Aplikasi menggambar 2D interaktif yang dibangun dengan Python dan Tkinter. Aplikasi ini memungkinkan pengguna untuk membuat berbagai bentuk geometris dengan fitur transformasi yang lengkap.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Kontrol dan Shortcut](#kontrol-dan-shortcut)
- [Struktur Kode](#struktur-kode)
- [Kontribusi](#kontribusi)

## ✨ Fitur Utama

### Alat Menggambar
- **Titik**: Membuat titik dengan berbagai ukuran
- **Garis**: Menggambar garis lurus dengan kontrol ketebalan
- **Persegi**: Membuat persegi panjang dan persegi
- **Ellipse**: Menggambar lingkaran dan oval

### Mode Operasi
- **Mode Gambar**: Untuk membuat objek baru
- **Mode Pilih**: Untuk memilih dan memanipulasi objek yang sudah ada

### Transformasi Objek
- **Translasi**: Menggeser objek pada sumbu X dan Y
- **Skala**: Memperbesar atau memperkecil objek
- **Rotasi**: Memutar objek dengan sudut tertentu (dalam derajat)

### Fitur Lainnya
- Pemilihan warna custom menggunakan color picker
- Kontrol ketebalan garis (1-20 piksel)
- Sistem Undo/Redo dengan history hingga 50 langkah
- Status bar informatif
- Antarmuka yang intuitif dan responsif

## 🔧 Persyaratan Sistem

- Python 3.6 atau lebih baru
- Tkinter (biasanya sudah termasuk dalam instalasi Python)
- Sistem operasi: Windows, macOS, atau Linux

## 📦 Instalasi

1. **Clone atau unduh repository ini**:
   ```bash
   git clone <repository-url>
   cd aplikasi-grafis-2d
   ```

2. **Pastikan Python terinstal**:
   ```bash
   python --version
   ```

3. **Jalankan aplikasi**:
   ```bash
   python paste.txt
   ```
   atau
   ```bash
   python3 paste.txt
   ```

> **Catatan**: Tkinter biasanya sudah termasuk dalam instalasi Python standar. Jika tidak tersedia, instal dengan package manager sistem operasi Anda.

## 🎨 Cara Penggunaan

### Memulai Menggambar

1. **Pilih Mode Gambar**
   - Klik radio button "Gambar" di panel kontrol

2. **Pilih Alat**
   - Pilih salah satu dari: Titik, Garis, Persegi, atau Ellipse

3. **Atur Pengaturan**
   - Klik "Pilih Warna" untuk mengubah warna
   - Sesuaikan slider ketebalan sesuai kebutuhan

4. **Mulai Menggambar**
   - **Titik**: Klik sekali pada canvas
   - **Garis**: Klik dan drag dari titik awal ke titik akhir
   - **Persegi/Ellipse**: Klik dan drag untuk menentukan ukuran

### Memanipulasi Objek

1. **Pilih Mode Pilih**
   - Klik radio button "Pilih"

2. **Pilih Objek**
   - Klik pada objek yang ingin dimanipulasi
   - Objek terpilih akan ditandai dengan garis putus-putus merah

3. **Aplikasikan Transformasi**
   - **Translasi X/Y**: Masukkan nilai perpindahan dalam piksel
   - **Skala**: Masukkan nilai skala (1.0 = ukuran asli)
   - **Rotasi**: Masukkan sudut rotasi dalam derajat

### Fitur Tambahan

- **Undo**: Klik tombol "Undo" atau tekan Ctrl+Z
- **Redo**: Klik tombol "Redo" atau tekan Ctrl+Y
- **Bersihkan Canvas**: Klik tombol "Bersihkan Canvas" untuk menghapus semua objek

## ⌨️ Kontrol dan Shortcut

| Aksi | Shortcut |
|------|----------|
| Undo | `Ctrl + Z` |
| Redo | `Ctrl + Y` atau `Ctrl + Shift + Z` |

### Kontrol Mouse
- **Klik**: Membuat titik (mode titik) atau memilih objek (mode pilih)
- **Klik dan Drag**: Membuat garis, persegi, atau ellipse

## 🏗️ Struktur Kode

### Kelas Utama

#### `DrawingObject`
Merepresentasikan objek gambar dengan properti:
- `type`: Jenis objek (point, line, rectangle, ellipse)
- `start`/`end`: Koordinat posisi
- `color`: Warna objek
- `thickness`: Ketebalan garis
- `transform`: Data transformasi (translasi, skala, rotasi)

#### `DrawingApp`
Kelas utama aplikasi yang mengelola:
- Antarmuka pengguna (UI)
- Event handling (mouse dan keyboard)
- Sistem rendering objek
- History management untuk undo/redo
- Transformasi matematis

### Fitur Teknis

#### Sistem Transformasi
Aplikasi mengimplementasikan transformasi 2D menggunakan:
- **Translasi**: Perpindahan linear pada sumbu X dan Y
- **Skaling**: Penskalaan dari titik pusat objek
- **Rotasi**: Rotasi menggunakan trigonometri dari titik pusat
