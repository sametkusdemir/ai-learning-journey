import json

ALANLAR = {
    "tarih_ham": (str, type(None)),
    "urun": (str, type(None)),
    "alan_donum": (int, float, type(None)),
    "islem": (str, type(None)),
    "yontem": (str, type(None)),
    "sure_saat": (int, float, type(None)),
    "girdi": (str, type(None)),
    "doz_miktar": (int, float, type(None)),
    "doz_birim": (str, type(None)),
    "doz_olcu": (str, type(None)),
    "amac": (str, type(None)),
    "gozlem": (str, type(None)),
    "yapilmayan": (str, type(None)),
    "belirsiz": (bool,),
}

def dogrula(metin: str) -> tuple[dict | None, list[str]]:
    """Model çıktısını kontrol eder. (veri, hata_listesi) döndürür."""
    hatalar = []
    try:
        veri = json.loads(metin)
    except json.JSONDecodeError as e:
        return None, [f"Geçersiz JSON: {e}"]

    for alan, tipler in ALANLAR.items():
        if alan not in veri:
            hatalar.append(f"Eksik alan: {alan}")
        elif not isinstance(veri[alan], tipler):
            hatalar.append(f"Yanlış tip: {alan} = {veri[alan]!r}")
    for alan in veri:
        if alan not in ALANLAR:
            hatalar.append(f"Şemada olmayan alan: {alan}")
    return veri, hatalar

if __name__ == "__main__":
    ornekler = [
        # 1) temiz çıktı
        '{"tarih_ham":"salı","urun":"arpa","alan_donum":null,"islem":"sulama","yontem":null,"sure_saat":null,"girdi":null,"doz_miktar":null,"doz_birim":null,"doz_olcu":null,"amac":null,"gozlem":null,"yapilmayan":"ilaçlama","belirsiz":true}',
        # 2) modelin açıklama eklediği bozuk çıktı
        'İşte JSON: {"urun":"arpa"}',
        # 3) tip hatası
        '{"tarih_ham":"salı","urun":"arpa","alan_donum":"on","islem":null,"yontem":null,"sure_saat":null,"girdi":null,"doz_miktar":null,"doz_birim":null,"doz_olcu":null,"amac":null,"gozlem":null,"yapilmayan":null,"belirsiz":"evet"}',
    ]
    for i, o in enumerate(ornekler, 1):
        veri, hatalar = dogrula(o)
        print(f"Örnek {i}:", "✅ geçerli" if not hatalar else hatalar)