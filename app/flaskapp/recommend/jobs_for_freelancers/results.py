from flaskapp.recommend.jobs_for_freelancers import recommend_jobs as jobs

def getResults(flId, n):
    #generate top matching jobs for a freelancer
    similarities_on = ['Job_description', 'Job_title', 'Skills']
    weights = [30, 20, 50]
    freelancer_no = flId
    job_recommendations = jobs.Implementation(freelancer_no, similarities_on, weights)

    results = job_recommendations.pick_top_n(n).tolist()

    return results




