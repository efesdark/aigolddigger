import json
import asyncio
import ccxt
import time
import ccxt
import json
from channels.generic.websocket import AsyncWebsocketConsumer





"""
class CandlestickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Burada gelen veriyi işleyebilirsiniz (isteğe bağlı)
         print(f"Received data: {text_data}")
         print(f"veri alındı")

    async def send_candlestick_data(self, event):
        # Gelen veriyi WebSocket üzerinden gönder
        data = event['data']
        await self.send(text_data=json.dumps(data))
        """
"""
class CandlestickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_candlestick_data(self, event):
        # Gelen veriyi doğrudan müşteriye gönder
        await self.send(text_data=json.dumps(event['data']))
"""

class CandlestickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Grup ismi, kullanıcı kimliğinden alınabilir veya başka bir benzersiz değer olabilir
        group_name = "candlestick_group"
        await self.channel_layer.group_add(group_name, self.channel_name)
        binance = ccxt.binance()
        symbol = 'BTC/USDT'
        timeframe = '1m'
        while True:
            try:
                candles = binance.fetch_ohlcv(symbol, timeframe, limit=1)
                candle = candles[0]
                timestamp, open_, high, low, close, _ = candle
                data = {
                    'timestamp': timestamp,
                    'open': open_,
                    'high': high,
                    'low': low,
                    'close': close,
                }
                await self.send(text_data=json.dumps(data))
                await asyncio.sleep(5)  # 5 saniyede bir güncelle
            except Exception as e:
                print(f"Hata: {e}")
    async def disconnect(self, close_code):
        group_name = "candlestick_group"
        await self.channel_layer.group_discard(group_name, self.channel_name)        
