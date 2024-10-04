import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from pymongo import MongoClient

from konversi import konversi_harga, get_total_harga_pulsa
from source_urls import source_urls

def scrap_from_url(source_urls, product):
    # Koneksi ke MongoDB
    client = MongoClient('mongodb+srv://dincuy:6IfUzvj3k7DhTqzc@dincuy-shop.crioxcr.mongodb.net/konter?retryWrites=true&w=majority&appName=dincuy-shop')
    db = client['konter'] # nama database
    collection = db[product] #nama koleksi

    jumlah_dokumen = collection.count_documents({})
    if jumlah_dokumen > 0:
        collection.delete_many({})
        print("Delete dulu boss")
    
    sources = source_urls[product]
    data = []
    current_time = datetime.now().strftime("Jam %H:%M:%S, %d %B %Y")
    
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
                    harga_jual = get_total_harga_pulsa(produk) if product == "pulsa" else konversi_harga(harga, 2000)
                    order = row.select_one("td:nth-child(4)").text.strip()

                    new_data.append({
                        "kode": kode,
                        "provider": provider,
                        "jenisPaket": " ".join(title.split(" ")[1:]),
                        "produk": produk,
                        "desc": desc,
                        "harga": harga,
                        "hargaJual": harga_jual,
                        "order": order,
                        "dibuatPada": current_time  # Menambahkan waktu dan tanggal saat ini
                    })
            except Exception as e:
                print(f"Error saat mengakses {url}: {e}")

            data.extend(new_data)
            
            # Simpan data ke MongoDB
            if new_data:
                collection.insert_many(new_data)

            processed_urls += 1
            progress = (processed_urls / total_urls) * 100
            print(f"Progress: {progress:.2f}%", end="\r")
            time.sleep(0.1)  # Optional: Untuk simulasi loading

    # Menyimpan data ke dalam file JSON
    # with open(f'{product}_data.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Data berhasil disimpan ke koleksi {product} di mongoDB")
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
