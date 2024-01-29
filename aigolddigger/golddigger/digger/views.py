from django.shortcuts import render
from django.http import JsonResponse
import ccxt

def home(request):
    return render(request, 'home.html')

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