from flask_login import login_required, login_user, current_user

from models import Survey, User, db
from config import app, login_manager
from flask import Flask, render_template, request, redirect, url_for, flash

import forms


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = forms.RegisterForm()
    if request.method == "POST":
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
            flash("something wrong!")
    return render_template('register.html', form=form)


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_required
@app.route('/profile/')
def profile() :
    return f"ETO {current_user.username} PROFILE"



@app.route('/login/', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter(username=username).first()
            print(user.username)
            if user.check_password(form.password.data):
                login_user(user)
                flash("login successfully!")
                return redirect(url_for('profile'))

    return render_template('login.html', form=form)


@app.route('/', methods=['POST', 'GET'])
def main():
    surveys = Survey.query.all()
    form = forms.Surveyform()
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

    return render_template('main.html', list=surveys, form=form)


@app.route('/detail/<int:id>', methods=["POST", "GET"])
def detail(id):
    surv = Survey.query.get_or_404(id)
    form = forms.SurveyUpdateform()

    if request.method == "POST":

        if form.validate_on_submit():
            surv.question = form.question.data
            surv.variant_1 = form.variant_1.data
            surv.variant_2 = form.variant_2.data

            db.session.commit()

            return redirect(url_for('detail', id=id))

    return render_template('detail.html', form=form, survey=surv)
