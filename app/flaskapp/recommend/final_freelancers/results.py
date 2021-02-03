from flaskapp.recommend.final_freelancers.jobSimilarity import Similarity
from flaskapp.recommend.freelancers_for_jobs import recommend_freelancers as freelancers

import pandas as pd 
import string
import os, sys


fileDir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#fileDir = os.path.join(fileDir, '..')
filePath = os.path.abspath(os.path.join(fileDir, 'data/jobs.csv'))
logPath = os.path.abspath(os.path.join(fileDir, 'logs'))
sys.path.insert(0, filePath)
sys.path.insert(0, logPath)
jobs_df = pd.read_csv(filePath)


def unamesFromLinks(links):
    #print('inner-called')
    #print(links)
    if isinstance(links, list):
        s = ' '.join(links)
    else:
        s = links
    table = str.maketrans(dict.fromkeys(string.punctuation))
    new_s = s.translate(table)
    #new_s = new_s.replace('\n', ' ')
    #new_s = new_s.replace('  ', ' ')
    s = [x for x in s.lower().split() if len(x) > 1]
    sub = []
    for i in s:
        if ('[' in i):
            sub.append(i[35:-2])
        elif (']' in i):
            sub.append(i[34:-2])
        else:
            sub.append(i[34:-2])
    return sub


def getInvitedFls(jobId):
    #print('outer-called')
    links = list(jobs_df['Link_of_invited_freelancers'].values)[jobId-1]
    #print(links)      
    return unamesFromLinks(links)

def getQuotedFls(jobId):
        #print('outer-called')
        links = list(jobs_df['Link_of_quoters'].values)[jobId-1]
        #print(links)        
        return unamesFromLinks(links)

def getHiredFls(jobId):
        #print('outer-called')
        links = list(jobs_df['Link_of_hired_freelancers'].values)[jobId-1]
        #print(links)        
        return unamesFromLinks(links)
    

def getResults(jobId, n):
    #running job to job similarity  
    similarity = Similarity()
    similar_jobs = similarity.get_similar_jobs(jobId, 1, 1, 1, 10)
    #print('Similar_Jobs: ',similar_jobs)
    fls_invited = []
    fls_hired = []
    fls_quoted = []

    #generate bucket 1 and 2 of freelancers based on job-job similarity
    for job in similar_jobs:
        fls_hired += getHiredFls(job)
        fls_hired = [x for x in fls_hired if x]
        fls_invited += getInvitedFls(job)
        fls_invited = [x for x in fls_invited if x]
        fls_quoted += getQuotedFls(job)
        fls_quoted = [x for x in fls_quoted if x]
    
    #generate bucket 3 from cotent-based matching
    similarities_on = ['Skills']
    weights = [30, 20, 50]
    freelancer_recommendations = freelancers.Implementation(jobId, similarities_on, weights)
    fls_content = freelancer_recommendations.pick_top_n(n)
    
    return fls_hired, fls_quoted, fls_invited, fls_content, similar_jobs




