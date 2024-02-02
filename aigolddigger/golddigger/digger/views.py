from django.shortcuts import render
from django.http import JsonResponse
import ccxt
import requests
def home(request):
    return render(request, 'home.html')

def chart(request):
    return render(request, 'chart.html') 
from django.shortcuts import render
import requests

def charts(request):
  # Binance API'dan canlı bitcoin fiyatlarını çekmek için bir istek yapın
    binance_api_url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'
    response = requests.get(binance_api_url)
    data = response.json()

    # Veriyi işleyerek grafikte kullanılabilir formata dönüştürün
    current_price = float(data['lastPrice'])
    change_percentage = float(data['priceChangePercent'])
    high_price = float(data['highPrice'])
    low_price = float(data['lowPrice'])
    volume = float(data['volume'])
    volume_usdt = float(data['quoteVolume'])

    # Template'e gönderilecek context oluşturun
    context = {
        'current_price': current_price,
        'change_percentage': change_percentage,
        'high_price': high_price,
        'low_price': low_price,
        'volume': volume,
        'volume_usdt': volume_usdt,
    }

    # HTML template'i ile birlikte render edin
    return render(request, 'chart.html', context)



def get_bitcoin_price(request):
    # Binance API'ye istek atmak için ccxt kütüphanesini kullanalım
    binance = ccxt.binance()

    try:
        # Binance'ten anlık fiyatı al
        ticker = binance.fetch_ticker('BTC/USDT')
        bitcoin_price = ticker['last']

        # JSON formatında yanıt döndür
        return JsonResponse({'price': bitcoin_price})

    except ccxt.NetworkError as e:
        return JsonResponse({'error': f'Network hatası: {e}'})

    except ccxt.ExchangeError as e:
        return JsonResponse({'error': f'Exchange hatası: {e}'})
        