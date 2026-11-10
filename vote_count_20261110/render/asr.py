import sys, wave, json, numpy as np, sherpa_onnx
d = 'sherpa-onnx-zipformer-korean-2024-06-24/'
r = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder-epoch-99-avg-1.int8.onnx', decoder=d+'decoder-epoch-99-avg-1.int8.onnx', joiner=d+'joiner-epoch-99-avg-1.int8.onnx', tokens=d+'tokens.txt', num_threads=4, decoding_method='greedy_search')
w = wave.open('narr16.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
b = [0.0] + [float(v) for v in sys.argv[1:]] + [len(x) / 16000]
out = []
for a, e in zip(b[:-1], b[1:]):
    s = r.create_stream(); s.accept_waveform(16000, x[int(a*16000):int(e*16000)]); r.decode_stream(s)
    res = s.result; print(round(a, 1), res.text)
    out += [(t, round(a + ts, 2)) for t, ts in zip(res.tokens, res.timestamps)]
json.dump(out, open('tokens.json', 'w'), ensure_ascii=False)
