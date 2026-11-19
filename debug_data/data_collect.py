import sounddevice as sd
import numpy as np
import time

duration = 5
sample_rate = 16_000

with sd.InputStream(
    device="adau7002",
    samplerate=sample_rate,
    channels=1,
    dtype="float32") as stream:

    time.sleep(1)

    chunk1, overflowed = stream.read(int(duration * sample_rate))

    chunk2, overflowed = stream.read(int(duration * sample_rate))

    chunk3, overflowed = stream.read(int(duration * sample_rate))


np.save("Chunk1.npy", chunk1)
np.save("Chunk2.npy", chunk2)
np.save("Chunk3.npy", chunk3)
