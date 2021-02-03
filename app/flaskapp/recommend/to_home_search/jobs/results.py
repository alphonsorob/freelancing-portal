from flaskapp.recommend.to_home_search.jobs import recommend_jobs as jobs

def getResults(searchInput, n):
    #generate top matching jobs for a freelancer
    similarities_on = ['Job_description', 'Job_title', 'Skills']
    weights = [30, 20, 50]
    job_recommendations = jobs.Implementation(searchInput, similarities_on, weights)
    return job_recommendations.pick_top_n(n)




