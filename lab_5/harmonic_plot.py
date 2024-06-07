from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup, Button, TextInput, Div
import numpy as np
import random

def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def create_noise(t, noise_mean, noise_std):
    return np.random.normal(noise_mean, noise_std, len(t))

def harmonic_with_noise(t, amplitude, frequency, phase=0, noise_mean=0, noise_std=0.1, noise=None):
    harmonic_signal = harmonic(t, amplitude, frequency, phase)
    if noise is not None:
        return harmonic_signal + noise
    else:
        global noise_g
        noise_g = create_noise(t, noise_mean, noise_std)
        return harmonic_signal + noise_g

def moving_avg(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

# Initial parameters
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_std = 0.1

t = np.linspace(0, 10, 1000)

plot = figure(title="Harmonic Signal with Noise and Moving Average Filter",
              x_axis_label='Time', y_axis_label='Amplitude',
              width=800, height=400)

harmonic_line = plot.line(t, harmonic(t, initial_amplitude, initial_frequency, initial_phase),
                          line_width=2, color='blue', legend_label='Harmonic line')

with_noise_line = plot.line(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase,
                                                   initial_noise_mean, initial_noise_std),
                            line_width=2, color='red', legend_label='Signal with noise')

filtered_signal = moving_avg(with_noise_line.data_source.data['y'], 5)
filtered_line = plot.line(t, filtered_signal, line_width=2, color='green', legend_label='Filtered Signal')

# Widgets
s_amplitude = Slider(title="Amplitude", value=initial_amplitude, start=0.1, end=10.0, step=0.1)
s_frequency = Slider(title="Frequency", value=initial_frequency, start=0.1, end=10.0, step=0.1)
s_phase = Slider(title="Phase", value=initial_phase, start=0.0, end=2 * np.pi, step=0.1)
s_noise_mean = Slider(title="Noise Mean", value=initial_noise_mean, start=-1.0, end=1.0, step=0.1)
s_noise_std = Slider(title="Noise Std Dev", value=initial_noise_std, start=0.0, end=1.0, step=0.1)
s_window_size = Slider(title="Moving Average Window Size", value=5, start=1, end=50, step=1)

cb_show_noise = CheckboxGroup(labels=['Show Noise'], active=[0])
button_regenerate_noise = Button(label='Regenerate Noise', button_type='success')
button_random_params = Button(label='Random Params', button_type='warning')
button_reset = Button(label='Reset', button_type='danger')
input_title = TextInput(value='Harmonic Signal with Noise and Moving Average Filter', title='Plot Title:')
title_div = Div(text=f"<h2>{input_title.value}</h2>")

def update(attr, old, new):
    amplitude = s_amplitude.value
    frequency = s_frequency.value
    phase = s_phase.value
    noise_mean = s_noise_mean.value
    noise_std = s_noise_std.value
    window_size = s_window_size.value

    harmonic_line.data_source.data['y'] = harmonic(t, amplitude, frequency, phase)
    with_noise_line.data_source.data['y'] = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_std)
    filtered_signal = moving_avg(with_noise_line.data_source.data['y'], window_size)
    filtered_line.data_source.data['y'] = filtered_signal

    plot.title.text = input_title.value
    title_div.text = f"<h2>{input_title.value}</h2>"

def regenerate_noise():
    noise_mean = s_noise_mean.value
    noise_std = s_noise_std.value
    noise_g = create_noise(t, noise_mean, noise_std)
    update(None, None, None)

def random_params():
    s_amplitude.value = random.uniform(0.1, 10.0)
    s_frequency.value = random.uniform(0.1, 10.0)
    s_phase.value = random.uniform(0.0, 2 * np.pi)
    s_noise_mean.value = random.uniform(-1.0, 1.0)
    s_noise_std.value = random.uniform(0.0, 1.0)
    regenerate_noise()

def reset_params():
    s_amplitude.value = initial_amplitude
    s_frequency.value = initial_frequency
    s_phase.value = initial_phase
    s_noise_mean.value = initial_noise_mean
    s_noise_std.value = initial_noise_std
    s_window_size.value = 5
    input_title.value = 'Harmonic Signal with Noise and Moving Average Filter'
    regenerate_noise()

s_amplitude.on_change('value', update)
s_frequency.on_change('value', update)
s_phase.on_change('value', update)
s_noise_mean.on_change('value', update)
s_noise_std.on_change('value', update)
s_window_size.on_change('value', update)
input_title.on_change('value', update)

button_regenerate_noise.on_click(regenerate_noise)
button_random_params.on_click(random_params)
button_reset.on_click(reset_params)

layout = column(title_div, plot,
                row(s_amplitude, s_frequency, s_phase),
                row(s_noise_mean, s_noise_std, s_window_size),
                row(cb_show_noise, button_regenerate_noise, button_random_params, button_reset),
                input_title,
                sizing_mode='stretch_width')

curdoc().add_root(layout)
