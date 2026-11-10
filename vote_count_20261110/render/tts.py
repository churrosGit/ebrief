# python3 tts.py <rate e.g. +15%> <out.mp3> <text file>
import sys, os, asyncio, certifi
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
rate, out, tf = sys.argv[1:4]
text = open(tf).read()
async def main():
    c = edge_tts.Communicate(text, 'ko-KR-InJoonNeural', rate=rate, proxy=os.environ.get('HTTPS_PROXY'))
    await c.save(out)
asyncio.run(main())
