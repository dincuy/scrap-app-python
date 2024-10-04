def konversi_harga(nominal):
    # Konversi nominal menjadi integer
    nominal_int = int(''.join(filter(str.isdigit, nominal)))

    # Tentukan keuntungan berdasarkan nominal
    profit = 2000 if nominal_int < 50000 else 3000

    # Hitung total harga dengan keuntungan
    new_total_harga = nominal_int + profit

    # Dapatkan ribuan dan ratusan
    ribuan = (new_total_harga // 1000) * 1000
    ratusan = new_total_harga % 1000

    # Bulatkan sesuai aturan yang diberikan
    bulatkan = ribuan + 1000 if ratusan >= 500 else ribuan

    # Format ke dalam Rupiah dengan format yang diinginkan
    return "Rp. {:,}".format(bulatkan).replace(",", ".")


def get_total_harga_pulsa(str_nominal):
    if str_nominal == "Pulsa - Cek Hutang Pulsa / Paket Darurat":
        return "Rp. 0"
    num = int(''.join(filter(str.isdigit, str_nominal)))

    if "Pulsa Transfer" in str_nominal:
        num_total_harga = num + 1000
        return "Rp. {:,}".format(num_total_harga).replace(",", ".")

    if num < 5000:
        num_total_harga = num + 1000
    elif num >= 10000 and num < 50000:
        num_total_harga = num + 2000
    else:
        num_total_harga = num + 3000

    return "Rp. {:,}".format(num_total_harga).replace(",", ".")

# Contoh penggunaan
# print(konversi_harga("Rp. 5000", 2000))
# print(get_total_harga_pulsa("Pulsa 3000"))
