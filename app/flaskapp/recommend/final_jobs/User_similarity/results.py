from flaskapp.flfl.User_similarity.freelancerSimilarity import similarity


from flaskapp.data_reader import read_data as rd
dataReader = rd.Data_Reader()
jobs = dataReader.get_jobs()
freelancers = dataReader.get_profiles()

def getSimilarFLs(flId)
    b=similarity()
    return b.find_similar_user(freelancers, flId)
