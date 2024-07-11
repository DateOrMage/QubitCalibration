from overrides import override
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from libs.pulses_processing import *
from libs. qubit_characterization import *
from .BaseNode import BaseNode


class QubitLifetimeNode(BaseNode):

    def __init__(self) -> None:
        super().__init__()

    
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
    def run_measurements(self, *args):
        
        q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, decay_lengths, I_cal_g, Q_cal_g, I_cal_e, Q_cal_e, start, stop, if_res = args

        I_decay, Q_decay = decay_1Q (q_num, qubits_params, mixer_cals, chip_name, hdawg, key, AVGS_POW, AVGS, decay_lengths)

        z0, z1 = data_centering(I_cal_g, Q_cal_g, I_cal_e, Q_cal_e, start, stop, 'rotation')
        p0, p1 = probabilities(z0, z1, I_decay, Q_decay, start, stop, 'rotation', if_res)

        return decay_lengths, p0, p1, 



    @override
    def run(self, data):
        """ Method executing calculation on node
            :return result: str, str that represents specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        error_good = 0.6
        std_dev = 0.01
        is_correct = True
        time, _, probability = data
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