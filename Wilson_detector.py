#!/bin/env python

# Wilson - a ball that is dropped on the table if microphone is mounted near table.
# The Ball generates specific sound between 100 - 500 Hz
# I just wrote simple function to "catch" desired frequency at some threshold
# Main advantage that is not a "CPU eater" for Raspberry Pi

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

# pyaudio constants
FORMAT = pyaudio.paInt16  # We use 16 bit format per sample
CHANNELS = 2
RATE = 44100
CHUNK = 4096  # 8192 bytes of data read from a buffer


i = 0
# f, ax = plt.subplots(2)

class Plots():

    def __init__(self):
        # Arrange plot environment for data
        x = np.arange(10000)
        y = np.random.randn(10000)
        _, ax = plt.subplots(2)
        # Plot 0 is for raw audio data
        li, = ax[0].plot(x, y)
        ax[0].set_xlim(0, 4096)
        ax[0].set_ylim(-50000, 50000)
        ax[0].set_title("Raw microphone signal")
        self.raw_plot_content = li
        # Plot 1 is for FFT of the audio
        li2, = ax[1].plot(x, y)
        ax[1].set_xlim(0, 15000)
        ax[1].set_ylim(0, 15000000)
        ax[1].set_title("Fast Fourier Transform")
        self.fft_plot_content = li2

        # Show the plot, but without blocking updates
        plt.pause(0.01)
        plt.tight_layout()


audio = pyaudio.PyAudio()

#start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)

plots_container = Plots()


#frames_per_buffer=CHUNK)

def read_chunk():
    in_data = stream.read(CHUNK)
    audio_data = np.fromstring(in_data, np.int16)
    return audio_data


def process_data(plots, data):

    global i
    fft1 = fft(data)
    freqz = np.fft.fftfreq(len(fft1), 1 / RATE)
    abs_fft = np.abs(fft1)
    # change values (abs_fft[5:50]) in frequency band freqz[5:50] if you changed ball or something else
    # print (abs_fft[5:50],freqz[5:50]
    high_values = [x for x in abs_fft[5:50] if x >= 3000000]
    result = len(high_values)
    # wynik = len([*filter(lambda x: x >= 3000000, abs_fft[5:50])])

    # change this value in if statement if you want bigger threshold
    if result > 15:

        print("'Wilson Trainer Tenis Ball' Detected!","Times:", i)
        i += 1

    #print (wynik)
    plots.raw_plot_content.set_xdata(np.arange(len(data)))
    plots.raw_plot_content.set_ydata(data)
    plots.fft_plot_content.set_xdata(np.arange(len(freqz))*10.)
    plots.fft_plot_content.set_ydata(abs_fft)

    # Show the updated plot, but without blocking
    plt.pause(0.01)


def shutdown():
    stream.stop_stream()
    stream.close()
    audio.terminate()
    

# Open the connection and start streaming the data
stream.start_stream()

print("| Press Ctrl+C to Break Recording |")


is_running = True
# Main Loop so program doesn't end while the stream is opened
while is_running:
    try:
        data = read_chunk()
        process_data(data)
    except KeyboardInterrupt:
        shutdown()
        is_running = False
    except :
        pass