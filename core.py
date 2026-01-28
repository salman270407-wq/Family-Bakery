import json
from pathlib import Path

# Lokasi file FAQ
BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_toko.json"

# Load data FAQ saat aplikasi dijalankan
with FAQ_FILE.open("r", encoding="utf-8") as f:
    FAQS = json.load(f)

def get_bot_reply(user_message: str) -> str:
    """
    Fungsi utama untuk menjawab pertanyaan.
    Dipakai bersama oleh web dan Telegram.
    """
    text = (user_message or "").lower()

    katakasar = ["anjing, tai, tolol, babi, monyet, bangsat, bajingan"]
    if any(s in text for s in katakasar):
        return (
            "bangsat 👋\n"
            "Silakan tanya seputar jam operasional, alamat, cara order, atau produk kami."
        )

    # 1. Cek kecocokan dengan daftar FAQ berdasarkan keyword
    for faq in FAQS:
        for kw in faq["keywords"]:
            if kw in text:
                return faq["answer"]

    # 2. Respon sapaan umum
    sapaan = ["halo", "hallo", "hai", "assalamualaikum", "assalamu'alaikum", "pagi", "siang", "sore", "malam"]
    if any(s in text for s in sapaan):
        return (
            "Halo, selamat datang di Family Bakery 👋\n"
            "Silakan tanya seputar jam operasional, alamat, cara order, atau produk kami."
        )

    # 3. Jawaban default kalau tidak ditemukan
    return (
        "Maaf, mungkin yang anda maksud  Menu & produk roti\n• Jam operasional toko\n• Alamat & lokasi\n• Cara pemesanan.\n"
        "Coba tanyakan dengan kalimat lain atau hubungi WhatsApp 087850670438 ya 😊"
    )
