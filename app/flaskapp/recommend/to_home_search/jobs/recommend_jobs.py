#import ufl_similairty as UFL
from flaskapp.recommend.to_home_search.jobs import jobs_similairty as UFL
from flaskapp.application_logging import logger
from flask import current_app
from flaskapp.models import Job, Profile, User
import pandas as pd
from functools import reduce
from flaskapp.data_reader import read_data as rd
import os, sys


#app = current_app()
'''
app_context = app.app_context()
app_context.push()
query = Job.query
q = query.statement.compile(dialect=db.session.bind.dialect)
print(q)
app_context.pop()
'''

fileDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#fileDir = os.path.join(fileDir, '..')
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, logPath)


class Implementation(object):
    def __init__(self, searchInput, similaritiesOn, weights):
        self.processLog = open(os.path.join(logPath, 'data_read_logs/Prediction_Log.txt'), 'a+')
        self.errorLog = open(os.path.join(logPath, 'data_read_logs/Error_Log.txt'), 'a+')
        self.log_writer = logger.App_Logger()
        self.similritiesOn = similaritiesOn
        self.weights = weights
        self.text = searchInput

    def generate_models(self):
        similarities = []
        for metric in self.similritiesOn:
            similarities.append(UFL.Similarity(metric).n_similar_listings(self.text))
        if len(self.similritiesOn) > 1:
            resultsCombo = reduce(lambda x, y: pd.merge(x, y, on='index', how='left'), similarities)
        else:
            resultsCombo = similarities
        return resultsCombo

    def pick_top_n(self, n):
        dataReader = rd.Data_Reader()
        jobs = dataReader.get_jobs()
        resultsCombo = self.generate_models()
        resultsCombo['finalScore'] = (resultsCombo.iloc[:,-len(self.weights):].values*self.weights).sum(axis = 1)
        top_n_jobs = resultsCombo.sort_values('finalScore', ascending=False)[:n]['index'].values
        top_n_jobs = jobs.iloc[top_n_jobs, :]['Id'].values
        #top_n_jobs = jobs.iloc[top_n_jobs]['Id'].values
        return top_n_jobs

