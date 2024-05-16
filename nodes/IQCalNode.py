import numpy as np
import pickle
from abc import ABC, abstractmethod
from typing import override
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from heapq import nlargest
from scipy.special import comb
from BaseNode import BaseNode


class IQCalNode(BaseNode):
    '''Калибровка состояний 0, 1'''

    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        data = self.get_data(self.filename)
        data_real_g, data_imag_g, data_real_e, data_imag_e = data[0], data[1], data[2], data[3]
        return data_real_g, data_imag_g, data_real_e, data_imag_e
    
    
    @override
    def run():
        pass
