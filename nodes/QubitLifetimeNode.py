from overrides import override
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from .BaseNode import BaseNode


class QubitLifetimeNode(BaseNode):

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, frequency data 
            :return SNRs: np.ndarray, SNRs data
        """
        data = self.get_data()
        time, probability = data[0], data[1]
        return time, probability
    
    @staticmethod
    def expa(x, a, b, c):
        return a * np.exp(-b * x) + c
    
    
    @staticmethod
    def create_plot(time, probability, prob_fit, decay):
        plt.figure(figsize=(9, 5))
        plt.plot(time, probability, 'b', marker='o')
        plt.plot(time, prob_fit, 'g')
        plt.xlabel('Time')
        plt.ylabel('Probability')
        plt.grid(True)
        plt.title(f'Decay T = {decay}')
        plt.tight_layout()
        return plt
    
    @override
    def run(self):
        """ Method executing calculation on node
            :return result: str, str that represents specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        error_good = 0.6
        std_dev = 0.01
        is_correct = True
        time, probability = self.convert_data()
        a_guess = np.max(probability)
        b_guess = len(time) / (time[-1] - time[0])
        c_guess = np.min(probability)
        p0 = [a_guess, b_guess, c_guess]
        popt, pcov = curve_fit(self.expa, time, probability, p0=p0)
        a, b, c = popt
        prob_fit = self.expa(time, a, b, c)
        decay = round((1 / b) * 1000000, 2)
        threshold_error = self.calculate_threshold(error_good, std_dev)
        if threshold_error < self.error_based_on_range(probability):
            is_correct = False

        plot = self.create_plot(time, probability, prob_fit, decay)
        
        result = decay

        return result, plot, is_correct