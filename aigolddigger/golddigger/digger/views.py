from django.shortcuts import render, redirect
import ccxt
import pandas as pd
from django.http import JsonResponse
import requests
# Create your views here.
def home(request):
   

    def get_data():
        return "Merhaba, Django dünyası!"

    # Fonksiyonun çıktısını context olarak tanımlayın
    context = {
        'data': get_data(),
    }

    return render(request, 'home.html', context)

def bitcoin_chart_view(request):
    api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    parameters = {
        'vs_currency': 'usd',
        'days': '7',  # Son 7 günün verisini al
        'interval': 'daily',
    }

    try:
        response = requests.get(api_url, params=parameters)
        response.raise_for_status()

        data = response.json()
        prices = data['prices']

        # Veriyi şablona iletmek için gerekli formatı oluştur
        bitcoin_price_data = {
            'labels': [entry[0] for entry in prices],
            'prices': [entry[1] for entry in prices],
        }

        context = {'bitcoin_price_data': bitcoin_price_data}
        return render(request, 'bitcoin_price.html', context)

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching Bitcoin price: {e}"
        context = {'error_message': error_message}
        return render(request, 'error.html', context)


def get_binance_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def bitcoin_chart(request):
    df = get_binance_data()
    data = {
        'timestamp': df['timestamp'].astype(str).tolist(),
        'close': df['close'].tolist(),
    }
    return JsonResponse(data)
