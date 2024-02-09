from django.shortcuts import render
from django.http import JsonResponse
import ccxt
import requests
def home(request):
    return render(request, 'home.html')

def test(request):
    return render(request, 'test/test.html')
def candles(request):
    binance_api_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': '1m',
        'limit': 3000,
    }
    response = requests.get(binance_api_url, params=params)
    binance_data = response.json()

    # Verileri uygun formata dönüştür
    formatted_data = [{
    'time': entry[0],
    'open': float(entry[1]),
    'high': float(entry[2]),
    'low': float(entry[3]),
    'close': float(entry[4]),
    } for entry in binance_data]
    return render(request, 'candles.html', {'formatted_data': formatted_data})




def chart(request):
    return render(request, 'chart.html') 
from django.shortcuts import render
import requests



def charts(request):
    # Binance API'den canlı bitcoin fiyatlarını çekmek için bir istek yapın
    binance_api_url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'
    response = requests.get(binance_api_url)
    data = response.json()

    # Binance API'den son işlemleri çekmek için bir istek yapın (trade parametresi)
    binance_trades_url = 'https://api.binance.com/api/v3/trades?symbol=BTCUSDT'
    response_trades = requests.get(binance_trades_url)
    trades = response_trades.json()

    # Binance API'den sembol bilgisini çekmek için bir istek yapın
    exchange_info_url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(exchange_info_url)
    exchange_info = response.json()

    # İlgilenilen sembolü seçin (örneğin, BTCUSDT)
    symbol_info = next(item for item in exchange_info['symbols'] if item['symbol'] == 'BTCUSDT')

    # Sembole ait bilgileri çekin
    current_coin = symbol_info['baseAsset']

    # Veriyi işleyerek grafikte kullanılabilir formata dönüştürün
    current_price = float(data['lastPrice'])
    change_percentage = float(data['priceChangePercent'])
    high_price = float(data['highPrice'])
    low_price = float(data['lowPrice'])
    volume = float(data['volume'])
    volume_usdt = float(data['quoteVolume'])
 #test
    binance_api_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': '1m',
        'limit': 300,
    }
    response = requests.get(binance_api_url, params=params)
    binance_data = response.json()

    # Verileri uygun formata dönüştür
    formatted_data = [{
    'time': entry[0],
    'open': float(entry[1]),
    'high': float(entry[2]),
    'low': float(entry[3]),
    'close': float(entry[4]),
    } for entry in binance_data]
    #return render(request, 'chart.html', context, {'formatted_data': formatted_data})
    
    

    # Template'e gönderilecek context oluşturun
    context = {
        'current_coin': current_coin,
        'current_price': current_price,
        'change_percentage': change_percentage,
        'high_price': high_price,
        'low_price': low_price,
        'volume': volume,
        'volume_usdt': volume_usdt, 
        'trades': trades,
        'formatted_data': formatted_data,
    }

    return render(request, 'chart.html', context)
   

    # HTML template'i ile birlikte render edin
   



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
        