import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://biletinial.com/tr-tr/mekan/sakip-sabanci-muzesi-sbtk"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

response = requests.get(URL, headers={
    "User-Agent": "Mozilla/5.0"
})

soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text(" ", strip=True)

films = [
    "Power Ballad",
    "Ferris Bueller's Day Off",
    "Only You"
]

for film in films:
    if film in text:
        print(f"{film}: Etkinlik bulundu")

        if "TÜKENDİ" not in text:
            send_telegram(
                f"🎟️ BİLET BULUNDU!\n\n"
                f"🎬 {film}\n"
                f"🎫 2 bilet için Biletinial'ı kontrol et:\n"
                f"{URL}"
            )
