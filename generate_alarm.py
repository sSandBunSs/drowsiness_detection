"""
Generate alarm sound file (alarm.wav) menggunakan numpy + scipy
Jalankan sekali untuk membuat file alarm.
"""
import numpy as np
import wave
import struct
import os

def generate_alarm(filepath="sounds/alarm.wav",
                   frequency=1000, duration=0.5,
                   sample_rate=44100, volume=0.7,
                   repeats=3):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    samples = []
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = (np.sin(2 * np.pi * frequency * t) * volume * 32767).astype(np.int16)
    silence = np.zeros(int(sample_rate * 0.1), dtype=np.int16)

    for _ in range(repeats):
        samples.extend(tone.tolist())
        samples.extend(silence.tolist())

    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        data = struct.pack(f"<{len(samples)}h", *samples)
        wf.writeframes(data)
    print(f"Alarm sound generated: {filepath}")

if __name__ == "__main__":
    generate_alarm()
