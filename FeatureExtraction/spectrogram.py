import numpy as np
import matplotlib.pyplot as plt
import math as m


def GenerateSignal(amplitude, samplingFreq, signFreq):
    ts = np.linspace(0, 1, samplingFreq);
    signal = amplitude * np.sin(2 * m.pi * signFreq * ts);
    return ts, signal


def Spectrogram(ts, signal, samplingFreq):
    # FFT of this
    Fs = samplingFreq  # sampling rate, Fs = 500MHz = 1/2ns
    n = len(signal)  # length of the signal
    k = np.arange(n)
    T = n / Fs
    frq = k / T  # two sides frequency range
    frq = frq[range(n / 2)]  # one side frequency range
    Y = np.fft.fft(signal) / n  # fft computing and normalization
    Y = Y[range(n / 2)] / max(Y[range(n / 2)])

    # plotting the data
    plt.subplot(3, 1, 1)
    plt.plot(ts * 1e3, signal, 'r')
    plt.xlabel('Time (micro seconds)')
    plt.ylabel('Amplitude')
    plt.grid()

    # plotting the spectrum
    plt.subplot(3, 1, 2)
    plt.plot(frq[0:600], abs(Y[0:600]), 'k')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')
    plt.grid()

    # plotting the specgram
    plt.subplot(3, 1, 3)
    Pxx, freqs, bins, im = plt.specgram(signal, NFFT=512, Fs=Fs, noverlap=10)
    plt.show()


def Example():
    pi = m.pi
    dt = 40e-9
    t = np.arange(0, 1000e-6, dt)
    fscale = t / max(t)
    y = np.cos(2 * pi * 1e6 * t * fscale) + (np.cos(2 * pi * 2e6 * t * fscale) * np.cos(2 * pi * 2e6 * t * fscale))
    y *= np.hanning(len(y))
    yy = np.concatenate((y, ([0] * 10 * len(y))))

    # FFT of this
    Fs = 1 / dt  # sampling rate, Fs = 500MHz = 1/2ns
    n = len(yy)  # length of the signal
    k = np.arange(n)
    T = n / Fs
    frq = k / T  # two sides frequency range
    frq = frq[range(n / 2)]  # one side frequency range
    Y = np.fft.fft(yy) / n  # fft computing and normalization
    Y = Y[range(n / 2)] / max(Y[range(n / 2)])

    # plotting the data
    plt.subplot(3, 1, 1)
    plt.plot(t * 1e3, y, 'r')
    plt.xlabel('Time (micro seconds)')
    plt.ylabel('Amplitude')
    plt.grid()

    # plotting the spectrum
    plt.subplot(3, 1, 2)
    plt.plot(frq[0:600], abs(Y[0:600]), 'k')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')
    plt.grid()

    # plotting the specgram
    plt.subplot(3, 1, 3)
    Pxx, freqs, bins, im = plt.specgram(y, NFFT=512, Fs=Fs, noverlap=10)
    plt.show()


if __name__ == '__main__':
    samplingFreq = 1000
    signFreq = 100
    amplitude = 10
    ts, signal1 = GenerateSignal(amplitude, samplingFreq, signFreq)

    signFreq = 200
    amplitude = 10
    ts, signal2 = GenerateSignal(amplitude, samplingFreq, signFreq)

    signFreq = 500
    amplitude = 5
    ts, signal3 = GenerateSignal(amplitude, samplingFreq, signFreq)

    signalTotal = signal1 + signal2 + signal3

    Spectrogram(ts, signalTotal, samplingFreq)
