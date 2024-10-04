import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from konversi import konversi_harga, get_total_harga_pulsa
from source_urls import source_urls

# Konfigurasi API Sanity
SANITY_PROJECT_ID = "bkraz3f2"  # Ganti dengan Project ID Anda
SANITY_DATASET = "production"        # Ganti dengan dataset yang digunakan
SANITY_API_VERSION = "2022-03-07"      # Versi API Sanity
SANITY_TOKEN = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"     # Ganti dengan token API Sanity Anda

# URL endpoint untuk menambahkan dokumen ke Sanity
sanity_url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"

# Headers untuk mengotorisasi request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SANITY_TOKEN}",
}

def scrap_from_url(source_urls, product):
    sources = source_urls[product]
    data = []
    current_time = datetime.now().isoformat()  # Menggunakan format ISO-8601 yang valid
    collected_ids = set()  # Untuk mengecek duplikasi
    duplicates = []  # Menyimpan kode yang duplikat

    # Tentukan kategori berdasarkan produk yang dipilih
    kategori = {
        "paket-internet": "paket internet",
        "voucher-internet": "voucher internet",
        "pulsa": "pulsa"
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
                    harga = row.select_one("td:nth-child(3)").text.strip()

                    # # Penanganan konversi harga
                    # if harga == "Rp 0":
                    #     harga = 0
                    # # else:
                    # #     harga = 0  # Set default jika harga kosong
                        
                    harga_jual = get_total_harga_pulsa(produk) if product == "pulsa" else konversi_harga(harga, 2000)
                    order = row.select_one("td:nth-child(4)").text.strip()

                    # Cek duplikasi berdasarkan kode
                    if kode in collected_ids:
                        duplicates.append(kode)
                    else:
                        collected_ids.add(kode)

                    if harga_jual == "Rp. 0":
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
                        "_id": f"paket-{item['kode']}",
                        "_type": "paket",
                        **item
                    }
                } for item in data
            ]
        }

        try:
            response = requests.post(sanity_url, headers=headers, data=json.dumps(mutations))
            if response.status_code == 200 or response.status_code == 202:
                print(f"Data berhasil ditambahkan ke Sanity.")
            else:
                print(f"Error saat menambahkan data: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error saat mengirim data ke Sanity: {e}")

    return data

# Menanyakan paket yang dipilih
pilih_product = ["paket-internet", "voucher-internet", "pulsa"]
product = ''

paket = input("Pilih paket (paket-internet, voucher-internet, pulsa): ").strip().lower()

while True:
    if paket in pilih_product:
        print(f"Paket yang dipilih adalah: {paket.replace('-', ' ').title()}")
        product = paket
        break
    else:
        print("Paket tidak valid. Silakan pilih dari paket yang tersedia: paket-internet, voucher-internet, pulsa.")
        paket = input("Pilih paket (paket-internet, voucher-internet, pulsa): ").strip().lower()

scrap_from_url(source_urls, product)
