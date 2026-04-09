from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_steam_deals():
    try:
        # Steam'in vitrinindeki özel fırsatları Türkiye fiyatlarıyla çekiyoruz
        url = "https://store.steampowered.com/api/featuredcategories?cc=tr&l=turkish"
        response = requests.get(url, timeout=10).json()
        
        # 'specials' kategorisi indirimdeki oyunları içerir
        specials = response.get('specials', {}).get('items', [])
        
        oyunlar = []
        for game in specials[:15]:  # İlk 15 büyük fırsatı çekelim
            # Fiyatları kuruş formatından TL formatına çeviriyoruz
            eski_fiyat = f"{game['original_price']/100:.2f} TL" if 'original_price' in game else ""
            yeni_fiyat = f"{game['final_price']/100:.2f} TL"
            
            oyunlar.append({
                "ad": game['name'],
                "indirim": game.get('discount_percent', 0),
                "eski_fiyat": eski_fiyat,
                "yeni_fiyat": yeni_fiyat,
                "resim": game['large_capsule_image'],
                "link": f"https://store.steampowered.com/app/{game['id']}"
            })
        return oyunlar
    except Exception as e:
        print(f"Hata: {e}")
        return []

@app.route("/")
def index():
    firsatlar = get_steam_deals()
    return render_template("index.html", firsatlar=firsatlar)

if __name__ == "__main__":
    app.run(debug=True)