import math
import numpy as np
import matplotlib.pyplot as plt

kernels = {}

def MovingAverage(t=None, dt=None, N=1):
    return 1/N

def Hilbert(t, dt, N = None):
    if t == 0:
        return 0
    else:
        return dt / (np.pi * t)

def Haar(t, dt, N = None):
    m = 0
    s=t*2**m + 0.5

    if s < 0:
        return 0
    elif 0 <= s < 0.5:
        return dt*2**(m/2)
    elif 0.5 <= s < 1:
        return -dt*2**(m/2)
    elif 1 <= s:
        return 0

kernels["MA"] = MovingAverage
kernels["HB"] = Hilbert
kernels["HR"] = Haar

def GenerateFormatKernelToConvolve(lengthSignal, fs, tstart=0, type="HB", lengthKernel=None, func=None):
    kernels["custom"] = func
    func = kernels[type]
    if lengthKernel == None:
        lengthKernel = 2 * lengthSignal - 1
    t = np.zeros(lengthKernel)
    h = np.zeros(lengthKernel)
    for k in range(lengthKernel):
        t[k] = (k + tstart * fs - ((lengthKernel+1)/2 - 2)) * 1/fs
        h[k] = func(t[k], 1/fs, lengthKernel)
    print(t)
    plt.figure(figsize=(15, 20))
    plt.plot(t, h, 'b-', linewidth=2)
    plt.grid(True)
    plt.show()
    return h

def GenerateFormatSignalToConvolve(signal, kernel):
    length = len(signal) + 2 * ((len(kernel)+1)/2 - 1)
    x = np.zeros(int(length))
    for k in range(int(length)):
        if k <= ((len(kernel)+1)/2 - 2):
            x[k] = 0
        elif k > ((len(kernel)+1)/2 - 2) and k <= (len(signal)-1 + (len(kernel)+1)/2 - 2):
            x[k] = signal[int(k - ((len(kernel)+1)/2 - 2))]
        else:
            x[k] = 0
    return x

def TransformFromConvolve(signal, kernel):
    # Свертка во временной области
    convolveResult = np.convolve(signal, kernel, mode='valid')
    return convolveResult

if __name__ == "__main__":
    # Параметры
    N = 3
    dt = 1/1000
    t = np.arange(0, 4, dt)
    noise = np.random.normal(0, 1 / 10, len(t))  # шум нормального распределения
    def f1(t): return np.sin(N * t)
    def f2(t):
        y = np.zeros(len(t))
        for k in range(len(t)):
            if t[k] >= 1 and t[k] < 2:
                y[k] = 1
            elif t[k] >= 2 and t[k] < 3:
                y[k] = -1
            else:
                y[k] = 0
        return y

    signal = f2(t)

    kernelToConvolve = GenerateFormatKernelToConvolve(len(signal), 1/dt, type="HR")
    signalToConvolve = GenerateFormatSignalToConvolve(signal, kernelToConvolve)
    signal_conv = TransformFromConvolve(signalToConvolve, kernelToConvolve)
    plt.figure(figsize=(15, 20))
    plt.plot(t, signal, 'b-', linewidth=2, label='Исходный сигнал')
    plt.step(t, signal_conv, 'r', linewidth=2, label='Результат свертки')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    plt.show()