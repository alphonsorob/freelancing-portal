from flaskapp.recommend.final_jobs.freelancerSimilarity import Similarity
import gc

def getSimilarFLs(flId, clusterId):
    from flaskapp.data_reader import read_data as rd
    dataReader = rd.Data_Reader()
    jobs = dataReader.get_jobs()
    freelancers = dataReader.get_profiles()

    print('All Freelancers: ', freelancers)
    freelancers_from_own_cluster = freelancers.loc[freelancers['Profile Cluster Id'] == clusterId].copy()
    print('Freelancer Cluster: ',clusterId)
    print('Cluster Fls: ',freelancers_from_own_cluster)
    similarity = Similarity()
    similar_fls = similarity.find_similar_user(freelancers_from_own_cluster, flId)
    print('Similar FLs from this Cluster: ',similar_fls)
    #similar_fls_df = freelancers[freelancers['Id'].isin(similar_fls)]
    #print(similar_fls_df['Freelancer Name'])
    gc.collect()
    return similar_fls
