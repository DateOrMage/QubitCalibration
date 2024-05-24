import numpy as np
import pickle
from abc import ABC, abstractmethod
from overrides import override
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from heapq import nlargest
from scipy.special import comb
from BaseNode import BaseNode


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
    

    @override
    def run(self):
        """ Method executing calculation on node
            :return x_max: float, specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        is_correct = True
        freq, SNRs = self.convert_data()
        control_points = np.column_stack((freq, SNRs))
        t = np.linspace(0, 1, 1000)
        curve_points = np.array([self.bezier_curve(control_points, ti) for ti in t])
        max_index = np.argmax(curve_points[:, 1])
        x_max = curve_points[max_index, 0]
        max_x_value = round(x_max / 1000000000, 6)
    
        plt.figure(figsize=(10, 5))
        plt.plot(freq, SNRs, c='b', marker='o', label='Исходные точки')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'g-', label='Аппроксимация Безье')
        plt.axvline(x=x_max, color='r', linestyle='--', label=f'Max frequency = {max_x_value}')
        plt.xlabel('Frequency, GHz')
        plt.ylabel('SNR')
        plt.title(f'Probe freq sweep, maximum at {max_x_value} GHz')
        plt.grid(True)
        plt.legend() 

        return max_x_value, plt, is_correct