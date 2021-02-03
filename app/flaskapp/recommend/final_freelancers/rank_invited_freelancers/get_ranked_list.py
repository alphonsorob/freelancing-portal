from flaskapp.recommend.final_freelancers.rank_invited_freelancers import recommend_freelancers as freelancers



def rankInvitedFls(job_id, fls_invited_ids):
    # rank these fls based on content based matching with main job id
    similarities_on = ['Skills']
    weights = [30, 20, 50]
    job_id = job_id
    freelancer_recommendations = freelancers.Implementation(job_id, similarities_on, weights, fls_invited_ids)
    n = len(fls_invited_ids)
    return freelancer_recommendations.pick_top_n()