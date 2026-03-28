import asyncio, websockets, urllib.request

async def test():
    async with websockets.connect('ws://localhost:8000/api/v1/logs/stream') as ws:
        print("Connected:", await ws.recv())
        
        # Trigger an access log
        try:
            urllib.request.urlopen("http://localhost:8000/api/v1/scrape/brands")
        except:
            pass
            
        print("Log 1:", await ws.recv())

asyncio.run(test())
