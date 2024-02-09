import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import ccxt

class CandlestickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        binance = ccxt.binance()
        symbol = 'BTC/USDT'
        timeframe = '1m'

        while True:
            try:
                candles = await binance.fetch_ohlcv(symbol, timeframe, limit=1)
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
                await asyncio.sleep(60)  # 60 saniyede bir güncelle
            except Exception as e:
                print(f"Hata: {e}")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name ='digger'

        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message= text_data_json['message']
        event = {
            'type': 'send_mesage',
            'message': message
        }

        await self.channel_layer.group_send(self.group_name,event)
    
    async def send_message(self,event):
        message = event ['message']

        await self.send(text_data=json.dumps({'message':message}))

    