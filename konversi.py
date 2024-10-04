# import locale

# locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

def konversi_harga(nominal, profit):
    new_total_harga = int(''.join(filter(str.isdigit, nominal))) + profit

    # Dapatkan ribuan dan ratusan
    ribuan = (new_total_harga // 1000) * 1000
    ratusan = new_total_harga % 1000

    # Bulatkan sesuai aturan yang diberikan
    bulatkan = ribuan + 1000 if ratusan >= 500 else ribuan

    # return "Rp.{}".format(locale.format_string("%d", bulatkan, grouping=True))
    return "Rp. {:,}".format(bulatkan).replace(",", ".")

def get_total_harga_pulsa(str_nominal):
    if str_nominal == "Pulsa - Cek Hutang Pulsa / Paket Darurat":
        return "Rp. 0"
    num = int(''.join(filter(str.isdigit, str_nominal)))

    if "Pulsa Transfer" in str_nominal:
        num_total_harga = num + 1000
        # return "Rp. {}".format(locale.format_string("%d", num_total_harga, grouping=True))
        return "Rp. {:,}".format(num_total_harga).replace(",", ".")

    if num < 5000:
        num_total_harga = num + 1000
    else:
        num_total_harga = num + 2000

    # return "Rp. {}".format(locale.format_string("%d", num_total_harga, grouping=True))
    return "Rp. {:,}".format(num_total_harga).replace(",", ".")

# Contoh penggunaan
# print(konversi_harga("Rp. 5000", 2000))
# print(get_total_harga_pulsa("Pulsa 3000"))
