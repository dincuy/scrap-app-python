import json
import requests

# Konfigurasi API Sanity
SANITY_PROJECT_ID = "bkraz3f2"  # Ganti dengan Project ID Anda
SANITY_DATASET = "production"   # Ganti dengan dataset yang digunakan
SANITY_API_VERSION = "2022-03-07"   # Versi API Sanity
SANITY_TOKEN = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"  # Ganti dengan token API Sanity Anda

# URL endpoint untuk query dan mutasi data di Sanity
sanity_url_query = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
sanity_url_mutate = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"

# Headers untuk mengotorisasi request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SANITY_TOKEN}",
}

def get_all_paket_ids():
    """Mendapatkan semua _id dari dokumen tipe 'paket' di Sanity"""
    query = '*[_type == "paket"]{_id}'
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

def delete_paket_documents(ids):
    """Menghapus dokumen berdasarkan _id yang diperoleh"""
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

def hapus_semua_data_paket():
    """Fungsi utama untuk menghapus semua dokumen 'paket'"""
    print("Mengambil semua _id dari dokumen 'paket'...")
    ids = get_all_paket_ids()
    if ids:
        print(f"Ditemukan {len(ids)} dokumen. Menghapus...")
        delete_paket_documents(ids)
    else:
        print("Tidak ada dokumen 'paket' yang ditemukan.")

# Panggil fungsi untuk menghapus semua data 'paket'
hapus_semua_data_paket()
