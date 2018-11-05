try:
    print("Loading libraries please stand by...")
    import numpy as np
    import matplotlib.pyplot as plt
    print("Done.")
except KeyboardInterrupt:
    print("You dont have nescessary libraries")

class DetectorState():
    
    def __init__(self):
        self.__detections = 0
    
    def register_detection(self):
        self.__detections += 1
    
    @property
    def detections(self):
        return self.__detections

    def __str__(self):
        return "Ball has been detected {} times".format(self.__detections)


class PlotsState():

    def __init__(self):
        f, ax = plt.subplots(2)
        # Arrange plot environment for data
        x = np.arange(10000)
        y = np.random.randn(10000)
        # Plot 0 is for raw audio data
        self.__li, = ax[0].plot(x, y)
        ax[0].set_xlim(0, 4096)
        ax[0].set_ylim(-50000, 50000)
        ax[0].set_title("Raw microphone signal")
        # Plot 1 is for FFT of the audio
        self.__li2, = ax[1].plot(x, y)
        ax[1].set_xlim(0, 15000)
        ax[1].set_ylim(0, 15000000)
        ax[1].set_title("Fast Fourier Transform")
        # Show the plot, but without blocking updates
        plt.pause(0.01)
        plt.tight_layout()

    @property
    def raw_data(self):
        return self.__li

    def set_raw_data(self, data):
        self.__li.set_xdata(np.arange(len(data)))
        self.__li.set_ydata(data)

    @property
    def fft_data(self):
        return self.__li2

    def set_fft_data(self, freqz, abs_fft):
        self.__li2.set_xdata(np.arange(len(freqz))*10.)
        self.__li2.set_ydata(abs_fft)
