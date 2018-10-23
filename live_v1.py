try:
    print("Loading libraries please stand by...")
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    from scipy import signal
    from scipy.io import wavfile
    import wave
    from scipy.fftpack import fft
    print("Done.")
except KeyboardInterrupt:
    print("You dont have nescessary libraries")
samplerate, file = wavfile.read('knock.wav')

i = 0
f, ax = plt.subplots(4)

# Arrange plot environment for data
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0, 8192)
ax[0].set_ylim(-50000, 50000)
ax[0].set_title("Sygnał z mikrofonu")
# Plot 1 is for FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0, 15000)
ax[1].set_ylim(0, 20000000)
ax[1].set_title("Fast Fourier Transform")
# Plot 2 is for correlation
li3, = ax[2].plot(x, y)
ax[2].set_xlim(0, 30000)
ax[2].set_ylim(0, 10000000000)
ax[2].set_title("correlation #comming soon")

# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

# pyaudio constants
FORMAT = pyaudio.paInt16  # We use 16 bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = 16384  # 8192 bytes of data read from a buffer

audio = pyaudio.PyAudio()

#start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)

#frames_per_buffer=CHUNK)

global loop
global in_data
global audio_data


loop = True

def const():
    const.s = np.array([])


def read_chunk():
    in_data = stream.read(CHUNK)
    audio_data = np.fromstring(in_data, np.int16)
    return audio_data


def plot_data():

    fft1 = fft(data)
    freqz = np.fft.fftfreq(len(fft1), 1 / RATE)

    li.set_xdata(np.arange(len(data)))
    li.set_ydata(data)
    li2.set_xdata(np.arange(len(freqz))*10.)
    li2.set_ydata(np.abs(fft1))


    #return in_data

    # Show the updated plot, but without blocking
    plt.pause(0.01)
    if loop:
        return True
    else:
        return False

def test():

    data_sample = np.append(const.s, data)
    g = np.pad(data_sample, ((len(file)-len(data_sample)), 0), 'constant', constant_values=(0, 0))
    xcorr = np.corrcoef(file,g)
    result = []
    result.append(xcorr[0][1])
    results = list(map(float, result))
    # correlation coefficient
    print(results)


const()

# Open the connection and start streaming the data
stream.start_stream()

print("| Press Ctrl+C to Break Recording |")

# Main Loop so program doesn't end while the stream is opened
while loop:
    try:
        #process_data()
        data = read_chunk()
        plot_data()
        test()
    except KeyboardInterrupt:
        loop = False
    except :
        pass

stream.stop_stream()
stream.close()
audio.terminate()
