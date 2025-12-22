import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt 

path_time_series_csv = 'sensors_mgb.csv'

df = pd.read_csv(path_time_series_csv)

time = df['time']      
signal = df['s1']  
dt = np.mean(np.diff(time))      
fs = 1 / dt                      

signal = signal - np.mean(signal)
# 4. اعمال FFT
N = len(signal)                 
y_fft = np.fft.fft(signal)       
y_fft = np.abs(y_fft[:N // 2])    
y_fft = y_fft / N                

# 5. محور فرکانس
freq = np.fft.fftfreq(N, d=dt)[:N // 2]

# 6. رسم نمودار
plt.figure(figsize=(10, 5))
plt.plot(freq, y_fft)
plt.title('FFT of Vibration Signal (Healthy Group)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()


