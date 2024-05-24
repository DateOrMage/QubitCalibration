import numpy as np
from overrides import override
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from scipy.special import comb
from .BaseNode import BaseNode


class RawQubitAmpCalNode(BaseNode):

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, frequency data 
            :return SNRs: np.ndarray, SNRs data
        """
        data = self.get_data()
        voltage, SNRs = data[0], data[1]
        return voltage, SNRs

    
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
    def create_plot(voltage, SNRs, curve_points, v_max) -> plt:
        """ Method creates plot for data and optimized function
            :return plot: plt, plot that shows data optimization result
        """

        plt.scatter(voltage, SNRs, label='Data')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'g-', label='Кривая Безье')
        plt.axvline(x=v_max, color='r', linestyle='--')
        plt.legend()
        plt.xlabel('Voltage, V')
        plt.ylabel('SNR')
        plt.title(f'Drive amp. sweep, maximum at {round(v_max, 6)}V')
        
        return plt


    @override
    def run(self):
        """ Method executing calculation on node
            :return v_max: float, specified value of voltage
            :return plot: plt, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        is_correct = True
        voltage, SNRs = self.convert_data()

        control_points = np.column_stack((voltage, SNRs))
        t = np.linspace(0, 1, 10000)
        SNRs_linspace = np.linspace(min(SNRs), max(SNRs), 10000)
        curve_points = np.array([self.bezier_curve(control_points, ti) for ti in t])

        max_index = np.argmax(curve_points[:, 1])
        v_max = curve_points[max_index, 0]


        entropy_H2_4_fine_resonator_freq_cal = self.entropy_H2(SNRs)
        print(f'entropy H2 4 fine_resonator_freq_cal - {entropy_H2_4_fine_resonator_freq_cal}')
      


        bezier_curve_mse = mean_squared_error(SNRs_linspace, curve_points[:, 1])
        print(f'mse - {bezier_curve_mse}')

        plot = self.create_plot(voltage, SNRs, curve_points, v_max)
        
        

        return v_max, plot, is_correct