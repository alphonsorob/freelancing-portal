#import ufl_similairty as UFL
from flaskapp.recommend.jobs_for_freelancers import jobs_similairty as UFL
from flaskapp.application_logging import logger
import pandas as pd
from functools import reduce
from flaskapp.data_reader import read_data as rd
import os, sys, gc, tracemalloc


fileDir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#fileDir = os.path.join(fileDir, '..')
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, logPath)


class Implementation(object):
    def __init__(self, freelancerNo, similaritiesOn, weights):
        #self.processLog = open(os.path.join(logPath, 'data_read_logs/Prediction_Log.txt'), 'a+')
        #self.errorLog = open(os.path.join(logPath, 'data_read_logs/Error_Log.txt'), 'a+')
        self.log_writer = logger.App_Logger()
        self.similritiesOn = similaritiesOn
        self.weights = weights
        self.freelancerNo = freelancerNo

    def generate_models(self):
        similarities = []
        for metric in self.similritiesOn:
            x = UFL.Similarity(metric).n_similar_listings(self.freelancerNo)
            similarities += [x]
            del x
        
        if len(self.similritiesOn) > 1:
            resultsCombo = reduce(lambda x, y: pd.merge(x, y, on='index', how='left'), similarities)
        else:
            resultsCombo = similarities
        del similarities

        gc.collect()
        return resultsCombo

    def pick_top_n(self, n):
        dataReader = rd.Data_Reader()
        jobs = dataReader.get_jobs()
        resultsCombo = self.generate_models()
            
        resultsCombo['finalScore'] = (resultsCombo.iloc[:,-len(self.weights):].values*self.weights).sum(axis = 1)

        top_n_jobs = resultsCombo.sort_values('finalScore', ascending=False)[:n]['index'].values
        top_n_jobs = jobs.iloc[top_n_jobs, :]['Id'].values
        del resultsCombo
        gc.collect()

        return top_n_jobs

