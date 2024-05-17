import numpy as np
from overrides import override
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from scipy.special import comb
from .BaseNode import BaseNode


class RawQubitAmpCalNode(BaseNode):
    '''Грубая калибровка амплитуды кубита'''

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        '''Конвертация данных'''
        data = self.get_data()
        voltage, SNRs = data[0], data[1]
        return voltage, SNRs
    
    @staticmethod
    def target(params, x, y):
        '''Целевая функция'''

        A1, t, decay, A3 , teta, A0 = params
        predicted = A1*np.exp(-t/decay)*np.cos(x*A3*t + teta)+A0
        error = np.mean((predicted - y) ** 2)

        return error
    
    @staticmethod
    def bezier_curve(control_points, t):
        '''Кривая Безье'''
        n = len(control_points) - 1
        curve_point = np.zeros(2)
        for i in range(n + 1):
            curve_point += control_points[i] * comb(n, i) * (1 - t)**(n - i) * t**i
        return curve_point
    
    
    def optimize(self, voltage, SNRs):
        '''Оптимизатор'''

        initial_guess = [1, 1, 1, 1, 1, 1]
        result = minimize(self.target, initial_guess, args=(voltage, SNRs), method='powell')

        A1, t, decay, A3 , teta, A0 = result.x
        opt_func = A1*np.exp(-t/decay)*np.cos(voltage*A3*t + teta)+A0
        x_func = np.linspace(voltage.min(), voltage.max(), 10000)
        y_func = A1*np.exp(-t/decay)*np.cos(x_func*A3*t + teta)+A0
        return x_func, y_func, opt_func



    @override
    def run(self):
        voltage, SNRs = self.convert_data()

        x_func, y_func, opt_func = self.optimize(voltage, SNRs)

        control_points = np.column_stack((voltage, SNRs))
        t = np.linspace(0, 1, 10000)
        curve_points = np.array([self.bezier_curve(control_points, ti) for ti in t])

        max_index = np.argmax(curve_points[:, 1])
        x_max = curve_points[max_index, 0]

        entropy_H1_4_raw_qubit_amp_cal_good = self.entropy_H1_new(SNRs)
        entropy_H2_4_raw_qubit_amp_cal_good = self.entropy_H2(SNRs)
        entropy_H3_4_raw_qubit_amp_cal_good = self.entropy_H3(SNRs)


        bezier_curve_mse = mean_squared_error(y_func, curve_points[:, 1])


        plt.scatter(voltage, SNRs, label='Data')
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'g-', label='Кривая Безье')
        plt.axvline(x=x_max, color='r', linestyle='--')
        plt.legend()
        plt.xlabel('Voltage, V')
        plt.ylabel('SNR')
        plt.title(f'Drive amp. sweep, maximum at {round(x_max, 6)}V')
        

        return x_max, plt