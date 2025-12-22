import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# پارامترهای سیستم
# ----------------------------
fs = 10000          # نرخ نمونه‌برداری (Hz) — کافی برای تا 5 kHz
T = 2.0             # مدت زمان سیگنال (ثانیه)
t = np.linspace(0, T, int(fs * T), endpoint=False)

GMF = 792.3         # فرکانس مش‌گیری (Hz)
harmonics = [1, 2, 3, 4]      # هارمونیک‌هایی که دخیل‌اند
amplitudes = [1.0, 0.15, 0.05, 0.02]  # دامنه‌های کاهشی (سالم = هارمونیک‌ها ضعیف‌تر)

# ----------------------------
# ساخت سیگنال لرزش (تمیز و سالم)
# ----------------------------
signal = np.zeros_like(t)
for n, amp in zip(harmonics, amplitudes):
    signal += amp * np.sin(2 * np.pi * n * GMF * t)

# اضافه کردن نویز کم برای واقعی‌تر شدن
np.random.seed(0)
signal += 0.02 * np.random.randn(len(t))

# ----------------------------
# محاسبه FFT
# ----------------------------
N = len(signal)
fft_vals = np.fft.rfft(signal)
fft_freq = np.fft.rfftfreq(N, d=1/fs)

# طیف توان (Power Spectrum)
psd = np.abs(fft_vals) ** 2

# ----------------------------
# رسم نمودار
# ----------------------------
plt.figure(figsize=(12, 5))
plt.plot(fft_freq, psd, color='steelblue')
plt.xlim(0, 3500)  # نمایش تا 3.5 kHz
plt.xlabel('Frequency (Hz)', fontsize=12)
plt.ylabel('Power Spectral Density (arb. units)', fontsize=12)
plt.title('Frequency Spectrum of a HEALTHY Gear Pair (GMF = 792 Hz)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)

# نشان‌دادن فرکانس‌های مهم
for n in harmonics:
    f = n * GMF
    if f < 3500:
        plt.axvline(f, color='red', linestyle=':', alpha=0.8)
        plt.text(f + 20, max(psd)*0.9 - n*max(psd)*0.15,
                 f'Harmonic {n}\n({f:.0f} Hz)', color='red', fontsize=10)

plt.tight_layout()
plt.show()