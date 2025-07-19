import requests

# Konfigurasi
project_id = "bkraz3f2"
dataset = "production"
api_token = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"

# URL untuk query & mutate
query_url = f"https://{project_id}.api.sanity.io/v2023-08-01/data/query/{dataset}?query=*[_type == 'paket']{{_id}}"
mutate_url = f"https://{project_id}.api.sanity.io/v2023-08-01/data/mutate/{dataset}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# --- 1. Ambil semua ID dokumen bertipe "paket" ---
res = requests.get(query_url, headers=headers)
data = res.json()
ids = [doc["_id"] for doc in data.get("result", [])]

print(f"Ditemukan {len(ids)} dokumen paket")

# --- 2. Hapus semua dokumen sekaligus (max 100 per request) ---
batch_size = 100
for i in range(0, len(ids), batch_size):
    batch_ids = ids[i:i + batch_size]
    mutations = [{"delete": {"id": doc_id}} for doc_id in batch_ids]
    
    response = requests.post(mutate_url, headers=headers, json={"mutations": mutations})
    
    if response.status_code == 200:
        print(f"✅ Berhasil menghapus {len(batch_ids)} dokumen")
    else:
        print("❌ Gagal menghapus:", response.text)
