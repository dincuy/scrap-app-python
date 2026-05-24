import os
from bs4 import BeautifulSoup
import re
import sys
import requests
import threading
import time

# from scrap_help import KODE_DIPILIH

loading = True


def animasi_loading():
    chars = "|/-\\"
    i = 0
    while loading:
        print(f"\rMengambil data... {chars[i % len(chars)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1


# Folder output
OUTPUT_FOLDER = "manual_data"

# Target Paket
TARGET_PAKET = {
    "VOC TELKOMSEL DATA JAWA BARAT",
    "VOC AXIS DATA MINI",
    "VOC XL FLEX MINI",
}

PRODUK_AKTIF = {
    "TVJBR5G1",
}


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


def get_kategori(jenis_paket):
    jp = jenis_paket.lower()
    if jp.startswith("voc"):
        return "voucher internet"
    elif jp.startswith("unlock"):
        return "aktivasi voucher internet"
    return "lainnya"


def buat_nama_variabel(kategori):
    nama = kategori.lower().strip()
    nama = re.sub(r"[^\w\s]", "", nama)
    nama = re.sub(r"\s+", "_", nama)
    return f"data_{nama}"


# =========================
# SCRAP DARI URL
# =========================

url = "https://prasticareload.webreport.info/harga.js.php?id=f483f4d60dc9d284bd4c6cb50b016284e025ac0fbb5fcc29a58dff035d775b398d163fd12c65d8751d008d645791730ce0e3-86"
headers = {"User-Agent": "Mozilla/5.0"}

# loading animasi
t = threading.Thread(target=animasi_loading)
t.start()

response = requests.get(url, headers=headers)

loading = False
t.join()
print("\rMengambil data... selesai!     ")

if response.status_code != 200:
    print("Gagal mengambil data dari URL")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

data = []
seen = set()  # ✅ untuk deduplikasi

tables = soup.select("table.tabel")

if not tables:
    print("Tidak ada tabel ditemukan")
    sys.exit(1)

for table in tables:
    head = table.select_one("tr.head td[colspan='6']")
    if not head:
        continue

    jenis_paket = head.get_text(" ", strip=True)

    if jenis_paket not in TARGET_PAKET:
        continue

    provider = get_provider(jenis_paket)
    kategori = get_kategori(jenis_paket)

    rows = table.select("tr.td1, tr.td2")

    for row in rows:
        cols = row.find_all("td")

        # ✅ skip row kosong / tidak valid
        if len(cols) < 4:
            continue

        kode = cols[0].get_text(strip=True)
        if not kode:
            continue

        # filter kode
        # if kode not in KODE_DIPILIH:
        #     continue

        keterangan = cols[1].get_text(" ", strip=True)
        harga_text = cols[2].get_text(strip=True)
        status = cols[3].get_text(" ", strip=True)

        harga = parse_harga(harga_text)

        # filter harga
        if harga > 70000:
            continue

        # ✅ deduplikasi
        key = (kode, keterangan, harga)
        if key in seen:
            continue
        seen.add(key)

        is_open = status.lower() == "open"

        item = {
            "kode": f"{kode}-PR",
            "provider": provider,
            "jenisPaket": jenis_paket,
            "kategori": kategori,
            "produk": format_produk(keterangan),
            "desc": jenis_paket,
            "harga": harga,
            "hargaJual": harga_jual(harga),
            "order": "ORDER" if is_open else "",
            "aktif": True if kode in PRODUK_AKTIF else False,
            "link": "",
        }

        data.append(item)

# =========================
# SIMPAN FILE
# =========================

if not data:
    print("Tidak ada data ditemukan")
    sys.exit(0)

kategori = data[0]["kategori"]
nama_variabel = buat_nama_variabel(kategori)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

nama_file = kategori.lower().strip()
nama_file = re.sub(r"[^\w\s]", "", nama_file)
nama_file = re.sub(r"\s+", "_", nama_file)

output_file = os.path.join(OUTPUT_FOLDER, f"{nama_file}.py")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"{nama_variabel} = ")
    f.write(repr(data))

print(f"Selesai! Data disimpan ke {output_file}")
print(f"Jumlah data: {len(data)}")
