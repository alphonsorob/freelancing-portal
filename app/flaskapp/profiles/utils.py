import pandas as pd
import os
from flask import current_App
from flaskapp import db
from flaskapp.models import Profile


def addProfilesCSV():
    file_path = os.path.join(current_app.root_path, 'freelancers.csv')
    profiles = pd.read_csv(file_path)
    for index, row in profiles.iterrows():
        p = Profile(location=row['location'], rate=row['rate'], skills=row['skills'], user_id=row['user_id'])
        db.session.add(j)
    db.session.commit()

# addProfilesCSV()
