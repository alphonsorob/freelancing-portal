from flaskapp.recommend.to_home_search.freelancers import freelancers_similairty as UFL
from flaskapp.application_logging import logger
from flaskapp.data_reader import read_data as rd
import pandas as pd
from functools import reduce
import numpy as np
import os, sys


fileDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#fileDir = os.path.join(fileDir, '..')
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, logPath)


class Implementation(object):
    def __init__(self, searchInput, features):
        self.processLog = open(os.path.join(logPath, 'data_read_logs/Prediction_Log.txt'), 'a+')
        self.errorLog = open(os.path.join(logPath, 'data_read_logs/Error_Log.txt'), 'a+')
        self.log_writer = logger.App_Logger()
        self.features = features
        self.text = searchInput

    def generate_models(self):
        similarities = []
        for metric in self.features:
            similarities.append(UFL.Similarity(self.text, metric).n_similar_listings())
        if len(self.features) > 1:
            resultsCombo = reduce(lambda x, y: pd.merge(x, y, on='index', how='left'), similarities)
        else:
            resultsCombo = similarities[0]
        return resultsCombo

    def pick_top_n(self, n):
        dataReader = rd.Data_Reader()
        freelancers = dataReader.get_profiles()
        resultsCombo = self.generate_models()
        top_n_fls = resultsCombo.sort_values('score_Skills', ascending=False)[:n]['index'].values
        top_n_fls = freelancers.iloc[top_n_fls, :]['Id'].values
        #print(resultsCombo.sort_values('score_Skills', ascending=False))
        return top_n_fls


