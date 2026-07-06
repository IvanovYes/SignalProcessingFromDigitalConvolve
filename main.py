import math
import numpy as np
import matplotlib.pyplot as plt

kernels = {}

def Hilbert(t, dt, N = None):
    if t == 0:
        return 0
    else:
        return dt / (np.pi * t)

def Haar(t=None, dt=None, N=1):
    return 1/N

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
    return h

def GenerateFormatSignalToConvolve(signal, kernel):
    length = len(signal) + 2 * ((len(kernel)+1)/2 - 1)
    print(len(signal))
    print(length)
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
    # Свертка
    transform_output = np.convolve(signal, kernel, mode='valid')
    return transform_output

if __name__ == "__main__":
    # Параметры
    N = 3
    dt = 4/100000
    #t = np.linspace(1, 3, int(2*1/dt))
    t = np.arange(0, 3*(2*np.pi/N)+dt, dt)
    noise = np.random.normal(0, 1 / 10, len(t))  # шум нормального распределения
    def f1(t): return np.sin(N * t)
    signal = f1(t)+noise
    kernelToConvolve = GenerateFormatKernelToConvolve(len(signal), 1/dt, type="HR", lengthKernel=9)
    signalToConvolve = GenerateFormatSignalToConvolve(signal, kernelToConvolve)
    analytic_signal_conv = TransformFromConvolve(signalToConvolve, kernelToConvolve)

    plt.figure(figsize=(15, 20))
    plt.plot(t, signal, 'b-', linewidth=2, label='Исходный сигнал')
    plt.plot(t, analytic_signal_conv, 'r--', linewidth=2, label='Гильберт (свертка)')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    plt.show()