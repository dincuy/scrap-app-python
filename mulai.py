import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
# from konversi import konversi_harga, get_total_harga_pulsa
from source_urls import source_urls
from helper.list_aktif import paket_internet_voucher, topup_game

def hapus_rp(nominal):
    nominal_int = int(''.join(filter(str.isdigit, nominal)))
    return nominal_int

def konversi_harga(kode, nominal):
    # Tentukan keuntungan berdasarkan nominal
    profit = 2000 if nominal < 50000 else 3000

    # Hitung total harga dengan keuntungan
    new_total_harga = nominal + profit

    # Dapatkan ribuan dan ratusan
    ribuan = (new_total_harga // 1000) * 1000
    ratusan = new_total_harga % 1000

    # Bulatkan sesuai aturan yang diberikan
    bulatkan = ribuan + 1000 if ratusan >= 500 else ribuan

    # Format ke dalam Rupiah dengan format yang diinginkan
    # return "Rp. {:,}".format(bulatkan).replace(",", ".")
    match kode:
        case "CAXSS5":
            bulatkan = 11000
        case "AXLBB3K3":
            bulatkan = 13000
        case "AVZMINI1":
            bulatkan = 15000
        case "SDZ1":
            bulatkan = 16000
        case "CAD2" | "IVXBP2K7":
            bulatkan = 17000
        case "SDZ3" | "IVXBP5K3" | "AXLBB3K5":
            bulatkan = 18000
        case "AXLBB3K7":
            bulatkan = 24000
        case "SDZ8":
            bulatkan = 29000
    return bulatkan


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

# Fungsi untuk melakukan scraping data
def scrap_from_url(source_urls, product):
    sources = source_urls[product]
    data = []
    current_time = datetime.now().isoformat()  # Menggunakan format ISO-8601 yang valid
    collected_ids = set()  # Untuk mengecek duplikasi
    duplicates = []  # Menyimpan kode yang duplikat
    
    list_aktif_now = {
        "paket-internet": paket_internet_voucher,
        "voucher-internet": paket_internet_voucher,
        # "pulsa": "pulsa",
        "topup-game": topup_game
    }.get(product, "lainnya")

    # Tentukan kategori berdasarkan produk yang dipilih
    kategori = {
        "paket-internet": "paket internet",
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
                    produk = row.select_one("td:nth-child(2)").text.strip()
                    desc = row.select_one("td:nth-child(2) b").get("data-title", "").replace("\n", " ").strip() or "tidak ada deskripsi"
                    strHaga = row.select_one("td:nth-child(3)").text.strip()
                    harga = hapus_rp(strHaga)
                    harga_jual = get_total_harga_pulsa(produk) if product == "pulsa" else konversi_harga(kode, harga)
                    order = row.select_one("td:nth-child(4)").text.strip()
                    aktif = True if kode in list_aktif_now else False

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
                        "kategori": kategori,  # Menggunakan kategori sesuai skema
                        "produk": produk,
                        "desc": desc,
                        "harga": harga,
                        "hargaJual": harga_jual,
                        "order": order,
                        "aktif": aktif,
                        "dibuatPada": current_time  # Menggunakan format ISO-8601
                    })
            except Exception as e:
                print(f"Error saat mengakses {url}: {e}")

            data.extend(new_data)
            processed_urls += 1
            progress = (processed_urls / total_urls) * 100
            print(f"Progress: {progress:.2f}%", end="\r")
            time.sleep(0.1)  # Optional: Untuk simulasi loading

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
pilih_product = ["paket-internet", "voucher-internet", "pulsa", "topup-game"]
paket = input("Pilih paket (paket-internet, voucher-internet, pulsa, topup-game): ").strip().lower()

while True:
    if paket in pilih_product:
        print(f"Paket yang dipilih adalah: {paket.replace('-', ' ').title()}")
        break
    else:
        print("Paket tidak valid. Silakan pilih dari paket yang tersedia: paket-internet, voucher-internet, pulsa.")
        paket = input("Pilih paket (paket-internet, voucher-internet, pulsa): ").strip().lower()

# Panggil fungsi gabungan
hapus_dan_scrap_data(source_urls, paket)
