from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import case
from flaskapp import db
from flaskapp.models import Job, Profile, User
from flaskapp.jobs.forms import JobPostForm
#from flaskapp.recommend.freelancers_for_jobs import results
from flaskapp.recommend.final_freelancers import results
from flaskapp.segment.predict.for_new_job.results import predictSegment
from flaskapp.recommend.final_freelancers.bucketing import bucket
from flaskapp.recommend.final_freelancers.rank_invited_freelancers.get_ranked_list import rankInvitedFls
from flaskapp.data_updater import update_data as update_data
import math
from sqlalchemy import case
from time import time
import gc

jobs = Blueprint('jobs', __name__)

dataUpdater = update_data.Data_Updater()

@jobs.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobPostForm()
    if form.validate_on_submit():
        job_cluster_id = predictSegment(form.min_budget.data, form.category.data)
        skills = form.skills.data if isinstance(form.skills.data, list) else form.skills.data.split(', ')
        skills_list = []
        for skill in skills:
            skills_list.append(skill.capitalize())
        skills_list = str(skills_list)
        job = Job(title=form.title.data, description=form.description.data, skills=skills_list, category=form.category.data, min_budget=form.min_budget.data, job_cluster_id=job_cluster_id, user=current_user)
        db.session.add(job)
        db.session.commit()
        job = Job.query.filter_by(id=job.id).first_or_404()
        dataUpdater.add_job(job)
        #dataUpdater.close_logs()
        print('Your job post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_job.html', title='Create New Job Post', form=form, legend='Create New Job Post', purpose='create')


@jobs.route('/employer_user/<string:userid>')
def job_posts(userid):
  #page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(id=userid).first_or_404()
  jobs = Job.query.filter_by(user=user)\
                    .order_by(Job.date.desc())
  #                  .paginate(page=page, per_page=5)
  #print('Job listings: ', jobs)
  return render_template('jobs.html', jobs=jobs, user=user)


@jobs.route('/job/<int:job_id>', )
def job(job_id):
    gc.collect()
    job = Job.query.get_or_404(job_id)

    #no of recommendations in the final listing 
    N = 30
    #no of recommendations per page
    n = 10

    #respective percentage/proportion of recommendation to be shown respectively from buckets of hired, invited and content-based freelancers
    w_hired = 4
    w_quoted = 3
    w_invited = 1
    w_content = 2
    
    weights_tuple = (w_hired, w_quoted, w_invited, w_content)
    fls_hired, fls_quoted, fls_invited, fls_content, similar_jobs = results.getResults(job_id, N)

    for id in similar_jobs:
        pass
        #print(id, Job.query.filter_by(id=int(id)).first().skills)
    users_hired = []
    users_quoted = []
    users_invited = []
    bucket_hired = []
    bucket_quoted = []
    bucket_invited = []
    bucket_invited_ids = []
    bucket_invited_ranked_ids = []
    bucket_invited_ranked = []
    bucket_content = []

    for fl in fls_hired:
        if fl:
            if User.query.filter_by(username=fl).first():
                users_hired.append(User.query.filter_by(username=fl).first())    
    for user in users_hired:
        bucket_hired.append(user.profiles[0])

    for fl in fls_quoted:
        if fl:
            if User.query.filter_by(username=fl).first():
                users_quoted.append(User.query.filter_by(username=fl).first())
    for user in users_quoted:
        if user in users_hired:
            continue
        else:
            bucket_quoted.append(user.profiles[0])
    

    for fl in fls_invited:
        if fl:
            if User.query.filter_by(username=fl).first():
                users_invited.append(User.query.filter_by(username=fl).first())
    for user in users_invited:
        if ((user in users_hired) or (user in users_quoted)):
            continue
        else:
            bucket_invited.append(user.profiles[0])

    '''
    bucket_invited_ids = [profile.id for profile in bucket_invited if profile]
    print('bucket_invited_ids: ', bucket_invited_ids)
    if len(bucket_invited_ids) == 0:
        pass
    else:
        bucket_invited_ranked_ids = rankInvitedFls(job_id, bucket_invited_ids)
    
    bucket_invited_ranked = [Profile.query.filter_by(id=int(id)).first_or_404() for id in bucket_invited_ranked_ids]
    print('bucket_invited_ranked_ids: ',bucket_invited_ranked_ids,'\n\n')
    '''
    print('fl_content: ',fls_content)
    for id in fls_content:
        if (id in [profile.id for profile in bucket_hired]) or (id in [profile.id for profile in bucket_invited]) or (id in [profile.id for profile in bucket_quoted]):
            continue
        else:
            bucket_content.append(Profile.query.filter_by(id=int(id)).first_or_404())
    
    pop = len(bucket_hired) + len(bucket_quoted) + len(bucket_invited)
    bucket_content = bucket_content[:-pop or None]
    #print('bucket_content: ',bucket_content)

    fls_tuple = (bucket_hired, bucket_quoted, bucket_invited, bucket_content)
    test = bucket_hired+bucket_invited+bucket_content
    for profile in test:
        pass
        #print(profile.user.username)
    #page = request.args.get('page', 1, type=int)
    final_list = bucket(N, n, fls_tuple, weights_tuple)
    #print('Final List: ',final_list)
    final_list_ids = [profile.id for profile in final_list]
    #print('Final List ids: ', final_list_ids)
    ordering = case(
        {id: index for index, id in enumerate(final_list_ids)},
        value=Profile.id
    )
    page = request.args.get('page', 1, type=int)
    rec_profiles = Profile.query.filter(Profile.id.in_(final_list_ids)).order_by(ordering).paginate(page=page, per_page=n)
    #print('Rec Profiles: ',rec_profiles)
    gc.collect()
    return render_template('job.html', job=job, title=job.title, description=job.description, rec_profiles=rec_profiles)


@jobs.route('/job/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user != current_user:
        abort(403)
    form = JobPostForm()
    if form.validate_on_submit():
        job.title = form.title.data
        skills = form.skills.data if isinstance(form.skills.data, list) else form.skills.data.split(', ')
        skills_list = []
        for skill in skills:
            skills_list.append(skill.capitalize())
        skills_list = str(skills_list)
        job.skills = skills_list
        job.description = form.description.data
        job.category = form.category.data
        job.min_budget = form.min_budget.data
        job_cluster_id = predictSegment(form.min_budget.data, form.category.data)
        job.job_cluster_id = job_cluster_id
        db.session.commit()
        job = Job.query.get_or_404(job_id)
        print('Min Budget: ',job.min_budget)
        print('Job Cluster: ',job.job_cluster_id)
        dataUpdater.update_job(job)
        flash('Your job post has been updated', 'success')
        return redirect(url_for('jobs.job', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.skills.data = job.skills
        form.description.data = job.description
        form.category.data = job.category
        form.min_budget.data = job.min_budget
    return render_template('create_job.html', title='Update Job Post', form=form, legend='Update Job Post', purpose='update')


@jobs.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user != current_user:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    dataUpdater.delete_job(job)
    #dataUpdater.resetJobIds()
    flash('The job post has been deleted', 'success')
    return redirect(url_for('main.home'))
