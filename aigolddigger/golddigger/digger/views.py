from django.shortcuts import render
from django.http import JsonResponse
import requests

def home(request):
    return render(request, 'home.html')

def get_bitcoin_price(request):
    def get_data():
        # Binance API endpoint'i
        binance_api_url = "https://api.binance.com/api/v3/ticker/price"
        
        # İlgili sembol (Bitcoin için BTCUSDT)
        symbol = "BTCUSDT"
        
        # API'den veri çekme
        try:
            response = requests.get(binance_api_url, params={"symbol": symbol})
            response.raise_for_status()  # HTTP hata durumunu kontrol et
            data = response.json()
            
            # Binance'den gelen veriyi işleme
            if "price" in data:
                return float(data['price'])  # Fiyatı float'a çevir
            else:
                return None  # Veri alınamadıysa None döndür

        except requests.exceptions.RequestException as e:
            return None  # Hata durumunda None döndür

    bitcoin_price = get_data()

    # JSON formatında yanıt döndür
    return JsonResponse({'price': bitcoin_price})