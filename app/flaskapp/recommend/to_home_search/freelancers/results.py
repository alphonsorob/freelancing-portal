from flaskapp.recommend.to_home_search.freelancers import recommend_freelancers as freelancers

def getResults(searchInput, n):

    #generate top matching freelancers for a job
    #method 1
    #similarities_on = ['Job_description', 'Job_title', 'Skills']
    #weights = [30, 20, 50]

    #method 2
    similarities_on = ['Skills']
    #weights = [30, 20, 50]
    #job_id = jobId
    freelancer_recommendations = freelancers.Implementation(searchInput, similarities_on)
    return freelancer_recommendations.pick_top_n(n)




