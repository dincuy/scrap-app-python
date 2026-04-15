import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
# from konversi import konversi_harga, get_total_harga_pulsa
from source_urls import source_urls
from helper.list_aktif import paket_internet, voucher_internet, aktivasi_voucher_internet, topup_game
# import manual data
from manual_data.paket_internet import data_paket_internet
from manual_data.aktivasi_voucher import data_aktivasi_voucher
from manual_data.voucher_internet import data_voucher_internet

def hapus_rp(nominal):
    nominal_int = int(''.join(filter(str.isdigit, nominal)))
    return nominal_int

def konversi_harga(kode, nominal):
    # Daftar harga khusus berdasarkan kode
    harga_khusus = {
        "CAXXS1": 8000,
        "AVZMINI1": 15000,
        "UVAM6GB3-PR": 16000,
        "AXLMF4G1H": 8000,
    }
    
    # Jika kode ada di harga khusus, langsung kembalikan nilainya
    if kode in harga_khusus:
        return harga_khusus[kode]
    
    # Pembulatan nominal ke ribuan
    sisa = nominal % 1000
    dasar = nominal - sisa
    
    if sisa <= 500:
        nominal_bulat = dasar
    else:
        nominal_bulat = dasar + 1000

    # Penentuan profit
    if nominal_bulat <= 7000:
        profit = 1000
    elif nominal_bulat <= 20000:
        profit = 2000
    elif nominal_bulat <= 100000:
        profit = 3000
    else:
        profit = 5000

    # Harga jual akhir
    harga_jual = nominal_bulat + profit

    return harga_jual


def get_total_harga_pulsa(str_nominal):
    if str_nominal == "Pulsa - Cek Hutang Pulsa / Paket Darurat":
        return 0
    num = int(''.join(filter(str.isdigit, str_nominal)))

    if "Pulsa Transfer" in str_nominal:
        num_total_harga = num + 1000
        # return "Rp. {:,}".format(num_total_harga).replace(",", ".")
        return num_total_harga

    if num < 5000:
        num_total_harga = num + 1000
    elif num >= 10000 and num < 50000:
        num_total_harga = num + 2000
    else:
        num_total_harga = num + 3000

    # return "Rp. {:,}".format(num_total_harga).replace(",", ".")
    return num_total_harga

# Contoh penggunaan
# print(konversi_harga("Rp. 5000", 2000))
# print(get_total_harga_pulsa("Pulsa 3000"))

# Konfigurasi API Sanity
SANITY_PROJECT_ID = "bkraz3f2"  # Ganti dengan Project ID Anda
SANITY_DATASET = "production"        # Ganti dengan dataset yang digunakan
SANITY_API_VERSION = "2022-03-07"      # Versi API Sanity
SANITY_TOKEN = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"     # Ganti dengan token API Sanity Anda

# URL endpoint untuk query dan mutasi data di Sanity
sanity_url_query = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
sanity_url_mutate = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"

# Headers untuk mengotorisasi request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SANITY_TOKEN}",
}

# Fungsi untuk mendapatkan semua _id dari dokumen di Sanity
def get_all_paket_ids(kategori):
    query = f'*[_type == "paket" && kategori == "{kategori}"]{{_id}}'
    try:
        response = requests.get(sanity_url_query, headers=headers, params={"query": query})
        if response.status_code == 200:
            result = response.json()
            ids = [doc["_id"] for doc in result.get("result", [])]
            return ids
        else:
            print(f"Error saat mengambil data dari Sanity: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        print(f"Error saat mengambil data dari Sanity: {e}")
        return []

# Fungsi untuk menghapus dokumen berdasarkan _id
def delete_paket_documents(ids):
    if not ids:
        print("Tidak ada dokumen 'paket' yang ditemukan untuk dihapus.")
        return

    mutations = {
        "mutations": [
            {"delete": {"id": _id}} for _id in ids
        ]
    }

    try:
        response = requests.post(sanity_url_mutate, headers=headers, data=json.dumps(mutations))
        if response.status_code == 200 or response.status_code == 202:
            print(f"{len(ids)} dokumen 'paket' berhasil dihapus.")
        else:
            print(f"Error saat menghapus dokumen: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error saat mengirim permintaan penghapusan: {e}")

# Fungsi untuk menghapus data paket berdasarkan kategori
def hapus_data_paket_by_kategori(kategori):
    print(f"Mengambil semua _id dari dokumen 'paket' dengan kategori '{kategori}'...")
    ids = get_all_paket_ids(kategori)
    if ids:
        print(f"Ditemukan {len(ids)} dokumen. Menghapus...")
        delete_paket_documents(ids)
    else:
        print(f"Tidak ada dokumen 'paket' ditemukan untuk kategori '{kategori}'.")

# Fungsi untuk ambil data manual
def get_manual_data(product):
    current_time = datetime.now().isoformat()

    mapping = {
        "paket-internet": data_paket_internet,
        "aktivasi-voucher-internet": data_aktivasi_voucher,
        "voucher-internet": data_voucher_internet,
    }

    manual_list = mapping.get(product, [])

    # Tambahkan field dibuatPada
    for item in manual_list:
        item["dibuatPada"] = current_time

    return manual_list

KODE_SKIP = {
    "IVXBP2K1",
    "AXLBB3K1",
    "SDZ4",
    "SDZ8",
    "SDZ14",
    "SDZ16",
    "ACJBR2030",
    "IVXBP2K3",
    "UVTJBR4",
    "UVAM2C",
    "CAB800",
    "CAB4",
    "CAB5",
    "AXZ15G3",
    "CAM1",
    "UVXFM20G3",
    "IVXBP2K5",
    "AXLBB3K7",
    "UVXFM20G7",
    "IVXBP5K7",
    "UVXFM40G7",
    "UVXFM75G7",
    "IVXBP5K10",
    "AVXFH5G14H",
    "UVXFM75",
    "UVXFM150",
    "IVXBP5K15",
    "IVXBP2K30",
    "AXLBB3K30",
    "AXLMF5G3H",
    "IVXBP5K3",
    "UVXFM6G3",
    "IVXBP5K5",
    "AXLMF17G7H",
    "UVXFM30",
    "AXLBB3K15",
    "IVXBP2K15",
    "IVXBP5K1",
    "CAXSS15",
    "UVXFM10G1",
    "UVXFM4G3",
    "AXLMF17G14",
    "IVXBP5K30",
    "AXLMF17G14",
    "SDZ18",
    "SDZ10",
    "ACJBR730",
    "UVTJBR10",
    "UVTJBR14",
    "SDZ11",                       
}

# Fungsi untuk melakukan scraping data
def scrap_from_url(source_urls, product):
    sources = source_urls[product]
    data = []
    current_time = datetime.now().isoformat()  # Menggunakan format ISO-8601 yang valid
    collected_ids = set()  # Untuk mengecek duplikasi
    duplicates = []  # Menyimpan kode yang duplikat
    
    list_aktif_now = {
        "paket-internet": paket_internet,
        "aktivasi-voucher-internet": aktivasi_voucher_internet,
        "voucher-internet": voucher_internet,
        # "pulsa": "pulsa",
        "topup-game": topup_game
    }.get(product, "lainnya")

    # Tentukan kategori berdasarkan produk yang dipilih
    kategori = {
        "paket-internet": "paket internet",
        "aktivasi-voucher-internet": "aktivasi voucher internet",
        "voucher-internet": "voucher internet",
        "pulsa": "pulsa",
        "topup-game": "topup game",
    }.get(product, "lainnya")  # Sesuaikan kategori dengan skema

    total_urls = sum(len(source["urls"]) for source in sources)
    processed_urls = 0

    for source in sources:
        provider = source["provider"]
        urls = source["urls"]

        for url in urls:
            new_data = []
            try:
                res = requests.get(url)
                html = res.text
                soup = BeautifulSoup(html, 'html.parser')

                title = soup.select_one(".payment_title").text

                for row in soup.select("table.hidden-xs tbody tr"):
                    kode = row.select_one("td:nth-child(1)").text.strip()
                    # Skip kode tertentu
                    if kode in KODE_SKIP:
                        continue
                    produk = row.select_one("td:nth-child(2)").text.strip()
                    desc = row.select_one("td:nth-child(2) b").get("data-title", "").replace("\n", " ").strip() or "tidak ada deskripsi"
                    strHaga = row.select_one("td:nth-child(3)").text.strip()
                    harga = hapus_rp(strHaga)
                    harga_jual = get_total_harga_pulsa(produk) if product == "pulsa" else konversi_harga(kode, harga)
                    order = row.select_one("td:nth-child(4)").text.strip()
                    aktif = True if kode in list_aktif_now else False

                    # Ambil link dari elemen <a>
                    link_tag = row.select_one("a")
                    link = link_tag.get("href") if link_tag else None

                    # Cek duplikasi berdasarkan kode
                    if kode in collected_ids:
                        duplicates.append(kode)
                        print(f"kode: {kode}\n dan link nya {url}")
                    else:
                        collected_ids.add(kode)

                    if harga_jual == 0:
                        continue
                    
                    # Membuat data untuk dikirim ke Sanity
                    new_data.append({
                        "kode": kode,
                        "provider": provider,
                        "jenisPaket": " ".join(title.split(" ")[1:]),
                        "kategori": kategori,
                        "produk": produk,
                        "desc": desc,
                        "harga": harga,
                        "hargaJual": harga_jual,
                        "order": order,
                        "aktif": aktif,
                        "link": link,  # field baru
                        "dibuatPada": current_time
                    })
            except Exception as e:
                print(f"Error saat mengakses {url}: {e}")

            data.extend(new_data)
            processed_urls += 1
            progress = (processed_urls / total_urls) * 100
            print(f"Progress: {progress:.2f}%", end="\r")
            time.sleep(0.1)  # Optional: Untuk simulasi loading

    # Ambil data manual
    manual_data = get_manual_data(product)

    # Gabungkan
    data.extend(manual_data)
    
    # Cek dan tampilkan duplikasi jika ada
    if duplicates:
        print(f"Duplikasi ditemukan untuk kode: {duplicates}")
    else:
        print("Tidak ada duplikasi ditemukan.")

    print(f"Scraping selesai, total {len(data)} data berhasil dikumpulkan.")
    
    # Kirim semua data ke Sanity
    if data:
        mutations = {
            "mutations": [
                {
                    "createOrReplace": {
                        # "_id": f"paket-{item['kode']}",
                        "_type": "paket",
                        **item
                    }
                } for item in data
            ]
        }

        try:
            response = requests.post(sanity_url_mutate, headers=headers, data=json.dumps(mutations))
            if response.status_code == 200 or response.status_code == 202:
                print(f"Data berhasil ditambahkan ke Sanity.")
                print(f"Jumlah data yang berhasil disimpan: {len(data)}")  # Menampilkan jumlah data

            else:
                print(f"Error saat menambahkan data: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error saat mengirim data ke Sanity: {e}")

    return data

# Gabungkan proses hapus dan scrap
def hapus_dan_scrap_data(source_urls, product):
    # Tentukan kategori berdasarkan produk
    kategori = {
        "paket-internet": "paket internet",
        "aktivasi-voucher-internet": "aktivasi voucher internet",
        "voucher-internet": "voucher internet",
        "pulsa": "pulsa",
        "topup-game": "topup game"
    }.get(product, "lainnya")
    
    # Hapus data terlebih dahulu
    hapus_data_paket_by_kategori(kategori)
    
    # Lakukan proses scraping
    print("Memulai proses scraping...")
    data = scrap_from_url(source_urls, product)
    return data

# Input dari pengguna
pilih_product = ["paket-internet", "aktivasi-voucher-internet", "voucher-internet", "pulsa", "topup-game"]
paket = input("Pilih paket (paket-internet, aktivasi-voucher-internet, voucher-internet, pulsa, topup-game): ").strip().lower()

while True:
    if paket in pilih_product:
        print(f"Paket yang dipilih adalah: {paket.replace('-', ' ').title()}")
        break
    else:
        print("Paket tidak valid. Silakan pilih dari paket yang tersedia: paket-internet, aktivasi-voucher-internet, pulsa.")
        paket = input("Pilih paket (paket-internet, aktivasi-voucher-internet, pulsa): ").strip().lower()

# Panggil fungsi gabungan
hapus_dan_scrap_data(source_urls, paket)
