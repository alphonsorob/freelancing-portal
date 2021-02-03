from flaskapp.recommend.final_freelancers.rank_invited_freelancers import freelancers_similairty as UFL
from flaskapp.application_logging import logger
import pandas as pd
from functools import reduce
import numpy as np
import os, sys


fileDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#fileDir = os.path.join(fileDir, '..')
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, logPath)


class Implementation(object):
    def __init__(self, job_id, features, weights, fl_ids):
        self.processLog = open(os.path.join(logPath, 'data_read_logs/Prediction_Log.txt'), 'a+')
        self.errorLog = open(os.path.join(logPath, 'data_read_logs/Error_Log.txt'), 'a+')
        self.log_writer = logger.App_Logger()
        self.features = features
        self.weights = weights
        self.job_id = job_id
        self.fl_ids = fl_ids

    def generate_models(self):
        similarities = []
        for metric in self.features:
            similarities.append(UFL.Similarity(self.job_id, metric, self.fl_ids).n_similar_listings())
        if len(self.features) > 1:
            resultsCombo = reduce(lambda x, y: pd.merge(x, y, on='index', how='left'), similarities)
        else:
            resultsCombo = similarities[0]
        return resultsCombo

    def pick_top_n(self):
        resultsCombo = self.generate_models()
        #print('ResultsCombo: ', resultsCombo)
        if len(self.features) > 1:
            resultsCombo['finalScore'] = (resultsCombo.iloc[:,-len(self.weights):].values*self.weights).sum(axis = 1)
            #top_n_jobs = resultsCombo.sort_values('finalScore', ascending=False)[:n]['index'].values+1
            top_n_jobs = resultsCombo.sort_values('score_Skills', ascending=False)['index'].values+1
            #print(top_n_jobs)
        else:
            #top_n_jobs = resultsCombo.sort_values('score_Skills', ascending=False)[:n]['index'].values+1
            top_n_jobs = resultsCombo.sort_values('score_Skills', ascending=False)['index'].values+1
            #print(top_n_jobs)
            #top_n_jobs = temp[temp['index'].isin(self.fl_ids)][:n]['index'].values+1
            #print(resultsCombo.sort_values('score_Skills', ascending=False))
        return top_n_jobs


