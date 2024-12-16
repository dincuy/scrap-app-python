import requests

# Konfigurasi API Sanity
SANITY_PROJECT_ID = "bkraz3f2"  # Ganti dengan Project ID Anda
SANITY_DATASET = "production"        # Ganti dengan dataset yang digunakan
SANITY_API_VERSION = "2022-03-07"      # Versi API Sanity
SANITY_TOKEN = "skaXZxlj9v8JJwm9lLUT919cI3aTvla0A1KmT3qNirYqywZzCf0sEVsem8nvQSafgrNeIcCw4h96gEcAXPLJf79bwlmpavoWYgQT0KnyVaenBWIolPq1AWsFFbVDkPFfMJh2pbxHMyoHp33dPD0MBf3O8R1ud2nTbqN0eFouHeqgkFbUZUSy"     # Ganti dengan token API Sanity Anda

# URL endpoint untuk menambahkan dokumen ke Sanity
SANITY_API_URL = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"

# Data JSON Anda
data = [
  {
    "nama": "A badru",
    "macAddress": "20:34:fb:d1:f7:7c",
    "dibuatPada": "14 Juli 2024 13.27.04"
  },
  {
    "nama": "Adina si hasan",
    "macAddress": "20:5e:f7:51:07:3c",
    "dibuatPada": "10 Juli 2024 16.12.37"
  },
  {
    "nama": "Bdk cep arif btr",
    "macAddress": "68:bf:c4:3d:65:c2",
    "dibuatPada": "16 September 2024 08.11.27"
  },
  {
    "nama": "Bdk cep arif redmi",
    "macAddress": "D0:9c:7a:07:9f:b4",
    "dibuatPada": "22 September 2024 14.29.15"
  },
  {
    "nama": "Bdk jemah",
    "macAddress": "C0:47:54:9c:9c:31",
    "dibuatPada": "16 September 2024 08.16.21"
  },
  {
    "nama": "Bdk jemah 2",
    "macAddress": "9c:6b:72:6b:fd:83",
    "dibuatPada": "16 September 2024 08.19.58"
  },
  {
    "nama": "bocah",
    "macAddress": "68:Bf:C4:78:88:77",
    "dibuatPada": "7 Agustus 2024 13.43.08"
  },
  {
    "nama": "Budak cep arif tea",
    "macAddress": "94:e1:29:5b:3f:8a",
    "dibuatPada": "24 Juli 2024 14.25.34"
  },
  {
    "nama": "Budak mang kalim",
    "macAddress": "30:1a:ba:12:c8:b3",
    "dibuatPada": "10 Juli 2024 08.47.46"
  },
  {
    "nama": "Dewi",
    "macAddress": "d4:1a:3f:81:8c:78",
    "dibuatPada": "10 Juli 2024 08.44.16"
  },
  {
    "nama": "Dewi teman 1",
    "macAddress": "20:5e:f7:b2:05:00",
    "dibuatPada": "10 Juli 2024 08.45.04"
  },
  {
    "nama": "Dewi teman 2",
    "macAddress": "20:5e:f7:80:f2:c2",
    "dibuatPada": "10 Juli 2024 08.45.37"
  },
  {
    "nama": "Dewi teman 3 realme c11",
    "macAddress": "44:8c:00:49:f2:2d",
    "dibuatPada": "10 Juli 2024 08.46.12"
  },
  {
    "nama": "Dewi teman 4 tab",
    "macAddress": "98:b0:8b:69:30:12",
    "dibuatPada": "10 Juli 2024 08.47.00"
  },
  {
    "nama": "Dewi teman 5",
    "macAddress": "Fc:a9:f5:5a:6d:3d",
    "dibuatPada": "24 Juli 2024 10.55.23"
  },
  {
    "nama": "Dina",
    "macAddress": "58:D6:97:38:00:61",
    "dibuatPada": "15 September 2024 08.25.01"
  },
  {
    "nama": "Dina sam",
    "macAddress": "20:5e:f7:1d:fb:e4",
    "dibuatPada": "10 Juli 2024 16.18.43"
  },
  {
    "nama": "Farid",
    "macAddress": "9a:d7:36:54:77:11",
    "dibuatPada": "10 Juli 2024 16.16.28"
  },
  {
    "nama": "Haifa",
    "macAddress": "00:ec:0a:f4:76:97",
    "dibuatPada": "10 Juli 2024 16.14.44"
  },
  {
    "nama": "Ipan",
    "macAddress": "Cc:42:10:c5:07:fd",
    "dibuatPada": "10 Juli 2024 16.16.10"
  },
  {
    "nama": "Ipan oppo",
    "macAddress": "4c:1a:3d:87:00:4f",
    "dibuatPada": "10 September 2024 20.34.27"
  },
  {
    "nama": "Laptop aini",
    "macAddress": "D0:39:57:a6:92:7b",
    "dibuatPada": "22 September 2024 14.30.04"
  },
  {
    "nama": "Laptop muf",
    "macAddress": "10:08:b1:f1:ad:37",
    "dibuatPada": "10 Juli 2024 08.43.22"
  },
  {
    "nama": "Laptop Zahra",
    "macAddress": "9c:4e:36:ca:f9:70",
    "dibuatPada": "13 Juli 2024 11.45.29"
  },
  {
    "nama": "My chromebook",
    "macAddress": "AC:82:47:A5:98:76",
    "dibuatPada": "10 Juli 2024 00.08.40"
  },
  {
    "nama": "My chromecast",
    "macAddress": "D0:C0:BF:91:62:F8",
    "dibuatPada": "10 Juli 2024 00.10.07"
  },
  {
    "nama": "My laptop",
    "macAddress": "74:e5:43:90:dd:27",
    "dibuatPada": "10 Juli 2024 00.09.35"
  },
  {
    "nama": "My redmi 4x",
    "macAddress": "ec:d0:9f:23:68:50",
    "dibuatPada": "10 Juli 2024 00.10.44"
  },
  {
    "nama": "My tab spen",
    "macAddress": "68:Bf:C4:78:05:64",
    "dibuatPada": "25 Juli 2024 18.45.27"
  },
  {
    "nama": "Neng aini",
    "macAddress": "e0:1f:88:50:79:52",
    "dibuatPada": "10 Juli 2024 16.19.50"
  },
  {
    "nama": "Pamajikan apid",
    "macAddress": "40:8e:f6:62:4b:bd",
    "dibuatPada": "10 Juli 2024 08.43.49"
  },
  {
    "nama": "Prol 1",
    "macAddress": "A0:d8:07:6d:f8:3f",
    "dibuatPada": "10 Juli 2024 16.17.39"
  },
  {
    "nama": "Prol iphone",
    "macAddress": "CE:4E:A7:FF:55:8B",
    "dibuatPada": "10 Juli 2024 16.17.19"
  },
  {
    "nama": "Teh enung",
    "macAddress": "88:d5:0c:1e:a9:32",
    "dibuatPada": "13 Juli 2024 11.45.00"
  },
  {
    "nama": "Teh sari",
    "macAddress": "20:cd:6e:e8:8b:01",
    "dibuatPada": "10 Juli 2024 16.19.31"
  },
  {
    "nama": "Th popon",
    "macAddress": "24:79:f3:f7:b8:27",
    "dibuatPada": "6 September 2024 21.43.54"
  },
  {
    "nama": "Tiara",
    "macAddress": "20:34:fb:d2:ca:80",
    "dibuatPada": "10 Juli 2024 16.16.51"
  },
  {
    "nama": "Tiara new",
    "macAddress": "Bc:B2:Cc:27:4b:2c",
    "dibuatPada": "10 Juli 2024 16.15.22"
  },
  {
    "nama": "uwal",
    "macAddress": "8c:e0:42:b3:bc:47",
    "dibuatPada": "24 Juli 2024 10.54.44"
  }
]


# Fungsi untuk menyimpan data ke Sanity
def save_to_sanity(data):
    headers = {
        "Authorization": f"Bearer {SANITY_TOKEN}",
        "Content-Type": "application/json",
    }
    
    mutations = {
        "mutations": [
            {
                "create": {
                    "_type": "wifiCustomer",
                    "namaPelanggan": item["nama"],
                    "alamatMacWifi": item["macAddress"],
                }
            }
            for item in data
        ]
    }

    response = requests.post(SANITY_API_URL, json=mutations, headers=headers)
    
    if response.status_code == 200:
        print("Data berhasil disimpan:", response.json())
    else:
        print("Gagal menyimpan data:", response.text)

# Jalankan fungsi untuk menyimpan
save_to_sanity(data)
