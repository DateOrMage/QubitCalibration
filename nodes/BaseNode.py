import numpy as np
import matplotlib as plt
import pickle
from abc import ABC, abstractmethod


class BaseNode(ABC):
    def __init__(self, filename) -> None:
        self.filename = filename


    def get_data(self) -> np.ndarray:
        """ Method gets data from path and return it
            :return data: pickle, data from path
        """
        with open(self.filename, 'rb') as file:
            data = pickle.load(file)
            return data


    @staticmethod
    def entropy_H2(y, n_intervals=10) -> float:
        """ Method calculates entropy for data
            :return entropy: float, shows entropy for data
        """
        
        y_min, y_max = np.min(y), np.max(y)
        interval_size = (y_max - y_min) / n_intervals
        N = len(y)
        p = []
        for i in range(n_intervals):
            interval_start = y_min + i * interval_size
            interval_end = interval_start + interval_size
            interval_count = np.sum((y >= interval_start) & (y < interval_end))
            p_interval = interval_count / N
            p.append(p_interval)
        p = np.array(p)
        p = p[p != 0]
        entropy = -np.sum(p * np.log2(p))
        return entropy

    
    @abstractmethod
    def convert_data(self):
        """ Method converts data to required type
            :return freq: np.ndarray, frequency data 
            :return SNRs: np.ndarray, SNRs data
        """
        pass


    @abstractmethod
    def run() -> None:
        """ Method executing calculation on node
            :return x_max: float, specified value of frequency
            :return plt: plot, plot that shows optimized data
            :return is_correct: bool, flag indicating whether the data is correct 
        """
        pass