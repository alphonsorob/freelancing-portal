import pandas as pd
import re, string, gc
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.metrics.pairwise import sigmoid_kernel
#from Application_logging.logger import App_Logger
class Similarity():
    def __init__(self):
        #self.logger = App_Logger()
        pass
    def give_record(self,df,sigmoid,idx):
        try:
            df=df
            # The index corresponding to original_title is in idx

            # Get the pairwsie similarity scores
            sig_scores = list(enumerate(sigmoid[idx]))

            # Sort the freelancers
            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

            # Scores of the 10 most similar freelancers
            sig_scores = sig_scores[1:11]

            # Movie indices
            freelancers_indices = [i[0] for i in sig_scores]

            # Top 10 most similar freelacers
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'top 10 most similar freelnacers have been computed and returned as a list ')
            #file.close()
            gc.collect()
            return df['Id'].iloc[freelancers_indices].tolist()
        except Exception as e:
            pass
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Error %s occurred while fetching top 10 most similar freelnacers from give_record method' %e)
            #file.close()

    def find_similar_user(self,data,freelancer_id):
        try:
            df=data
            print(df)
            print(freelancer_id)
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Entered into the find_similar_user method for finding the similar users')
            #file.close()

            # making the Skills feature as a string of Skills
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Started making the Skills feature as a string of Skills')
            #file.close()
            
            for index, row in df.iterrows():
                row_string = ""
                for j in row['Skills'][0:-1].split(','):
                    for i in range(0, len(j[2:-1].split(' '))):
                        row_string += j[2:-1].split(' ')[i] # combining skill like 'web application development' into
                        # single word 'webapplicationdevelopment'
                    row_string += " "
                df.at[index, "Modified_Skills"] = row_string
            
            #print(df['Modified_Skills'])
            
            #print(df[['Modified_Skills']].head(2))

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Completed making the Skills feature as a string of Skills')
            #file.close()

            # converting all the letters into lowercase so that words like Java and java are considered as one word
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Started converting all the letters into lowercase such that words like Java and java are considered as one word')
            #file.close()

            df['Modified_Skills'] = [row['Modified_Skills'].lower() for index, row in df.iterrows()]
            #print(df['Modified_Skills'])
            #print(df.Modified_Skills.iloc[0][:500])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Completed converting all the letters into lowercase word')
            #file.close()

            # Now making the 3 different features out of Location feature
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Started making the 3 different features ("City","State","Country") out of Location feature')
            #file.close()
            df['City'] = [row['Location'].split(',')[0].lower() for index, row in df.iterrows()]
            df['State'] = [row['Location'].split(',')[1].lower() for index, row in df.iterrows()]
            df['Country'] = [row['Location'].split(',')[2].lower() for index, row in df.iterrows()]
            print(df['Country'])
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Completed splitting the location feature into 3 different features ("City","State","Country") ')
            #file.close()
            # featurizing the Modified_Skills feature into tf-idf vectorizer
            vectorizer_skills = TfidfVectorizer()
            skills_tf = vectorizer_skills.fit_transform(df['Modified_Skills'])
            #print(skills_tf)
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'featurized the Modified_Skills feature into tf-idf vectorizer')
            #file.close()

            # Featurizing the state feature into tf-idf vectorizer
            vec_state = TfidfVectorizer()
            state_tf = vec_state.fit_transform(df['State'])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'featurized the State feature into tf-idf vectorizer')
            #file.close()

            # Featurizing the City feature into tf-idf vectorizer
            vec_city = TfidfVectorizer()
            city_tf = vec_city.fit_transform(df['City'])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'featurized the City feature into tf-idf vectorizer')
            #file.close()

            ## Featurizing the Country feature into tf-idf vectorizer
            vec_country = TfidfVectorizer()
            country_tf = vec_country.fit_transform(df['Country'])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'featurized the Country feature into tf-idf vectorizer')
            #file.close()

            # Droping the Location feature
            df = df.drop('Location', axis=1)
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Dropped the Location feature as it is of no use')
            #file.close()


            # Now merging all the Tf-idf features of Skills,state,City,Country

            final_vec = hstack((state_tf, city_tf, country_tf, skills_tf))
            
            #print ('The shape of final tf-idf vector {}'.format(final_vec.shape))

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Merged all the Tf-idf features of Skills,state,City,Country into a single Tf-idf vectorizer')
            #file.close()


            #  Making the final Model
            # Compute the sigmoid kernel
            sig = sigmoid_kernel(final_vec, final_vec)
            print(sig)
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Computed the sigmoid kernel for finding the similar users')
            #file.close()


            # renaming the column Freelancer Name as FreeLancer_Name
            df.rename(columns={"Freelancer Name": "Freelancer_Name"}, inplace=True)

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Renamed the column Freelancer Name as FreeLancer_Name')
            #file.close()

            # Reverse mapping of indices and Freelancers name
            print('Reached')
            df.reset_index(inplace=True, drop=True)
            print('Reached Next')
            indices = pd.Series(df.index, index=df['Id']).drop_duplicates()     
            print('Reached Next Next')       
            print('Test: ',sig[indices[freelancer_id]])

            # Testing our content-based recommendation system with the Freelancer Name NIX Solutions Ltd
            #b=similarity()
            similiar_users_list=self.give_record(df,sig,indices[freelancer_id]) # The index corresponding to original_title is in indices[freelancer_name]
            #print(similiar_users_list)
            gc.collect()
            return similiar_users_list
        except Exception as e:
            pass
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,'Error %s occurred while retirveing the similar freelancers' %e)
            #file.close()
