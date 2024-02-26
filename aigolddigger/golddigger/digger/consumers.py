import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import ccxt
import time
import ccxt
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CandlestickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

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
                await asyncio.sleep(1)  # 60 saniyede bir güncelle
            except Exception as e:
                print(f"Hata: {e}")        
