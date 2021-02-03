import pandas as pd
import numpy as np
import os, sys
from werkzeug.utils import secure_filename
from flaskapp.application_logging import logger

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

fileDir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#fileDir = os.path.join(fileDir, '..')
filePath = os.path.abspath(os.path.join(fileDir, 'data/jobs.csv'))
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, filePath)
sys.path.insert(0, logPath)

# YOU JUST NEED TO CALL -  get_similar_jobs($jobID, $w_title, $w_desc, $w_skills, $num_similar_jobs)

class Similarity(object):
    def __init__(self):
        self.logger_object = logger.App_Logger()

    def preprocessSkills(self, filepath):
        f = open(logPath+"/PreProcessing_Log.txt", 'a+')
        self.logger_object.log(f, 'Data Importing - Started the started reading the data file')

        try:
            df = pd.read_csv(filepath)
            #self.logger_object.log(f, ' Successfully read the data file')
            df['Skills_str'] = df.Skills.map(lambda x: ', '.join(x))
            #self.logger_object.log(f,'Pre-Processing - Successfully completed')
            return df
            return ("Pre-Processing of Skills is Success")

        except Exception as e:
            self.logger_object.log(f, 'Exception occured in data pre-processing. Exception message:  ' + str(e))
            f.close()
            return "Error during input file pre-processing!Please check logs for details."

    def tfidf_model_skills(self, jobId, df_clustered, w_skills):
        f = open(logPath+"/tfidf_Log.txt", 'a+')
        self.logger_object.log(f, 'Skills tfidf calculation started')
        self.w_skills = w_skills
        # Skills
        try:
            tfv_skills = TfidfVectorizer(min_df=3, ngram_range=(1, 2), max_features=None, stop_words='english',
                                         strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}')
            tfv_matrix_skills = tfv_skills.fit_transform(
                df_clustered['Skills_str'])
            sigmoid_skills = sigmoid_kernel(
                tfv_matrix_skills, tfv_matrix_skills)
            jobIndex = df_clustered[df_clustered['Id'] == jobId].index[0]
            sigmoid_skills = sigmoid_skills[jobIndex]
            wtd_sigmoid_skills = w_skills * sigmoid_skills
            return (wtd_sigmoid_skills)
        except Exception as e:
            self.logger_object.log(f, 'Exception occured in tfidf calcuation of Skills. Exception message:  ' + str(e))
            f.close()
            return "Error during tfidf skills!Please check logs for details."

    def tfidf_model_desc(self, jobId, df_clustered, w_desc):
        f = open(logPath+"/tfidf_Log.txt", 'a+')
        self.logger_object.log(f, 'Desc tfidf calculation started')
        self.w_desc = w_desc
        # Description
        try:

            tfv_desc = TfidfVectorizer(min_df=3, ngram_range=(1, 3), max_features=None, stop_words='english',
                                       strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}')
            tfv_matrix_desc = tfv_desc.fit_transform(
                df_clustered['Job_description'])
            sigmoid_desc = sigmoid_kernel(tfv_matrix_desc, tfv_matrix_desc)
            jobIndex = df_clustered[df_clustered['Id'] == jobId].index[0]
            sigmoid_desc = sigmoid_desc[jobIndex]
            wtd_sigmoid_desc = w_desc * sigmoid_desc
            return (wtd_sigmoid_desc)
        except Exception as e:
            self.logger_object.log(f, 'Exception occured in tfidf calcuation of description. Exception message:  ' + str(e))
            f.close()
            return "Error during tfidf desciption!Please check logs for details."

    def tfidf_model_title(self, jobId, df_clustered, w_title):
        f = open(logPath+"/tfidf_Log.txt", 'a+')
        self.logger_object.log(f, 'title tfidf calculation started')
        self.w_title = w_title
        # Title
        try:

            tfv_title = TfidfVectorizer(min_df=1, ngram_range=(1, 2), max_features=None, stop_words='english',
                                        strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}')
            tfv_matrix_title = tfv_title.fit_transform(
                df_clustered['Job_title'])
            sigmoid_title = sigmoid_kernel(tfv_matrix_title, tfv_matrix_title)
            jobIndex = df_clustered[df_clustered['Id'] == jobId].index[0]
            sigmoid_title = sigmoid_title[jobIndex]
            wtd_sigmoid_title = w_title * sigmoid_title
            wtd_sigmoid_title
            return (wtd_sigmoid_title)
        except Exception as e:
            self.logger_object.log(f, 'Exception occured in tfidf calcuation of title. Exception message:  ' + str(e))
            f.close()
            return "Error during tfidf title!Please check logs for details."

    def get_similar_jobs(self, jobId, w_title, w_desc, w_skills, num_similar_jobs):
        f = open(logPath+"/getSimilarJobs.txt", 'a+')
        self.logger_object.log(f, 'getting similar jobs for the job ID')

        try:
            #jobId = 1737717
            #jobId = 67
            #self.jobId = jobId
            df = self.preprocessSkills(filePath)
            df_clustered = df[df['Job_cluster_id'] ==
                              df[df['Id'] == jobId].Job_cluster_id.values[0]]
            df_clustered = df_clustered.reset_index(drop=True)
            #print(df_clustered)
            jobIndex = df_clustered[df_clustered['Id'] == jobId].index[0]
            title = df_clustered[df_clustered['Id'] == jobId].Job_title
            #print(title)
            desc = df_clustered[df_clustered['Id'] == jobId].Job_description
            skills = df_clustered[df_clustered['Id'] == jobId].Skills_str

            wtd_sigmoid_title = self.tfidf_model_title(jobId, df_clustered, w_title)
            wtd_sigmoid_desc = self.tfidf_model_desc(jobId, df_clustered, w_desc)
            wtd_sigmoid_skills = self.tfidf_model_skills(jobId, df_clustered, w_skills)

            sigmoid_total = wtd_sigmoid_title + wtd_sigmoid_desc + wtd_sigmoid_skills
            #print('sigmoid',sigmoid_total)
            job_scores = sorted(list(enumerate(sigmoid_total)),
                                key=lambda x: x[1], reverse=True)
            df_indices = [i[0] for i in job_scores]

            return df_clustered['Id'].iloc[df_indices].iloc[1:(num_similar_jobs + 1)].values

        except Exception as e:
            self.logger_object.log(f, 'Exception occured in job-job recommendation. Exception message:  ' + str(e))
            f.close()
            return "Error during input file recommendation job-job!Please check logs for details."
