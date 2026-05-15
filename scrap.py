import os
from bs4 import BeautifulSoup
import json
import re
import sys

# Folder output
OUTPUT_FOLDER = "manual_data"
# Folder tempat HTML
FOLDER_HTML = "html"


def parse_harga(text):
    return int(text.replace(".", "").replace(",", "").strip())


def bulatkan_ribuan(harga):
    sisa = harga % 1000
    bawah = harga - sisa
    atas = bawah + 1000
    return bawah if sisa < 500 else atas


def hitung_profit(harga_bulat):
    if harga_bulat < 7000:
        return 1000
    elif 7000 <= harga_bulat <= 20000:
        return 2000
    elif 20000 < harga_bulat <= 100000:
        return 3000
    else:
        return 5000


def harga_jual(harga):
    harga_bulat = bulatkan_ribuan(harga)
    return harga_bulat + hitung_profit(harga_bulat)


def format_produk(keterangan):
    if " - " in keterangan:
        isi, durasi = keterangan.rsplit(" - ", 1)
    else:
        isi, durasi = keterangan, ""

    isi = isi.replace("Voucher ", "").strip()
    durasi = re.sub(r"(\d+)\s*Hari", r"\1 Hari", durasi.strip())

    hasil = f"Voucher Internet - {isi}"
    if durasi:
        hasil += f" / {durasi}"
    return hasil


def get_provider(judul):
    judul = judul.lower()

    if "telkomsel" in judul:
        return "telkomsel"
    elif "axis" in judul:
        return "axis"
    elif "xl" in judul:
        return "xl"
    elif "indosat" in judul or "im3" in judul:
        return "indosat"
    elif "tri" in judul:
        return "tri"
    elif "smartfren" in judul:
        return "smartfren"
    else:
        return "unknown"


def buat_nama_variabel(kategori):
    nama = kategori.lower().strip()
    nama = re.sub(r"[^\w\s]", "", nama)
    nama = re.sub(r"\s+", "_", nama)
    return f"data_{nama}"


# Validasi folder
if not os.path.isdir(FOLDER_HTML):
    print(f"Folder '{FOLDER_HTML}' tidak ditemukan")
    sys.exit(1)

files = sorted([f for f in os.listdir(FOLDER_HTML) if f.endswith(".html")])

if not files:
    print("Tidak ada file HTML")
    sys.exit(1)

# Pilih file
print("Pilih file HTML:")
for i, file in enumerate(files, start=1):
    print(f"{i}. {file}")

try:
    pilihan = int(input("Masukkan nomor: ")) - 1
except ValueError:
    print("Input harus angka")
    sys.exit(1)

if pilihan < 0 or pilihan >= len(files):
    print("Pilihan tidak valid")
    sys.exit(1)

file_terpilih = files[pilihan]
path_file = os.path.join(FOLDER_HTML, file_terpilih)

# Baca HTML
with open(path_file, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

data = []

tables = soup.select("table.tabel")

if not tables:
    print("Tidak ada tabel class='tabel' yang ditemukan")
    sys.exit(1)

for table in tables:
    head = table.select_one("tr.head td[colspan='6']")
    if not head:
        continue

    jenis_paket = head.get_text(" ", strip=True)
    provider = get_provider(jenis_paket)

    rows = table.select("tr.td1, tr.td2")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        kode = cols[0].get_text(strip=True)
        keterangan = cols[1].get_text(" ", strip=True)
        harga_text = cols[2].get_text(strip=True)
        status = cols[3].get_text(" ", strip=True)

        harga = parse_harga(harga_text)
        is_open = status.lower() == "open"

        item = {
            "kode": f"{kode}-PR",
            "provider": provider,
            "jenisPaket": jenis_paket,
            "kategori": "voucher internet",
            "produk": format_produk(keterangan),
            "desc": jenis_paket,
            "harga": harga,
            "hargaJual": harga_jual(harga),
            "order": "ORDER" if is_open else "",
            "aktif": False,
            "link": "",
        }

        data.append(item)

# Tentukan nama variabel dari kategori
kategori = data[0]["kategori"] if data else "data"
nama_variabel = buat_nama_variabel(kategori)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Simpan ke file .py
nama_file = file_terpilih.replace(".html", ".py")
output_file = os.path.join(OUTPUT_FOLDER, nama_file)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"{nama_variabel} = ")
    f.write(repr(data))

print(f"Selesai! Data disimpan ke {output_file}")
print(f"Nama variabel: {nama_variabel}")
