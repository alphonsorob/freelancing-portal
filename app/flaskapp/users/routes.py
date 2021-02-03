from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User, Job, Profile
from flaskapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskapp.users.utils import save_picture, send_reset_email
from flaskapp.data_updater import update_data as update_data
import os, sys
users = Blueprint('users', __name__)

dataUpdater = update_data.Data_Updater()

@users.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    usertype = form.usertype.data
    firstname = form.firstname.data
    lastname = form.lastname.data
    username = '-'.join([firstname.replace(' ', '-'), lastname.replace(' ', '-')]).lower() if lastname else firstname.replace(' ', '-').lower()
    email = form.email.data
    user = User(usertype=usertype, firstname=firstname, lastname=lastname, username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created. You will now be able to log in.', 'success')
    return redirect(url_for('users.login'))
  return render_template('register.html', title='register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    if current_user.usertype == "employer":
      return redirect(url_for('jobs.job_posts', userid=current_user.id))
    elif current_user.usertype == "freelancer":
      return redirect(url_for('profiles.profile_posts', userid=current_user.id))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):  
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')    #called a query parameter
      if next_page:
        redirect(next_page)
      else:
        if current_user.usertype == "employer":
          return redirect(url_for('jobs.job_posts', userid=current_user.id))
        elif current_user.usertype == "freelancer":
          return redirect(url_for('profiles.profile_posts', userid=current_user.id))
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='login', form=form)


@users.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    current_user.firstname = form.firstname.data
    current_user.lastname = form.lastname.data
    current_user.email = form.email.data
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    db.session.commit()
    flash('Your account has been updated.', 'success')
    return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.email.data = current_user.email
  image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('users.login'))
  return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid/expired token.', 'warning')
    return redirect(url_for('users.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_new_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
    user.password = hashed_new_password
    db.session.commit()
    flash('Your password has been reset.', 'success')
    return redirect(url_for('users.login'))
  return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/account/delete', methods=['POST'])
@login_required
def delete_account():
  user = current_user
  uid = user.id
  utype = user.usertype
  if utype=='employer':
    jobs = Job.query.filter_by(user_id=uid)
    for job in jobs:
      db.session.delete(job)
      dataUpdater.delete_job(job)
      #dataUpdater.close_logs()
    #dataUpdater.resetJobIds()
    db.session.delete(user)
    db.session.commit()
  elif utype=='freelancer':
    profiles = Profile.query.filter_by(user_id=uid)
    for profile in profiles:
      db.session.delete(profile)
      dataUpdater.delete_profile(profile)
      #dataUpdater.close_logs()
    #dataUpdater.resetProfileIds()
    db.session.delete(user)
    db.session.commit()
  logout_user()
  flash('User account has been permanently deleted', 'success')
  return redirect(url_for('main.home'))


