import requests

# Konfigurasi API Sanity
PROJECT_ID = "bkraz3f2"  # Ganti dengan Project ID Anda
DATASET = "production"        # Ganti dengan Dataset Anda
API_TOKEN = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"    # Ganti dengan API Token Anda
SANITY_API_URL = f"https://{PROJECT_ID}.api.sanity.io/v2021-06-07/data/query/{DATASET}"
SANITY_MUTATION_URL = f"https://{PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/{DATASET}"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def get_all_paket_ids(kategori):
    """Mengambil semua _id dari dokumen dengan kategori tertentu."""
    query = f'*[_type == "paket" && kategori == "{kategori}"]{ "{ _id }" }'
    response = requests.get(SANITY_API_URL, headers=headers, params={"query": query})

    if response.status_code == 200:
        result = response.json()
        ids = [doc['_id'] for doc in result.get('result', [])]
        return ids
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return []

def delete_paket_documents(ids):
    """Menghapus dokumen berdasarkan daftar ID."""
    mutations = [{"delete": {"id": _id}} for _id in ids]
    payload = {"mutations": mutations}

    response = requests.post(SANITY_MUTATION_URL, headers=headers, json=payload)

    if response.status_code in [200, 202]:
        print(f"Successfully deleted {len(ids)} documents.")
    else:
        print(f"Error deleting documents: {response.status_code} - {response.text}")

if __name__ == "__main__":
    kategori = "paket internet"
    print(f"Fetching all paket IDs with kategori '{kategori}'...")
    ids = get_all_paket_ids(kategori)

    if ids:
        print(f"Found {len(ids)} documents. Proceeding to delete...")
        delete_paket_documents(ids)
    else:
        print("No documents found to delete.")
