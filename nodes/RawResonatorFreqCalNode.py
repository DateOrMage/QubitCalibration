import numpy as np
import pickle
from abc import ABC, abstractmethod
from overrides import override
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from heapq import nlargest
from scipy.special import comb
from .BaseNode import BaseNode


class RawResonatorFreqCalNode(BaseNode):

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, frequency data 
            :return SNRs: np.ndarray, SNRs data
        """
        data = self.get_data()
        freq, SNRs = data[0], data[1]
        return freq, SNRs

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
    def run(self):
        """ Method executing calculation on node
            :return result: str, str that represents specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        error_good = 0.2
        std_dev = 0.01
        is_correct = True
        freq, SNRs = self.convert_data()

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