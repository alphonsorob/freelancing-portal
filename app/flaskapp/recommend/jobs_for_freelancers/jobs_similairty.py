import pandas as pd
import string
from stop_words import get_stop_words
from gensim import corpora
from gensim import models
from gensim import similarities
from flask import Blueprint
from flaskapp.application_logging import logger
from flaskapp.data_reader import read_data as rd
#from flaskapp.database_reader import read_db as rd
import os, gc, sys, tracemalloc


fileDir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#fileDir = os.path.join(fileDir, '..')
dataPath = os.path.abspath(os.path.join(fileDir, 'data'))
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, dataPath)
sys.path.insert(0, logPath)


stop_words = get_stop_words('english')


class Similarity(object):
    classObjects = []

    def __init__(self, corpusFeature):
        self.__class__.classObjects.append(self)
        #self.processLog = open(os.path.join(logPath, 'data_read_logs/UFL_Similarity_Process_Log.txt'), 'a+')
        #self.errorLog = open(os.path.join(logPath, 'data_read_logs/UFL_Similarity_Error_Log.txt'), 'a+')
        self.log_writer = logger.App_Logger()
        self.jobs, self.freelancers = self.importDataFrames()
        self.corpusFeature = corpusFeature
        self.dictionary = self.getDictionary()
        self.bowCorpus = self.generate_bow()
        self.tfidf, self.similaritiesModel = self.train_model()

    #import dataframe from csv
    def importDataFrames(self):
        dataReader = rd.Data_Reader()
        jobs = dataReader.get_jobs()
        freelancers = dataReader.get_profiles()
        dataReader.close_logs()
        return jobs, freelancers
    
    #preprocessing
    def preProcess(self, skills):
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
    
    #create dictionary
    def getDictionary(self):

        def generate_masterskills():
            masterSkills = []
            for skills in self.freelancers['Skills']:
                masterSkills.append(self.preProcess(skills))
            return masterSkills


        masterSkills = generate_masterskills()


        def generate_dictionary():
            dictionary = corpora.Dictionary(list(masterSkills))
            return dictionary
        
        gc.collect()
        return generate_dictionary()

    #recommendation methods

    def generate_bow(self):
        bowCorpus = [self.dictionary.doc2bow(self.preProcess(self.jobs.loc[jobID, self.corpusFeature]))
                          for jobID in self.jobs.index.values]
        return bowCorpus

    def train_model(self):
        tfidf = models.TfidfModel(self.bowCorpus)
        similaritiesModel = similarities.SparseMatrixSimilarity(tfidf[self.bowCorpus],
                                                                     num_features=len(self.dictionary))
        return tfidf, similaritiesModel

    def n_similar_listings(self, freelancerNo):
        queryDocument = self.preProcess(self.freelancers.iloc[self.freelancers[self.freelancers['Id'] == freelancerNo].index]['Skills'].values[0])
        queryBow = self.dictionary.doc2bow(queryDocument)
        sims = self.similaritiesModel[self.tfidf[queryBow]]

        #results = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:n]
        gc.collect()

        return pd.DataFrame(enumerate(sims), columns=['index', 'score_'+self.corpusFeature])

    def getObjects(self):
        return Similarity.classObjects





