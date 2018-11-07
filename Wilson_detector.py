#!/usr/bin/env python

"""
Wilson - a ball that is dropped on the table if microphone is mounted near table.
The Ball generates specific sound between 100 - 500 Hz
I just wrote simple function to "catch" desired frequency at some threshold
Main advantage that is not a "CPU eater" for Raspberry Pi
"""
try:
    print("Loading libraries please stand by...")
    import pyaudio
    import numpy as np

    # for raspberry
    # uncomement below if you use Raspberry Pi

    # import matplotlib
    # matplotlib.use("TkAgg")

    # keep calm and install - sudo apt-get install python3-tk ;)

    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    from scipy import signal
    import wave
    from scipy.fftpack import fft
    from state_keepers import PlotsState, DetectorState
    print("Done.")
except KeyboardInterrupt:
    print("You dont have nescessary libraries")

# pyaudio constants
FORMAT = pyaudio.paInt16  # We use 16 bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = 4096  # 8192 bytes of data read from a buffer


def read_chunk(stream):

    # There is some kind of overflow error in Raspberry uncomment if program does't work
    # in_data = stream.read(CHUNK, exeption_on_overflow=False)
    
    in_data = stream.read(CHUNK)
    audio_data = np.fromstring(in_data, np.int16)
    return audio_data


def process_data(detector_state, plots_state, data):
    fft1 = fft(data)
    freqz = np.fft.fftfreq(len(fft1), 1 / RATE)
    abs_fft = np.abs(fft1)
    # change values (abs_fft[5:50]) in frequency band freqz[5:50] if you changed ball or something else
    # print (abs_fft[5:50],freqz[5:50]
    result = len([x for x in abs_fft[5:50] if x >= 3000000])
    # change this value in if statement if you want bigger threshold
    if result > 15:
        detector_state.register_detection()
        print("'Wilson Trainer Tenis Ball' Detected!","Times:", detector_state.detections)
    plots_state.set_raw_data(data)
    plots_state.set_fft_data(freqz, abs_fft)
    # Show the updated plot, but without blocking
    plt.pause(0.01)


def main():
    audio = pyaudio.PyAudio()
    #start Recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True)

    #frames_per_buffer=CHUNK)

    detector_state = DetectorState()
    plots_state = PlotsState()
    # Open the connection and start streaming the data
    stream.start_stream()

    print("| Press Ctrl+C to Break Recording |")

    loop = True
    # Main Loop so program doesn't end while the stream is opened
    while loop:
        try:
            data = read_chunk(stream)
            process_data(detector_state, plots_state, data)
        except KeyboardInterrupt:
            loop = False
        # except Exception as e:
        #     print(e)
        #     pass

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == '__main__':
    main()