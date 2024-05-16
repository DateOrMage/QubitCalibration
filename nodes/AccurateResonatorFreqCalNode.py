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


class AccurateResonatorFreqCalNode(BaseNode):
    '''Точная калибровка частоты резонатора'''
    
    def __init__(self, filename) -> None:
        super().__init__(filename)

    
    @override
    def convert_data(self):
        data = self.get_data(self.filename)
        freq, SNRs = data[0], data[1]
        return freq, SNRs

    
    
    @override
    def run():
        pass
