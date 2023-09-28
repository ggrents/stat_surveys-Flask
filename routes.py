from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash

from models import Survey, User, db
from config import app, login_manager, custom_logger
from flask import Flask, render_template, request, redirect, url_for, flash, session

import forms


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = forms.RegisterForm()
    if request.method == "POST":

        is_user = User.query.filter_by(username=form.username.data).first()

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password1.data

            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash("success")

            return redirect(url_for('main'))
        else:
            if form.password1.data != form.password2.data:
                flash("Passwords are not same!")

            if len(form.password1.data) < 8:
                flash("Passwords are not same!")

            if is_user:
                flash("User with such a username already exists")

    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['POST', 'GET'])
def main():
    surveys = Survey.query.all()
    return render_template('main_page.html', list=surveys)


@app.route('/detail/<int:id>', methods=["POST", "GET"])
def detail(id):
    surv = Survey.query.get_or_404(id)
    form = forms.SurveyUpdateform()

    if request.method == "POST":

        if form.validate_on_submit():
            surv.question = form.question.data if form.question.data != '' else surv.question
            surv.variant_1 = form.variant_1.data if form.variant_1.data != '' else surv.variant_1
            surv.variant_2 = form.variant_2.data if form.variant_2.data != '' else surv.variant_2

            db.session.commit()

            return redirect(url_for('detail', id=id))

    return render_template('detail.html', form=form, survey=surv)


@login_required
@app.route('/profile/')
def profile():
    surveys = Survey.query.filter_by(user = current_user)
    return render_template('profile.html', surveys = surveys)


@app.route('/login/', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("login successfully!")
                response = redirect(url_for('profile'))
                response.set_cookie('username', username)
                if f'count_visit_of_{username}' not in session:
                    session[f'count_visit_of_{username}'] = 1
                else:
                    session[f'count_visit_of_{username}'] = session[f'count_visit_of_{username}'] + 1
                return response
            else:
                flash("something went wrong!")

    return render_template('login.html', form=form)


@login_required
@app.route('/create_surv/', methods=["GET", "POST"])
def create_surv():
    form = forms.Surveyform()
    if request.method == "POST":

        if form.validate_on_submit():
            flash('Survey was created!')
            question = form.question.data
            variant_1 = form.variant_1.data
            variant_2 = form.variant_2.data
            user = User.query.filter_by(id=1).first()
            survey = Survey(question=question, variant_1=variant_1, variant_2=variant_2, user=user)
            db.session.add(survey)
            db.session.commit()

            return redirect(url_for('main'))

    return render_template('create_surv.html', form=form)


@login_required
@app.route('/logout/')
def logout():
    response = redirect(url_for("main"))
    response.delete_cookie('username')
    logout_user()
    return response
