from flask import Blueprint
from flask import render_template, request, flash
from flask_login import current_user
from flaskapp import db
import pandas as pd
from flaskapp.models import Job, Profile
from flaskapp.recommend.to_home_search.freelancers import results as fl_home_results
from flaskapp.recommend.to_home_search.jobs import results as job_home_results
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.usertype == 'employer':
            jobs = Job.query.filter_by(user=current_user)\
                    .order_by(Job.date.desc())
            return render_template('jobs.html', jobs=jobs, title='Home')
        else:
            profiles = Profile.query.filter_by(user=current_user)\
                    .order_by(Profile.location.desc())
            return render_template('profiles.html', profiles=profiles, title='Home')
    return render_template('home.html', title='Home')


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/demo")
def demo():
    return render_template('demo.html', title='Demo Guide')

#endpoint for search
@main.route('/search', methods=['GET', 'POST'])
def search():
    #query = Job.query
    #q = query.statement.compile(dialect=db.session.bind.dialect)
    #print(q)
    #jobs = pd.read_sql(q, db.session.bind)
    #print(jobs)
    if request.method == "POST":
        s_query = request.form['search']
        search_for = request.form['searchtype']
        rec_jobs = []
        rec_profiles = []
        if (search_for == 'freelancer'):
            rec_profiles_ids = fl_home_results.getResults(s_query, 10)
            print(rec_profiles_ids)
            for id in rec_profiles_ids:
                rec_profiles.append(Profile.query.filter_by(id=int(id)).first_or_404())
        elif (search_for == 'job'):
            rec_jobs_ids = job_home_results.getResults(s_query, 10)
            print(rec_jobs_ids)
            for id in rec_jobs_ids:
                rec_jobs.append(Job.query.filter_by(id=int(id)).first_or_404())

        return render_template('search.html', rec_profiles=rec_profiles, rec_jobs=rec_jobs)
        
    return render_template('search.html')
