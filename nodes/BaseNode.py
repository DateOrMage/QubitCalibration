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
    def calculate_threshold(error_good, std_dev):
        """ Method calculates required threshold
            :return threshold: float, required threshold
        """
        threshold = error_good + std_dev
        return threshold

    @staticmethod
    def error_based_on_range(data):
        """ Method calculates the error threshold
            :param data: np.ndarray
            :return mean_error: float, required sigma
        """ 
        normalized_data = (data - min(data)) / (max(data) - min(data))
        differences = normalized_data[1:] - normalized_data[:-1]
        mean_error = sum(abs(differences)) / len(differences)
        return mean_error

    
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