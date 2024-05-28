import numpy as np
from overrides import override
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import math

from .BaseNode import BaseNode


class IQCalNode(BaseNode):

    def __init__(self, filename) -> None:
        super().__init__(filename)


    @override
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, frequency data 
            :return SNRs: np.ndarray, SNRs data
        """
        data = self.get_data()
        data_real_g, data_imag_g, data_real_e, data_imag_e = data[0], data[1], data[2], data[3]
        return data_real_g, data_imag_g, data_real_e, data_imag_e


    @staticmethod
    def circle_residuals(params, x, y):
        x0, y0, r = params
        return (x - x0)**2 + (y - y0)**2 - r**2


    @staticmethod
    def is_inside_circle(point, x0, y0, r):
        distance = np.sqrt((point[0] - x0)**2 + (point[1] - y0)**2)
        return distance <= r


    @staticmethod
    def create_plot(data_real_g, data_imag_g, data_real_e, data_imag_e, x0, y0, x1, y1, r0, r1, dist) -> plt:
        """ Method creates plot for data and optimized function
            :return plot: plt, plot that shows optimization result
        """
        
        plt.figure(figsize=(10, 6))

        plt.scatter(data_real_e, data_imag_e, label=f'e = {abs(r0):.2f}', color='orange')
        plt.scatter(data_real_g, data_imag_g, label=f'g = {abs(r1):.2f}', color='blue')

        # Добавление центров окружностей
        plt.scatter(x0, y0, color='green', s=200, marker='o', label='Center e')
        plt.scatter(x1, y1, color='red', s=200, marker='o', label='Center g')

        # Добавление окружностей
        c0 = plt.Circle((x0, y0), r0, fill=False, color='green', linestyle='--')
        c1 = plt.Circle((x1, y1), r1, fill=False, color='red', linestyle='--')
        plt.gca().add_artist(c0)
        plt.gca().add_artist(c1)

        plt.xlabel('i')
        plt.ylabel('q')
        plt.title(f'iq-diagram, Distance between centers: {dist:.2f}')
        plt.legend()
        plt.grid()
    
        return plt


    def optimize_circle(self, data_real, data_imag):
        initial_guess = [0, 0, 1]
        result = least_squares(self.circle_residuals, initial_guess, args=(data_real, data_imag))
        x0, y0, r = result.x

        return x0, y0, r


    @override
    def run(self):
        """ Method executing calculation on node
            :return result: str, str that represents specified value of distance between centers of circles
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        min_distance = 120
        data_real_g, data_imag_g, data_real_e, data_imag_e = self.convert_data()
        
        x0, y0, r0 = self.optimize_circle(data_real_e, data_imag_e)
        x1, y1, r1 = self.optimize_circle(data_real_g, data_imag_g)
        dist = math.hypot(x0 - x1, y0 - y1)

        plot = self.create_plot(data_real_g, data_imag_g, data_real_e, data_imag_e, x0, y0, x1, y1, r0, r1, dist)

        is_correct = True if dist >= min_distance else False
        
        result = f'distance between centers - {dist}'
        return result, plot, is_correct
        
