import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.metrics.pairwise import sigmoid_kernel
#from Application_logging.logger import App_Logger
class similarity:
    def __init__(self):
        #self.logger = App_Logger()
        pass
    def give_record(self,df,sigmoid,idx):
        try:
            self.df=df
            # The index corresponding to original_title is in idx

            # Get the pairwsie similarity scores
            self.sig_scores = list(enumerate(sigmoid[idx]))

            # Sort the freelancers
            self.sig_scores = sorted(self.sig_scores, key=lambda x: x[1], reverse=True)

            # Scores of the 10 most similar freelancers
            self.sig_scores = self.sig_scores[1:11]

            # Movie indices
            self.freelancers_indices = [i[0] for i in self.sig_scores]

            # Top 10 most similar freelacers
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'top 10 most similar freelnacers have been computed and returned as a list ')
            #file.close()

            return self.df['Freelancer_Name'].iloc[self.freelancers_indices]
        except Exception as e:
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Error %s occurred while fetching top 10 most similar freelnacers from give_record method' %e)
            #file.close()

    def find_similar_user(self,data,freelancer_name):
        """ Method Name: find_similar_user
            Description: this method will take dataframe as input and returns top 10 similar users
            Return :list of top 10 similar users
            Written by: Harsh Kumar
            Version: 1.0
            Revisions: None """
        try:
            self.df=data
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Entered into the find_similar_user method for finding the similar users')
            #file.close()

            # making the Skills feature as a string of Skills
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Started making the Skills feature as a string of Skills')
            #file.close()

            for index, row in self.df.iterrows():
                row_string = ""
                for j in row['Skills'][0:-1].split(','):
                    for i in range(0, len(j[2:-1].split(' '))):
                        row_string += j[2:-1].split(' ')[i] # combining skill like 'web application development' into
                        # single word 'webapplicationdevelopment'
                    row_string += " "
                self.df.at[index, "Modified_Skills"] = row_string
            print(self.df[['Modified_Skills']].head(2))

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Completed making the Skills feature as a string of Skills')
            #file.close()

            # converting all the letters into lowercase so that words like Java and java are considered as one word
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file, 'Started converting all the letters into lowercase such that words like Java and java are considered as one word')
            #file.close()

            self.df['Modified_Skills'] = [row['Modified_Skills'].lower() for index, row in self.df.iterrows()]
            print(self.df.Modified_Skills.iloc[0][:500])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Completed converting all the letters into lowercase word')
            #file.close()

            # Now making the 3 different features out of Location feature
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Started making the 3 different features ("City","State","Country") out of Location feature')
            #file.close()
            self.df['City'] = [row['Location'].split(',')[0].lower() for index, row in self.df.iterrows()]
            self.df['State'] = [row['Location'].split(',')[1].lower() for index, row in self.df.iterrows()]
            self.df['Country'] = [row['Location'].split(',')[2].lower() for index, row in self.df.iterrows()]

            print(self.df)
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Completed splitting the location feature into 3 different features ("City","State","Country") ')
            #file.close()
            # featurizing the Modified_Skills feature into tf-idf vectorizer
            vectorizer_skills = TfidfVectorizer()
            self.skills_tf = vectorizer_skills.fit_transform(self.df['Modified_Skills'])
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'featurized the Modified_Skills feature into tf-idf vectorizer')
            #file.close()

            # Featurizing the state feature into tf-idf vectorizer
            vec_state = TfidfVectorizer()
            self.state_tf = vec_state.fit_transform(self.df['State'])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'featurized the State feature into tf-idf vectorizer')
            #file.close()

            # Featurizing the City feature into tf-idf vectorizer
            vec_city = TfidfVectorizer()
            self.city_tf = vec_city.fit_transform(self.df['City'])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'featurized the City feature into tf-idf vectorizer')
            #file.close()

            ## Featurizing the Country feature into tf-idf vectorizer
            vec_country = TfidfVectorizer()
            self.country_tf = vec_country.fit_transform(self.df['Country'])

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'featurized the Country feature into tf-idf vectorizer')
            #file.close()

            # Droping the Location feature
            self.df = self.df.drop('Location', axis=1)
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Dropped the Location feature as it is of no use')
            #file.close()


            # Now merging all the Tf-idf features of Skills,state,City,Country

            self.final_vec = hstack((self.state_tf, self.city_tf, self.country_tf, self.skills_tf))
            print ('The shape of final tf-idf vector {}'.format(self.final_vec.shape))

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Merged all the Tf-idf features of Skills,state,City,Country into a single Tf-idf vectorizer')
            #file.close()


            #  Making the final Model
            # Compute the sigmoid kernel
            self.sig = sigmoid_kernel(self.final_vec, self.final_vec)

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Computed the sigmoid kernel for finding the similar users')
            #file.close()


            # renaming the column Freelancer Name as FreeLancer_Name
            self.df.rename(columns={"Freelancer Name": "Freelancer_Name"}, inplace=True)

            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                        'Renamed the column Freelancer Name as FreeLancer_Name')
            #file.close()

            # Reverse mapping of indices and Freelancers name
            self.indices = pd.Series(self.df.index, index=self.df['Freelancer_Name']).drop_duplicates()

            print(self.indices)

            # Testing our content-based recommendation system with the Freelancer Name NIX Solutions Ltd
            #b=similarity()
            self.similiar_users_list=self.give_record(self.df,self.sig,self.indices[freelancer_name]) # The index corresponding to original_title is in self.indices[freelancer_name]
            print(self.similiar_users_list)
            return self.similiar_users_list
        except Exception as e:
            #file = open('logs/User_similarity_logs.txt', 'a+')
            #self.logger.log(file,
                            'Error %s occurred while retirveing the similar freelancers' %e)
            #file.close()















