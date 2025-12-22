import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# پارامترهای فیزیکی تست (بر اساس گزارش فارسی - تست اول)
# ----------------------------
fs = 10000           # نرخ نمونه‌برداری (Hz)
T = 4.0              # مدت زمان سیگنال (ثانیه)
t = np.linspace(0, T, int(fs * T), endpoint=False)

RPM = 2507
f_shaft = RPM / 60   # 41.7 Hz
GMF = f_shaft * 10   # فقط برای نمایش واضح — ولی ما می‌خوایم 19 دندانه داشته باشه
# دقیق‌تر:
teeth = 19
GMF = f_shaft * teeth  # 792.3 Hz

print(f"Shaft Frequency: {f_shaft:.1f} Hz")
print(f"GMF: {GMF:.1f} Hz")

# ----------------------------
# 1. ساخت سیگنال سالم
# ----------------------------
harmonics = [1, 2, 3, 4]
amps = [1.0, 0.12, 0.04, 0.015]

signal_healthy = np.zeros_like(t)
for n, amp in zip(harmonics, amps):
    signal_healthy += amp * np.sin(2 * np.pi * n * GMF * t)

# نویز کم
np.random.seed(0)
signal_healthy += 0.01 * np.random.randn(len(t))

# ----------------------------
# 2. ساخت سیگنال معیوب (یک دندانه خراب)
# ----------------------------
# روش: مدولاسیون دامنه با فرکانس f_shaft
# چون هر دور یک‌بار دندانه معیوب عبور می‌کنه

# اول سیگنال تماس عادی (بدون توجه به عیب)
base_signal = np.zeros_like(t)
for n, amp in zip(harmonics, amps):
    base_signal += amp * np.sin(2 * np.pi * n * GMF * t)

# حالا دامنه‌اش رو با فرکانس f_shaft مدوله کن (ضربه قوی‌تر هر دور)
modulation = 1 + 0.4 * np.sin(2 * np.pi * f_shaft * t)  # 40% عیب — قابل تنظیم
signal_faulty = base_signal * modulation

# نویز
signal_faulty += 0.01 * np.random.randn(len(t))

# ----------------------------
# 3. محاسبه FFT برای هر دو
# ----------------------------
def compute_psd(signal, fs):
    N = len(signal)
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    psd = np.abs(fft_vals) ** 2
    return freqs, psd

freq_h, psd_h = compute_psd(signal_healthy, fs)
freq_f, psd_f = compute_psd(signal_faulty, fs)

# ----------------------------
# 4. رسم نمودارها
# ----------------------------
plt.figure(figsize=(14, 10))

# -------- سیگنال سالم --------
plt.subplot(2, 1, 1)
plt.plot(freq_h, psd_h, color='steelblue', linewidth=1.2)
plt.xlim(0, 2500)
plt.title('سیگنال سالم — فقط GMF و هارمونیک‌های ضعیف', fontsize=14)
plt.ylabel('Power Spectrum (arb. units)')
plt.grid(True, linestyle='--', alpha=0.6)

# نشان‌دادن GMF و هارمونیک‌ها
for n in range(1, 5):
    f = n * GMF
    if f < 2500:
        plt.axvline(f, color='red', linestyle=':', alpha=0.8)
        plt.text(f + 30, np.max(psd_h)*0.9 - n*0.15*np.max(psd_h),
                 f'Harmonic {n}', color='red')

# -------- سیگنال معیوب --------
plt.subplot(2, 1, 2)
plt.plot(freq_f, psd_f, color='darkorange', linewidth=1.2)
plt.xlim(0, 2500)
plt.title('سیگنال معیوب — پیک‌های جانبی حول GMF', fontsize=14)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectrum (arb. units)')
plt.grid(True, linestyle='--', alpha=0.6)

# نشان‌دادن GMF
plt.axvline(GMF, color='black', linestyle='-', linewidth=1.5, label='GMF')

# نشان‌دادن sidebands: GMF ± n * f_shaft
for n in range(1, 4):
    f_low = GMF - n * f_shaft
    f_high = GMF + n * f_shaft
    if f_low > 0:
        plt.axvline(f_low, color='green', linestyle='--', alpha=0.8)
    if f_high < 2500:
        plt.axvline(f_high, color='green', linestyle='--', alpha=0.8)
    # نوشتن n=1,2,...
    if n == 1 and GMF + f_shaft < 2500:
        plt.text(GMF + f_shaft + 30, np.max(psd_f)*0.8,
                 f'Sidebands (±{n}×f_shaft)', color='green')

plt.legend()
plt.tight_layout()
plt.show()