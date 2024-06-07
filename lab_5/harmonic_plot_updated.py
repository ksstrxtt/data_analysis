import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons, TextBox
import numpy as np
from scipy.signal import butter, filtfilt

def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def create_noise(t, noise_mean, noise_covariance):
    return np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))

def harmonic_with_noise(t, amplitude, frequency, phase=0, noise_mean=0, noise_covariance=0.1, show_noise=None, noise=None):
    harmonic_signal = harmonic(t, amplitude, frequency, phase)
    if noise is not None and show_noise:
        return harmonic_signal + noise
    elif show_noise:
        global noise_g
        noise_g = create_noise(t, noise_mean, noise_covariance)
        return harmonic_signal + noise_g
    else:
        return harmonic_signal

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff_freq, fs, order=5):
    b, a = butter_lowpass(cutoff_freq, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Initial parameters
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
noise_g = None

t = np.linspace(0, 10, 1000)
sampling_frequency = 1 / (t[1] - t[0])

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4, right=0.9, top=0.95)

harmonic_line, = ax.plot(t, harmonic(t, initial_amplitude, initial_frequency, initial_phase), lw=2, color='blue', linestyle=':', label='Harmonic Signal')
with_noise_line, = ax.plot(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, show_noise=True, noise=None), lw=2, color='red', label='Noise Signal')
filtered_signal = lowpass_filter(with_noise_line.get_ydata(), 3, sampling_frequency, order=5)
l_filtered, = ax.plot(t, filtered_signal, lw=2, color='green', label='Filtered Signal')
ax.legend()

# Customize the appearance
ax.set_facecolor('#f0f0f0')
ax.grid(True, linestyle='--', linewidth=0.5)

# Add titles and labels
ax.set_title('Harmonic Signal Analysis', fontsize=16, fontweight='bold')
ax.set_xlabel('Time (s)', fontsize=14)
ax.set_ylabel('Amplitude', fontsize=14)

# Slider axes
axcolor = 'lightgoldenrodyellow'
ax_amplitude = plt.axes([0.1, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_frequency = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_noise_covariance = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)

s_amplitude = Slider(ax_amplitude, 'Amplitude', 0.1, 10.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Frequency', 0.1, 10.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Noise Covariance', 0.0, 1.0, valinit=initial_noise_covariance)

ax_cutoff_frequency = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
s_cutoff_frequency = Slider(ax_cutoff_frequency, 'Cutoff Frequency', 0.1, 10.0, valinit=3)

# CheckButtons for toggling the noise
rax = plt.axes([0.8, 0.5, 0.1, 0.15], facecolor=axcolor)
cb_show_noise = CheckButtons(rax, ['Show Noise'], [True])

# Buttons for additional functionalities
button_regenerate_noise = Button(plt.axes([0.8, 0.425, 0.1, 0.04]), 'Regenerate Noise', color=axcolor, hovercolor='0.975')
button_random_params = Button(plt.axes([0.8, 0.35, 0.1, 0.04]), 'Random Params', color=axcolor, hovercolor='0.975')
button_reset = Button(plt.axes([0.8, 0.275, 0.1, 0.04]), 'Reset', color=axcolor, hovercolor='0.975')

# TextBox for dynamic title update
ax_textbox = plt.axes([0.8, 0.6, 0.1, 0.05], facecolor=axcolor)
textbox_title = TextBox(ax_textbox, 'Title', initial='Harmonic Signal Analysis')

def update(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val

    harmonic_line.set_ydata(harmonic(t, amplitude, frequency, phase))
    with_noise_line.set_ydata(harmonic_with_noise(t, amplitude, frequency, phase, noise=noise_g, show_noise=cb_show_noise.get_status()[0]))

    cutoff_frequency = s_cutoff_frequency.val
    filtered_signal = lowpass_filter(with_noise_line.get_ydata(), cutoff_frequency, sampling_frequency)
    l_filtered.set_ydata(filtered_signal)

    fig.canvas.draw_idle()

def update_chb(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val

    harmonic_line.set_ydata(harmonic(t, amplitude, frequency, phase))
    with_noise_line.set_ydata(harmonic_with_noise(t, amplitude, frequency, phase, noise=noise_g, show_noise=cb_show_noise.get_status()[0]))
    fig.canvas.draw_idle()

def update_noise(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    harmonic_line.set_ydata(harmonic(t, amplitude, frequency, phase))
    with_noise_line.set_ydata(harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, cb_show_noise.get_status()[0]))

    cutoff_frequency = s_cutoff_frequency.val
    filtered_signal = lowpass_filter(with_noise_line.get_ydata(), cutoff_frequency, sampling_frequency)
    l_filtered.set_ydata(filtered_signal)
    fig.canvas.draw_idle()

def update_amplitude(val):
    global noise_g
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    harmonic_line.set_ydata(harmonic(t, amplitude, frequency, phase))
    with_noise_line.set_ydata(harmonic_with_noise(t, amplitude, frequency, phase, noise=noise_g, show_noise=cb_show_noise.get_status()[0]))

    cutoff_frequency = s_cutoff_frequency.val
    filtered_signal = lowpass_filter(with_noise_line.get_ydata(), cutoff_frequency, sampling_frequency)
    l_filtered.set_ydata(filtered_signal)
    fig.canvas.draw_idle()

    min_y = harmonic_with_noise(t, amplitude, frequency, phase, noise=noise_g, show_noise=cb_show_noise.get_status()[0]).min() - 2
    max_y = harmonic_with_noise(t, amplitude, frequency, phase, noise=noise_g, show_noise=cb_show_noise.get_status()[0]).max() + 2

    ax.set_ylim(int(min_y), int(max_y))

    fig.canvas.draw_idle()

def regenerate_noise(event):
    with_noise_line.set_ydata(harmonic_with_noise(t, s_amplitude.val, s_frequency.val, s_phase.val, s_noise_mean.val, s_noise_covariance.val, show_noise=True))
    fig.canvas.draw_idle()

def random_params(event):
    s_amplitude.set_val(np.random.uniform(0.1, 10.0))
    s_frequency.set_val(np.random.uniform(0.1, 10.0))
    s_phase.set_val(np.random.uniform(0.0, 2 * np.pi))
    s_noise_mean.set_val(np.random.uniform(-1.0, 1.0))
    s_noise_covariance.set_val(np.random.uniform(0.0, 1.0))
    regenerate_noise(event)

def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_frequency.reset()
    cb_show_noise.set_active(0)
    regenerate_noise(event)

def update_filter(val):
    cutoff_frequency = s_cutoff_frequency.val
    filtered_signal = lowpass_filter(with_noise_line.get_ydata(), cutoff_frequency, sampling_frequency)
    l_filtered.set_ydata(filtered_signal)
    fig.canvas.draw_idle()

def update_title(text):
    ax.set_title(text)
    fig.canvas.draw_idle()

s_amplitude.on_changed(update_amplitude)
s_frequency.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update_noise)
s_noise_covariance.on_changed(update_noise)
s_cutoff_frequency.on_changed(update_filter)

cb_show_noise.on_clicked(update_chb)
button_regenerate_noise.on_clicked(regenerate_noise)
button_random_params.on_clicked(random_params)
button_reset.on_clicked(reset)
textbox_title.on_submit(update_title)

plt.show()
