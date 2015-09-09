import numpy as np
import matplotlib.pyplot as plt
import math as m

def MovingAverage(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def GenerateSignal(amplitude, samplingFreq, signFreq):
    ts = np.linspace(0, 1, samplingFreq)
    signal = amplitude * np.sin(2 * m.pi * signFreq * ts)
    return ts, signal

def ReadCSVData(fileName):
    data = np.genfromtxt(fileName, delimiter=',')
    return data

def Spectrogram(ts, signal, samplingFreq):
    signalLen = len(signal)
    ticks = np.arange(signalLen)
    period = float(signalLen) / samplingFreq
    frq = ticks / period
    frq = frq[range(signalLen / 2)]
    fftResult = np.fft.fft(signal)
    fftResult = fftResult[range(signalLen / 2)] / max(fftResult[range(signalLen / 2)])

    plt.subplot(3, 1, 1)
    plt.plot(ts, signal, 'r')
    plt.xlabel('Time (days)')
    plt.ylabel('Amplitude')
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(frq, abs(fftResult), 'k')
    plt.xlabel('Freq (Hz)')
    plt.grid()

    plt.subplot(3, 1, 3)
    nSlidingWindowFFT = 100
    [Pxx, freqs, bins, im] = plt.specgram(signal, NFFT=nSlidingWindowFFT, Fs=samplingFreq, noverlap=nSlidingWindowFFT - 1)
    plt.show()

def ExampleSyntheticData():
    samplingFreq = 1000
    signFreq = 100
    amplitude = 10
    ts, signal1 = GenerateSignal(amplitude, samplingFreq, signFreq)

    signFreq = 200
    amplitude = 5
    ts, signal2 = GenerateSignal(amplitude, samplingFreq, signFreq)

    signFreq = 300
    amplitude = 2.5
    ts, signal3 = GenerateSignal(amplitude, samplingFreq, signFreq)

    signal4 = signal1 + signal2 + signal3
    Spectrogram(ts, signal4, 1)

def ExampleRealSignal():
    data = ReadCSVData('table.csv')
    data = data[1:]
    lenData = data.shape[0]
    open = data[:,[0]].reshape(lenData)
    high = data[:,[1]].reshape(lenData)
    low = data[:,[2]].reshape(lenData)
    close = data[:,[3]].reshape(lenData)
    volume = data[:,[4]].reshape(lenData)

    ma = MovingAverage(close, n=60)
    ts = np.linspace(0, len(ma), len(ma))
    Spectrogram(ts, ma, 1)

if __name__ == '__main__':
    ExampleSyntheticData()
    ExampleRealSignal()
