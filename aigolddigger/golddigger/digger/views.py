from django.shortcuts import render
from django.http import JsonResponse
import ccxt
import pandas as pd
import requests
import json
from datetime import datetime
binance_limit = 300

binance = ccxt.binance()
binance_timeframe= '5m'
binance_symbol = 'BTC/USDT'

def ajax(request):
    return render(request, 'test/ajax.html')

def test_message(request):
#def test_message(request, binance_symbol='BTC/USDT'):
  #Bu değişikliklerle binance_symbol artık send_symbol fonksiyonu içinde tanımlanacak ve test_message fonksiyonuna gönderilecek. 
  #Eğer send_symbol içinde değer belirtilmezse, varsayılan olarak 'BTC/USDT' kullanılacaktır.
  if request.method == "POST":
    global binance_timeframe
    binance_timeframe = request.POST["binance_timeframe"]
    
    
   
    binance_data = binance.fetch_ohlcv(binance_symbol, binance_timeframe, limit=binance_limit)

    formatted_data = [{
            'time': entry[0] / 1000,
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
            'timeframe': binance_timeframe,

        } for entry in binance_data]

    return JsonResponse({'formatted_data': formatted_data})
  
def searchCoin(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', None)

        # ccxt borsa nesnesini oluştur
        binance = ccxt.binance()
        # Binance'da bulunan tüm sembollerin listesini al
        symbols = binance.fetch_markets()

        # Sadece sembol isimlerini içeren bir liste oluştur
        symbol_names = [symbol['symbol'] for symbol in symbols]

        # search_query ile başlayan sembolleri filtrele
        filtered_symbols = [symbol for symbol in symbol_names if symbol.startswith(search_query.upper())]

        # Sonuçları göster

        # Coin bilgilerini JSON formatında döndür
        data = {
            'symbol': filtered_symbols,
            
        }

        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def send_symbol(request):
    if request.method == 'POST':
    
    
        symbol = request.POST.get('symbol', 'BTC/USDT')
          #Bu değişikliklerle binance_symbol artık send_symbol fonksiyonu içinde tanımlanacak ve test_message fonksiyonuna gönderilecek. 
          #Eğer send_symbol içinde değer belirtilmezse, varsayılan olarak 'BTC/USDT' kullanılacaktır.
        
        # Symbol değeri ile istediğiniz işlemleri yapın
        # Örneğin, bu değeri konsolda gösterelim
        global binance_symbol
        
        binance_symbol = symbol
        binance = ccxt.binance()
        binance_data = binance.fetch_ohlcv(binance_symbol, binance_timeframe, limit=binance_limit)
         # Piyasa bilgilerini çek
       

        formatted_data = [{
            'time': entry[0] / 1000,
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
            'timeframe': binance_timeframe,
        } for entry in binance_data]

    return JsonResponse({'formatted_data': formatted_data})



def ajax_message(request):
  if request.method == "POST":
    message = request.POST["message"]
    return JsonResponse({"message": message})
  
def home(request):
 #esential
    
    global binance_symbol
    global binance_timeframe 
    binance_limit = 300
    
    binance = ccxt.binance()
    # Binance'da bulunan tüm sembollerin listesini al
    symbols = binance.fetch_markets()

    # Piyasa bilgilerini çek
    ticker = binance.fetch_ticker(binance_symbol)
     # İlgili bilgileri al
    try:
        current_price = ticker['last']
    except (TypeError, ValueError):
        current_price = 0.0
#burası bazen son datayı alırken patlıyor galiba coin coin işlem çiftlerinde
    try:
        change_percentage = float(ticker['percentage'])
    except (TypeError, ValueError):
        change_percentage = 0.0
    # 24 saatlik en yüksek ve en düşük fiyatları al
    high_price = float(ticker['high'])
    low_price = float(ticker['low'])

    # Hacim bilgilerini al
    volume = ticker['baseVolume']
    volume_usdt = ticker['quoteVolume']
    # Binance API'den son işlemleri çekmek için bir istek yapın (trade parametresi)
    link_symbol= binance_symbol.replace('/', '') 
    binance_trades_url = f'https://api.binance.com/api/v3/trades?symbol={link_symbol}'
    response_trades = requests.get(binance_trades_url)
    trades = response_trades.json()    
   
    binance_data = binance.fetch_ohlcv(binance_symbol, binance_timeframe, limit=binance_limit)
 
   


    formatted_data = [{
        #'time': datetime.utcfromtimestamp(entry[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # Unix zaman damgasını çevir
        'time': entry[0]/1000, 
        'open': float(entry[1]),
        'high': float(entry[2]),
        'low': float(entry[3]),
        'close': float(entry[4]),
        'timesframe': binance_timeframe,
        
         } for entry in binance_data]
    
    

    # Template'e gönderilecek context oluşturun
    context = {
        'current_coin': binance_symbol,
        'current_price': current_price,
        'change_percentage': change_percentage,
        'high_price': high_price,
        'low_price': low_price,
        'volume': volume,
        'volume_usdt': volume_usdt, 
        'trades': trades,

        'formatted_data': formatted_data,
    }

    return render(request, 'home.html', context)

    
def test(request):
    binance_symbol = 'BTC/USDT'
    binance_timeframe = '1h'
    binance_limit = 300

    binance = ccxt.binance()
    binance_data = binance.fetch_ohlcv(binance_symbol, binance_timeframe, limit=binance_limit)
 
    # Verileri uygun formata dönüştür
    
    formatted_data = [{
        #'time': datetime.utcfromtimestamp(entry[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # Unix zaman damgasını çevir
        'time': entry[0]/1000, 
        'open': float(entry[1]),
        'high': float(entry[2]),
        'low': float(entry[3]),
        'close': float(entry[4]),
        'timesframe': binance_timeframe,
         } for entry in binance_data]
  
    # JSON formatına dönüştür
    #formatted_data_json = json.dumps(formatted_data)

    #return render(request, 'test/test.html', {'formatted_data_json': formatted_data_json})
    return render(request, 'test/test.html', {'formatted_data': formatted_data})

def update_chart(request):
    if request.method == 'GET':
        binance_symbol = 'BTC/USDT'
        binance_timeframe = request.GET.get('binance_timeframe')  # Default olarak '5m' kullanabilirsiniz
        binance_limit = 300

        binance = ccxt.binance()
        binance_data = binance.fetch_ohlcv(binance_symbol, binance_timeframe, limit=binance_limit)

        formatted_data = [{
            'time': entry[0] / 1000,
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
            'timesframe': binance_timeframe,
        } for entry in binance_data]

        return JsonResponse({'formatted_data': formatted_data})


def your_view_name(request):
    if request.method == 'POST' and request.is_ajax():
        # AJAX isteği üzerinden gelen veriyi al
        example_value = request.POST.get('example_key', None)
        
        # İşlemleri gerçekleştir
        result = f"{example_value} başarılı"

        # JSON formatında bir yanıt gönder
        return JsonResponse({'response_key': result})

    return JsonResponse({'response_key': 'Hatalı istek'})

def candles(request):
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
    
def python_test_ccxt(request):
    binance= ccxt.binance()
    market_binance=binance.load_markets()
    
    

        