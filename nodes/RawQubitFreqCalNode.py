import numpy as np
import pickle
from abc import ABC, abstractmethod
from overrides import override
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from heapq import nlargest
from scipy.special import comb

from libs.pulses_processing import *
from libs.pi_pulse_cals_fw import *
from .BaseNode import BaseNode


class RawQubitFreqCalNode(BaseNode):

    def __init__(self) -> None:
        super().__init__()


    @staticmethod
    def bezier_curve(control_points, t):
        """ Method for optimizing data with bezier_curve
            :param control_points: coordinates of optimizing data
            :param t: 0-1 value for bezier curve
            :return curve_point:  
        """
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

        
        plt.scatter(freq, SNRs, label='Data')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'g-', label='Кривая Безье')
        plt.axvline(x=v_max, color='r', linestyle='--')
        plt.legend()
        plt.xlabel('Voltage, V')
        plt.ylabel('SNR')
        plt.title(f'Drive amp. sweep, maximum at {round(v_max, 6)}V')
        
        return plt
    
    
    @override
    def run_measurements(self, *args):
        q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, probe_pulse_duration, drive_f_sweep, start, stop, if_res = args
    
        I_g_drive, Q_g_drive = drive_frequency_sweep_ground (q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, probe_pulse_duration, [drive_f_sweep[0]])
        I_e_drive, Q_e_drive = drive_frequency_sweep_excited(q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, probe_pulse_duration, drive_f_sweep)

        drive_freqs_data = SNR_pi_pulse_calibrations(I_g_drive, Q_g_drive, I_e_drive, Q_e_drive, start, stop, if_res=if_res)

        return drive_f_sweep, drive_freqs_data




    @override
    def run(self, data):
        """ Method executing calculation on node
            :return result: str, str that represents value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        error_good = 0.1
        std_dev = 0.01
        is_correct = True
        freq, SNRs = data
        
        t = np.linspace(0, 1, 1000)

        control_points = np.column_stack((freq, SNRs))
        SNRs_linspace = np.linspace(min(SNRs), max(SNRs), 1000)
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
