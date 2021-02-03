import pandas as pd
import os
from flask import current_App
from flaskapp import db
from flaskapp.models import Job


def addJobsCSV():
    file_path = os.path.join(current_app.root_path, 'jobs.csv')
    jobs = pd.read_csv(file_path)
    for index, row in jobs.iterrows():
        j = Job(title=row['title'], description=row['description'], skills=row['skills'], user_id=row['user_id'])
        db.session.add(j)
    db.session.commit()

# addJobssCSV()
