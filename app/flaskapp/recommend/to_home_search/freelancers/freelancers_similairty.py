import pandas as pd
import string
from flask import current_app
from stop_words import get_stop_words
from gensim import corpora
from gensim import models
from gensim import similarities
from flaskapp.application_logging import logger
from flaskapp.data_reader import read_data as rd
#from flaskapp.database_reader import read_db as rd
import os
import sys


fileDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#fileDir = os.path.join(fileDir, '..')
dataPath = os.path.abspath(os.path.join(fileDir, 'data'))
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, dataPath)
sys.path.insert(0, logPath)


stop_words = get_stop_words('english')


def preProcess(skills):
    if isinstance(skills, list):
        s = ' '.join(skills)
    else:
        s = skills
    table = str.maketrans(dict.fromkeys(string.punctuation))
    new_s = s.translate(table)
    new_s = new_s.replace('\n', ' ')
    new_s = new_s.replace('  ', ' ')
    new_s = [x for x in new_s.lower().split() if len(x) > 1 and x not in stop_words]
    return new_s


class Similarity(object):
    def __init__(self, searchInput, feature):
        self.processLog = open(os.path.join(logPath, 'data_read_logs/UFL_Similarity_Process_Log.txt'), 'a+')
        self.errorLog = open(os.path.join(logPath, 'data_read_logs/UFL_Similarity_Error_Log.txt'), 'a+')
        self.log_writer = logger.App_Logger()
        self.text = searchInput
        self.jobs = ''
        self.freelancers = ''
        self.importDataFrames()
        self.bowCorpus = []
        self.feature = feature
        self.generate_dictionary()
        self.generate_bow()
        self.train_model()

    def importDataFrames(self):
        dataReader = rd.Data_Reader()
        self.jobs = dataReader.get_jobs()
        self.freelancers = dataReader.get_profiles()
        dataReader.close_logs()
    
    def generate_dictionary(self):
        #method 2
        s = preProcess(self.text)
        self.dictionary = corpora.Dictionary([s])
        #print(len(self.dictionary))
        #method 1
        #self.dictionary = corpora.Dictionary([preProcess(jobs[jobs['Job_id'] == self.job_id][self.feature].values[0])])

    def generate_bow(self):
        self.bowCorpus = [self.dictionary.doc2bow(preProcess(self.freelancers.loc[freelancerID, 'Skills']))
                          for freelancerID in self.freelancers.index.values]
        #print(self.bowCorpus)
    def train_model(self):
        self.tfidf = models.TfidfModel(self.bowCorpus)
        self.similaritiesModel = similarities.SparseMatrixSimilarity(self.tfidf[self.bowCorpus],
                                                                     num_features=len(self.dictionary))

    def n_similar_listings(self):
        query_document = preProcess(self.text)
        query_bow = self.dictionary.doc2bow(query_document)
        sims = self.similaritiesModel[self.tfidf[query_bow]]
        return pd.DataFrame(enumerate(sims), columns=['index', 'score_'+self.feature])

