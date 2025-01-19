import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
# from konversi import konversi_harga, get_total_harga_pulsa
# from source_urls import source_urls

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
        case "DTTTBR153" | "VJABAR153":
            bulatkan = 10000
        case "VJABAR255" | "DTTTBR255" | "VJBR33":
            bulatkan = 15000
        case "VJBR35" | "SDA3G5NA":
            bulatkan = 16000
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

paket_internet_urls = [
    {
        "provider": "axis",
        "urls": [
            "https://isipulsa.web.id/harga/paket-internet/axis-kuota-harian-nasional",
            "https://isipulsa.web.id/harga/paket-internet/axis-kuota-harian-nasional?page=2",
            # "https://isipulsa.web.id/harga/paket-internet/axis-masa-aktif-1-bulan",
            "https://isipulsa.web.id/harga/paket-internet/axis-bonus-lokal-jawa"
        ],
    },
    {
        "provider": "indosat",
        "urls": [
            "https://isipulsa.web.id/harga/paket-internet/indosat-11",
            "https://isipulsa.web.id/harga/paket-internet/indosat-mini-kuota-bulanan",
            "https://isipulsa.web.id/harga/paket-internet/indosat-mini-kuota-bulanan?page=2",
            "https://isipulsa.web.id/harga/paket-internet/indosat-old-freedom",
            "https://isipulsa.web.id/harga/paket-internet/indosat-yellow",
            "https://isipulsa.web.id/harga/paket-internet/indosat-freedom-internet-max"
        ],
    },
    {
        "provider": "telkomsel",
        "urls": [
            # paket kuota
            "https://isipulsa.web.id/harga/paket-kuota/telkomsel-kuota-lokal-jawa-barat",
            # paket internet
            "https://isipulsa.web.id/harga/paket-internet/telkomsel-kuota-mini",
            "https://isipulsa.web.id/harga/paket-internet/telkomsel-kuota-mini?page=2",
            "https://isipulsa.web.id/harga/paket-internet/telkomsel-kuota-mini?page=3",
            "https://isipulsa.web.id/harga/paket-internet/telkomsel-tsel-flash-full",
            "https://isipulsa.web.id/harga/paket-internet/telkomsel-tsel-flash-full?page=2",
            "https://isipulsa.web.id/harga/paket-internet/telkomsel-tsel-flash-full?page=3"
        ],
    },
    {
        "provider": "three",
        "urls": [
            "https://isipulsa.web.id/harga/paket-internet/three-23",
            "https://isipulsa.web.id/harga/paket-internet/three-kuota-mini",
            "https://isipulsa.web.id/harga/paket-internet/three-happy",
            "https://isipulsa.web.id/harga/paket-internet/three-happy?page=2",
            "https://isipulsa.web.id/harga/paket-internet/three-data-bulanan",
        ],
    },
    {
        "provider": "xl",
        "urls": [
            "https://isipulsa.web.id/harga/paket-internet/xl-kuota-mini",
            "https://isipulsa.web.id/harga/paket-internet/xl-kuota-mini?page=2",
            "https://isipulsa.web.id/harga/paket-internet/xl-kuota-mini?page=3",
            "https://isipulsa.web.id/harga/paket-internet/xl-kuota-mini?page=4",
            "https://isipulsa.web.id/harga/paket-internet/xl-xtra-combo-flex",
            "https://isipulsa.web.id/harga/paket-internet/xl-kuota-jumbo",
        ],
    },
]

voucher_internet_urls = [
    {
        "provider": "axis",
        "urls": [
            "https://isipulsa.web.id/harga/voucher-internet/axis-aigo",
            "https://isipulsa.web.id/harga/voucher-internet/axis-nasional",
        ],
    },
    {
        "provider": "indosat",
        "urls": [
            "https://isipulsa.web.id/harga/voucher-internet/indosat-freedom-u",
            "https://isipulsa.web.id/harga/voucher-internet/indosat-old-freedom-324",
            "https://isipulsa.web.id/harga/voucher-internet/indosat-freedom-mini-harian",
        ],
    },
    {
        "provider": "telkomsel",
        "urls": [
            "https://isipulsa.web.id/harga/voucher-internet/telkomsel-khusus-daerah-jawa-barat",
        ],
    },
    {
        "provider": "three",
        "urls": ["https://isipulsa.web.id/harga/voucher-internet/three-always-on"],
    },
    {
        "provider": "xl",
        "urls": [
            "https://isipulsa.web.id/harga/fitur-voucher/xl-aktivasi-combo-flex",
            "https://isipulsa.web.id/harga/fitur-voucher/xl-aktivasi-hotrod-spesial",
            "https://isipulsa.web.id/harga/fitur-voucher/xl-aktivasi-paket-harian",
            "https://isipulsa.web.id/harga/fitur-voucher/xl-aktivasi-bebas-puas-2k",
            "https://isipulsa.web.id/harga/fitur-voucher/xl-aktivasi-bebas-puas-3k",
            "https://isipulsa.web.id/harga/fitur-voucher/xl-aktivasi-bebas-puas-5k",  
        ],
    },
]

pulsa_urls = [
    {
        "provider": "axis",
        "urls": ["https://isipulsa.web.id/harga/pulsa/axis-5"],
    },
    {
        "provider": "indosat",
        "urls": ["https://isipulsa.web.id/harga/pulsa/indosat-2"],
    },
    {
        "provider": "telkomsel",
        "urls": ["https://isipulsa.web.id/harga/pulsa/telkomsel-1"],
    },
    {
        "provider": "three",
        "urls": ["https://isipulsa.web.id/harga/pulsa/three-4"],
    },
    {
        "provider": "xl",
        "urls": ["https://isipulsa.web.id/harga/pulsa/xl-3"],
    },
]

source_urls = {
    "pulsa": pulsa_urls,
    "paket-internet": paket_internet_urls,
    "voucher-internet": voucher_internet_urls,
}

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

    # Tentukan kategori berdasarkan produk yang dipilih
    kategori = {
        "paket-internet": "paket internet",
        "voucher-internet": "voucher internet",
        "pulsa": "pulsa"
    }.get(product, "lainnya")  # Sesuaikan kategori dengan skema

    total_urls = sum(len(source["urls"]) for source in sources)
    processed_urls = 0
    listAktif = [
        "TDSL2",
        "DTTTBR153",
        "DTTTBR255",
        "FLASH255",
        "MGB4",
        "MGB5",
        "MGBMI3",
        "MG2SKSH",
        "MGMLM12",
        "MGM3",
        "MGA3",
        "SDA3G5NA",
        "TDKM3",
        "TDKM17",
        "TDKM37",
        "TFLASHK2",
        "TFLASHK3",
        "TFLASHK4",
        "TFLASHK5",
        "TFLASHK6",
        "TFLASHK7",
        "TFLASHK8",
        "SDG10",
        "TFLASHK11",
        "TFLASHS12",
        "TSELMINI27",
        "VJABAR153",
        "VJABAR255",
        "VJBR33",
        "VJBR35",
        "VJABAR357",
        "VAX1H1",
        "IV1",
        "VAXM1H3",
        "VAX1SH3",
        "VABMI3",
        "VAX2SH7",
        "MGM1GB1",
        "MGB1",
        "MGX1",
        "TDJBM6",
        # paket internet xl
        "XLDB5001",
        "DXBP5K1",
        "DXBP2K3",
        "DXBP5K3",
        "XLDB153",
        "DXBP2K5",
        "XLDB255",
        "XHPRO1",
        "XLDB357",
        "XHPRO4",
        "XHPRO2",
        "DXBP2K7",
        "XCFS",
        "XCFSS",
        "FLMM",
        "XCFL",
        # inject voucher xl
        "IVXFLXS",
        "IVXFLS",
        "AVXHS3",
        "AVXHS4",
        "IVXBP2K5",
        "IVXBP2K7",
        "IVXBP2K10",
        "AXLBB3K1",
        "AXLBB3K5",
        "AXLBB3K7",
        "AXLBB3K10",
        "IVXBP5K1",
        "IVXBP5K3",
        "IVXBP2K3",
        "AVXSM2",
        "AXLBB3K3",
    ]

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
                    aktif = True if kode in listAktif else False

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
        "pulsa": "pulsa"
    }.get(product, "lainnya")
    
    # Hapus data terlebih dahulu
    hapus_data_paket_by_kategori(kategori)
    
    # Lakukan proses scraping
    print("Memulai proses scraping...")
    data = scrap_from_url(source_urls, product)
    return data

# Input dari pengguna
pilih_product = ["paket-internet", "voucher-internet", "pulsa"]
paket = input("Pilih paket (paket-internet, voucher-internet, pulsa): ").strip().lower()

while True:
    if paket in pilih_product:
        print(f"Paket yang dipilih adalah: {paket.replace('-', ' ').title()}")
        break
    else:
        print("Paket tidak valid. Silakan pilih dari paket yang tersedia: paket-internet, voucher-internet, pulsa.")
        paket = input("Pilih paket (paket-internet, voucher-internet, pulsa): ").strip().lower()

# Panggil fungsi gabungan
hapus_dan_scrap_data(source_urls, paket)
