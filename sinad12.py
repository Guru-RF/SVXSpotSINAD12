import numpy as np
from scipy.io.wavfile import write

# Parameters
fs = 44100  # Sampling frequency
duration = 5  # seconds
f = 1000  # Frequency of the tone (1 kHz)

# Time array
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Generate tone (signal)
signal = np.sin(2 * np.pi * f * t)

# Generate white noise
noise = np.random.normal(0, 1, signal.shape)

# Adjust noise level to achieve 12 dB SINAD
signal_power = np.mean(signal**2)
noise_power = np.mean(noise**2)
k = np.sqrt(signal_power / (10**(12 / 10) * noise_power))
adjusted_noise = noise * k

# Combine signal and noise
combined = signal + adjusted_noise

# Normalize to prevent clipping
combined /= np.max(np.abs(combined))

# Save as WAV file
write('12dB_SINAD.wav', fs, np.int16(combined * 32767))
