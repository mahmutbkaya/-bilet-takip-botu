import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://biletinial.com/tr-tr/mekan/sakip-sabanci-muzesi-sbtk"

FILMS = [
    {
        "name": "Power Ballad",
        "date": "23 Temmuz 2026"
    },
    {
        "name": "Ferris Bueller's Day Off",
        "date": "28 Temmuz 2026"
    },
    {
        "name": "Only You",
        "date": "30 Temmuz 2026"
    }
]

def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        },
        timeout=20
    )

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Sayfadaki tüm metni alıyoruz
page_text = soup.get_text(" ", strip=True)

for film in FILMS:

    film_name = film["name"]

    if film_name not in page_text:
        print(f"{film_name}: Sayfada bulunamadı")
        continue

    # Film adından sonraki bölümde TÜKENDİ ifadesini arıyoruz
    film_position = page_text.find(film_name)

    next_film_positions = [
        page_text.find(other["name"], film_position + len(film_name))
        for other in FILMS
        if other["name"] != film_name
        and page_text.find(other["name"], film_position + len(film_name)) != -1
    ]

    if next_film_positions:
        end_position = min(next_film_positions)
        film_section = page_text[film_position:end_position]
    else:
        film_section = page_text[film_position:film_position + 500]

    if "TÜKENDİ" in film_section.upper():
        print(f"{film_name}: TÜKENDİ")
    else:
        print(f"{film_name}: BİLET AÇILMIŞ OLABİLİR!")

        message = (
            "🎟️ BİLET BULUNDU OLABİLİR!\n\n"
            f"🎬 {film_name}\n"
            f"📅 {film['date']}\n"
            "🎫 2 bilet için hemen kontrol et!\n\n"
            f"🔗 {URL}"
        )

        send_telegram(message)
