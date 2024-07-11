import numpy as np
from overrides import override
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from scipy.special import comb

from libs.pi_pulse_cals_fw import *  # type: ignore
from libs.pulses_processing import * # type: ignore
from .BaseNode import BaseNode


class RawResonatorFreqCalNode(BaseNode):

    def __init__(self) -> None:
        super().__init__()



    @staticmethod
    def bezier_curve(control_points, t):
        n = len(control_points) - 1
        curve_point = np.zeros(2)
        for i in range(n + 1):
            curve_point += control_points[i] * comb(n, i) * (1 - t)**(n - i) * t**i
        return curve_point
    
    @staticmethod
    def create_plot(freq, SNRs, curve_points, v_max) -> plt:
        """ Method creates plot for data and optimized function
            :return plot: plt, plot that shows data optimization result
        """

        
        plt.figure(figsize=(10, 5))
        plt.plot(freq, SNRs, c='b', marker='o', label='Data')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'g-', label='Bezier curve')
        plt.axvline(x=v_max, color='r', linestyle='--', label=f'Max frequency = {v_max}')
        plt.xlabel('Frequency, GHz')
        plt.ylabel('SNR')
        plt.title(f'Probe freq sweep, maximum at {v_max} GHz')
        plt.grid(True)
        plt.legend()

        return plt
    
    @override
    def run_measurements(self, *args):     
        
        q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, probe_pulse_duration, probe_f_sweep, start, stop, if_res = args

        I_g_probe, Q_g_probe = probe_frequency_sweep_ground(q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, probe_pulse_duration, probe_f_sweep)
        I_e_probe, Q_e_probe = probe_frequency_sweep_excited(q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, probe_pulse_duration, probe_f_sweep)

        probe_freqs_data, signal_g, signal_e = SNR_pi_pulse_calibrations(I_g_probe, Q_g_probe, I_e_probe, Q_e_probe, start, stop, if_res=if_res, shift=True)
        
        return probe_f_sweep, probe_freqs_data

    @override
    def run(self, data):
        """ Method executing calculation on node
            :return result: str, str that represents specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        
        error_good = 0.2
        std_dev = 0.01
        is_correct = True
        freq, SNRs = data

        SNRs_linspace = np.linspace(min(SNRs), max(SNRs), 1000)
        control_points = np.column_stack((freq, SNRs))
        t = np.linspace(0, 1, 1000)
        curve_points = np.array([self.bezier_curve(control_points, ti) for ti in t])

        freq_max_index = np.argmax(curve_points[:, 1])
        freq_max = curve_points[freq_max_index, 0]
        freq_max_rounded = round(freq_max / 1000000000, 6)
    
        threshold_error = self.calculate_threshold(error_good, std_dev)
        
        if threshold_error < self.error_based_on_range(SNRs):
            is_correct = False

        bezier_curve_mse = mean_squared_error(SNRs_linspace, curve_points[:, 1])
        print(f'mse - {bezier_curve_mse}')
        plot = self.create_plot(freq, SNRs, curve_points, freq_max)
        result = f'{freq_max_rounded} Ghz'
        return result, plot, is_correct
    


uzel = RawResonatorFreqCalNode()

