import requests
import json
from datetime import datetime

# Konfigurasi API Sanity
# Konfigurasi API Sanity
SANITY_PROJECT_ID = "bkraz3f2"  # Ganti dengan Project ID Anda
SANITY_DATASET = "production"        # Ganti dengan dataset yang digunakan
SANITY_API_VERSION = "2022-03-07"      # Versi API Sanity
SANITY_TOKEN = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"     # Ganti dengan token API Sanity Anda

# URL endpoint untuk melakukan mutate (menambahkan data)
url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"

# Headers untuk mengirim request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SANITY_TOKEN}",
}

# Data yang ingin ditambahkan ke Sanity sesuai skema 'paket'
data = {
    "mutations": [
        {
            "create": {
                "_type": "paket",  # Tipe dokumen sesuai skema Sanity
                "kode": "PAK001",
                "provider": "Provider XYZ",
                "jenisPaket": "Unlimited",
                "kategori": "paket internet",
                "produk": "Paket Data Unlimited",
                "desc": "Paket data unlimited dengan kecepatan tinggi",
                "harga": "Rp 100.000",
                "hargaJual": "Rp 120.000",
                "order": "1",
                "dibuatPada": datetime.now().isoformat(),  # Menggunakan format ISO
            }
        }
    ]
}

# Mengirim data ke Sanity
response = requests.post(url, headers=headers, data=json.dumps(data))

# Memeriksa respons dari Sanity
if response.status_code == 200:
    print("Data berhasil ditambahkan:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
