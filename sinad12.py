import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft
from scipy.signal import find_peaks

def calculate_sinad(wav_filename, num_harmonics=5):
    # Load WAV file
    fs, data = wav.read(wav_filename)

    # Ensure mono signal
    if data.ndim > 1:
        data = data[:, 0]  # Use only the first channel if stereo

    # Normalize data to -1 to 1 range
    data = data / np.max(np.abs(data))

    # Apply Hanning window and compute FFT
    N = len(data)
    window = np.hanning(N)
    spectrum = np.abs(fft(data * window))[:N//2]  # One-sided spectrum
    freqs = np.fft.fftfreq(N, 1/fs)[:N//2]  # Corresponding frequencies

    # **Fix 1: Correct FFT Power Calculation with Window Gain Compensation**
    window_correction = np.sum(window**2) / N  # Normalization factor
    power_spectrum = (spectrum ** 2) / (window_correction * N)  # Proper power scaling

    # **Fix 2: Refine Fundamental Frequency Detection with Interpolation**
    peaks, _ = find_peaks(spectrum, height=np.max(spectrum) * 0.1)  # Adaptive threshold

    if len(peaks) > 0:
        fundamental_index = peaks[0]
    else:
        fundamental_index = np.argmax(spectrum)  # Fallback: Use max FFT bin

    # Use linear interpolation to refine fundamental frequency
    if fundamental_index > 0 and fundamental_index < len(freqs) - 1:
        left = spectrum[fundamental_index - 1]
        center = spectrum[fundamental_index]
        right = spectrum[fundamental_index + 1]
        correction = (right - left) / (2 * (2 * center - left - right))
        fundamental_freq = freqs[fundamental_index] + correction * (freqs[1] - freqs[0])
    else:
        fundamental_freq = freqs[fundamental_index]  # No correction if edge case

    # **Fix 3: More Accurate Signal Power Estimation (Using Adjacent Bins)**
    bin_width = 3  # Adjust based on FFT resolution
    signal_power = np.sum(power_spectrum[fundamental_index-bin_width : fundamental_index+bin_width+1])

    # **Fix 4: More Precise Harmonic Subtraction**
    harmonic_power = 0
    for i in range(2, num_harmonics + 1):
        harmonic_freq = fundamental_freq * i
        harmonic_idx = np.argmin(np.abs(freqs - harmonic_freq))
        harmonic_power += np.sum(power_spectrum[harmonic_idx-bin_width : harmonic_idx+bin_width+1])

    # **Fix 5: Improved Noise Floor Estimation**
    total_power = np.sum(power_spectrum)

    # Smoothing noise floor to reduce variance effects
    smoothed_spectrum = np.convolve(power_spectrum, np.ones(5)/5, mode='same')

    noise_power = max(np.sum(smoothed_spectrum) - (signal_power + harmonic_power), 1e-12)  # Prevent log(0)

    # Compute SINAD
    sinad_value = 10 * np.log10(signal_power / noise_power)

    print(f"SINAD: {sinad_value:.2f} dB")
    return sinad_value

# Example usage
sinad = calculate_sinad("input.wav")
