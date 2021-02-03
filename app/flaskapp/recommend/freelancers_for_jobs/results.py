from flaskapp.recommend.freelancers_for_jobs import recommend_freelancers as freelancers

def getResults(jobId, n):

    #generate top matching freelancers for a job
    #method 1
    #similarities_on = ['Job_description', 'Job_title', 'Skills']
    #weights = [30, 20, 50]

    #method 2
    similarities_on = ['Skills']
    weights = [30, 20, 50]
    job_id = jobId
    freelancer_recommendations = freelancers.Implementation(job_id, similarities_on, weights)
    return freelancer_recommendations.pick_top_n(n)




