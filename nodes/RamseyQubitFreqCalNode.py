import numpy as np
import pickle
from abc import ABC, abstractmethod
from overrides import override
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from .BaseNode import BaseNode


class RamseyQubitFreqCalNode(BaseNode):

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, time data 
            :return SNRs: np.ndarray, probability data
        """
        data = self.get_data()
        time, probability = data[0], data[1]
        return time, probability


    @staticmethod
    def find_monotonicity_changes(x, y):
        derivatives = np.gradient(y, x)
        sign_changes = np.where(np.diff(np.sign(derivatives)))[0]
        points_of_change = [(x[i], y[i]) for i in sign_changes]
        return points_of_change


    @staticmethod
    def create_plot(time, probability, y_cosine, freq_rams) -> plt:
        """ Method creates plot for data and optimized function
            :return plot: plt, plot that shows data optimization result
        """

        plt.figure(figsize=(9, 5))
        plt.plot(time, probability, 'b',marker='o', label='Исходные данные')
        plt.plot(time, y_cosine, 'g', label=f'framsey = {freq_rams} MHz')
        plt.xlabel('Time')
        plt.ylabel('Probability')
        plt.grid(True)
        plt.title(f'f_ramsey = {freq_rams} MHz')
        plt.tight_layout()
    
        return plt


    @staticmethod
    def fit_cosine(x, a, b, c, d):
       return c * np.cos(x * a + d) + b


    @override
    def run(self):
        """ Method executing calculation on node
            :return result: str, str that represents specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        error_good = 0.01
        std_dev = 0.001
        is_correct = True
        time, probability = self.convert_data()
        popt, pcov = curve_fit(self.fit_cosine, time, probability)
        a, b, c, d = popt
        y_cosine = self.fit_cosine(time, a, b, c, d)
        freq_rams = round(a/(2*np.pi*1000000), 3)
        
        plot = self.create_plot(time, probability, y_cosine, freq_rams)

        threshold_error = self.calculate_threshold(error_good, std_dev)

        points_of_change = self.find_monotonicity_changes(time, y_cosine)
        num_monotonicity_changes = len(points_of_change)
        print(num_monotonicity_changes)
        print(self.error_based_on_range(probability))
        if self.error_based_on_range(probability) > threshold_error and num_monotonicity_changes < 2:
            is_correct = False
    
        result = f'{freq_rams} Mhz'
    
        return result, plot, is_correct
