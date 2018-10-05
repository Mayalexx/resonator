"""
Plot resonator data and fits on matplotlib Axes.
"""
# ToDo: replace mmr with method calls
from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
try:
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']  # matplotlib >= 1.5
except KeyError:
    color_cycle = plt.rcParams['axes.color_cycle']  # matplotlib < 1.5
import numpy as np

DEFAULT_NUM_MODEL_POINTS = 10000

measurement_defaults = {'linestyle': 'none',
                        'marker': '.',
                        'markersize': 2,
                        'color': 'gray',
                        'alpha': 1}

model_defaults = {'linestyle': '-',
                  'linewidth': 0.3,
                  'color': color_cycle[0],
                  'alpha': 1}

resonance_defaults = {'linestyle': 'none',
                      'marker': '.',
                      'markersize': 3,
                      'color': color_cycle[1],
                      'alpha': 1}


frequency_scale_to_unit = {1: 'Hz',
                           1e-3: 'kHz',
                           1e-6: 'MHz',
                           1e-9: 'GHz',
                           1e-12: 'THz'}


def magnitude_vs_frequency(resonator, axes, normalize=False, num_model_points=DEFAULT_NUM_MODEL_POINTS,
                           frequency_scale=1, three_ticks=True, decibels=True, label_axes=True,
                           measurement_settings=None, model_settings=None, resonance_settings=None):
    """
    Plot magnitude versus frequency on the given axis for the data, best-fit model, and model at the best-fit resonance
    frequency; return a structure containing the measurement, model, and resonance values.

    :param resonator: an instance of a fitter.ResonatorFitter subclass.
    :param axes: a matplotlib Axes instance.
    :param normalize: if True, normalize the plotted values by dividing them by the best-fit background model values.
    :param num_model_points: the number of points at which to evaluate the model over the frequency range.
    :param frequency_scale: a float by which the plotted frequencies are multiplied.
    :param three_ticks: if True, the horizontal axis will have exactly three tick marks at the minimum frequency,
      resonance frequency, and maximum frequency.
    :param decibels: if True, the magnitude will be plotted in dB.
    :param label_axes: if True, give the axes reasonable labels.
    :param measurement_settings: a dict of pyplot.plot keywords used to plot the measurement values; see
      measurement_defaults above.
    :param model_settings: a dict of pyplot.plot keywords used to plot the model values; see model_defaults above.
    :param resonance_settings: a dict of pyplot.plot keywords used to plot the model values at the resonance frequency;
     see resonance_defaults above.
    :return: a fitter.MeasurementModelResonance object containing the measurement, model, and resonance values, either
      normalized or not.
    """
    measurement_kwds = measurement_defaults.copy()
    if measurement_settings is not None:
        measurement_kwds.update(measurement_settings)
    model_kwds = model_defaults.copy()
    if model_settings is not None:
        model_kwds.update(model_settings)
    resonance_kwds = resonance_defaults.copy()
    if resonance_settings is not None:
        resonance_kwds.update(resonance_settings)
    mmr = resonator.measurement_model_resonance(normalize=normalize, num_model_points=num_model_points)
    if decibels:
        data_transform = lambda data: 20 * np.log10(np.abs(data))
        vertical_label = 'magnitude / dB'
    else:
        data_transform = lambda data: np.abs(data)
        vertical_label = 'magnitude'
    axes.plot(frequency_scale * mmr.measurement_frequency, data_transform(mmr.measurement_data), **measurement_kwds)
    axes.plot(frequency_scale * mmr.model_frequency, data_transform(mmr.model_data), **model_kwds)
    axes.plot(frequency_scale * mmr.resonance_frequency, data_transform(mmr.resonance_data), **resonance_kwds)
    if three_ticks:
        axes.set_xticks(frequency_scale * np.array([mmr.measurement_frequency.min(), mmr.resonance_frequency,
                                                    mmr.measurement_frequency.max()]))
    if label_axes:
        try:
            axes.set_xlabel('frequency / {}'.format(frequency_scale_to_unit[frequency_scale]))
        except KeyError:
            axes.set_xlabel('frequency')
        axes.set_ylabel(vertical_label)
    return mmr


def phase_vs_frequency(resonator, axes, normalize=False, num_model_points=DEFAULT_NUM_MODEL_POINTS,
                       frequency_scale=1, three_ticks=True, degrees=True, label_axes=True,
                       measurement_settings=None, model_settings=None, resonance_settings=None):
    """
    Plot phase versus frequency on the given axis for the data, best-fit model, and model at the best-fit resonance
    frequency; return a structure containing the measurement, model, and resonance values.

    :param resonator: an instance of a fitter.ResonatorFitter subclass.
    :param axes: a matplotlib Axes instance.
    :param normalize: if True, normalize the plotted values by dividing them by the best-fit background model values.
    :param num_model_points: the number of points at which to evaluate the model over the frequency range.
    :param frequency_scale: a float by which the plotted frequencies are multiplied.
    :param three_ticks: if True, the horizontal axis will have exactly three tick marks at the minimum frequency,
      resonance frequency, and maximum frequency.
    :param degrees: if True, the phase will be plotted in degrees instead of radians.
    :param label_axes: if True, give the axes reasonable labels.
    :param measurement_settings: a dict of pyplot.plot keywords used to plot the measurement values; see
      measurement_defaults above.
    :param model_settings: a dict of pyplot.plot keywords used to plot the model values; see model_defaults above.
    :param resonance_settings: a dict of pyplot.plot keywords used to plot the model values at the resonance frequency;
     see resonance_defaults above.
    :return: a fitter.MeasurementModelResonance object containing the measurement, model, and resonance values, either
      normalized or not.
    """
    measurement_kwds = measurement_defaults.copy()
    if measurement_settings is not None:
        measurement_kwds.update(measurement_settings)
    model_kwds = model_defaults.copy()
    if model_settings is not None:
        model_kwds.update(model_settings)
    resonance_kwds = resonance_defaults.copy()
    if resonance_settings is not None:
        resonance_kwds.update(resonance_settings)
    mmr = resonator.measurement_model_resonance(normalize=normalize, num_model_points=num_model_points)
    if degrees:
        data_transform = lambda data: np.degrees(np.angle(data))
        vertical_label = 'phase / deg'
    else:
        data_transform = lambda data: np.angle(data)
        vertical_label = 'phase / rad'
    axes.plot(frequency_scale * mmr.measurement_frequency, data_transform(mmr.measurement_data), **measurement_kwds)
    axes.plot(frequency_scale * mmr.model_frequency, data_transform(mmr.model_data), **model_kwds)
    axes.plot(frequency_scale * mmr.resonance_frequency, data_transform(mmr.resonance_data), **resonance_kwds)
    if three_ticks:
        axes.set_xticks(frequency_scale * np.array([mmr.measurement_frequency.min(), mmr.resonance_frequency,
                                                    mmr.measurement_frequency.max()]))
    if label_axes:
        try:
            axes.set_xlabel('frequency / {}'.format(frequency_scale_to_unit[frequency_scale]))
        except KeyError:
            axes.set_xlabel('frequency')
        axes.set_ylabel(vertical_label)
    return mmr


def real_and_imaginary(resonator, axes, normalize=False, num_model_points=DEFAULT_NUM_MODEL_POINTS, equal_aspect=True,
                       label_axes=True, measurement_settings=None, model_settings=None, resonance_settings=None):
    """
    Plot imaginary parts versus real parts on the given axis for the data, best-fit model, and model at the best-fit
    resonance frequency; return a structure containing the measurement, model, and resonance values.

    :param resonator: an instance of a fitter.ResonatorFitter subclass.
    :param axes: a matplotlib Axes instance.
    :param normalize: if True, normalize the plotted values by dividing them by the best-fit background model values.
    :param num_model_points: the number of points at which to evaluate the model over the frequency range.
    :param equal_aspect: if True, set the axes aspect ratio to 'equal' so that the normalized resonance forms a circle.
    :param label_axes: if True, give the axes reasonable labels.
    :param measurement_settings: a dict of pyplot.plot keywords used to plot the measurement values; see
      measurement_defaults above.
    :param model_settings: a dict of pyplot.plot keywords used to plot the model values; see model_defaults above.
    :param resonance_settings: a dict of pyplot.plot keywords used to plot the model values at the resonance frequency;
     see resonance_defaults above.
    :return: a fitter.MeasurementModelResonance object containing the measurement, model, and resonance values, either
      normalized or not.
    """
    measurement_kwds = measurement_defaults.copy()
    if measurement_settings is not None:
        measurement_kwds.update(measurement_settings)
    model_kwds = model_defaults.copy()
    if model_settings is not None:
        model_kwds.update(model_settings)
    resonance_kwds = resonance_defaults.copy()
    if resonance_settings is not None:
        resonance_kwds.update(resonance_settings)
    mmr = resonator.measurement_model_resonance(normalize=normalize, num_model_points=num_model_points)
    axes.plot(mmr.measurement_data.real, mmr.measurement_data.imag, **measurement_kwds)
    axes.plot(mmr.model_data.real, mmr.model_data.imag, **model_kwds)
    axes.plot(mmr.resonance_data.real, mmr.resonance_data.imag, **resonance_kwds)
    if equal_aspect:
        axes.set_aspect('equal')
    if label_axes:
        axes.set_xlabel('real')
        axes.set_ylabel('imag')
    return mmr
