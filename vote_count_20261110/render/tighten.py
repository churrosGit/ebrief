# 문장 끝 긴 쉼(0.9초 이상)을 0.4초로 줄임
import numpy as np, wave, sys
KEEP = 0.4
for i in range(4):
    w = wave.open(f'p{i}.wav'); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).copy(); w.close()
    hop = sr // 100; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n*hop].astype(np.float32)/32768).reshape(n, hop).__pow__(2).mean(1)) + 1e-6); low = db < -45
    segs = []; k = 0
    while k < n:
        if low[k]:
            j = k
            while j < n and low[j]: j += 1
            if (j - k) / 100 >= 0.9: segs.append((k * hop, j * hop))
            k = j
        else: k += 1
    out = []; pos = 0
    for a, b in segs:
        cut = (b - a) - int(KEEP * sr); m = a + (b - a) // 2
        out.append(x[pos:m - cut // 2]); pos = m - cut // 2 + cut
    out.append(x[pos:]); y = np.concatenate(out)
    o = wave.open(f'p{i}t.wav', 'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
    print(i, round(len(x)/sr, 2), '->', round(len(y)/sr, 2), [round((b-a)/sr, 2) for a, b in segs])
