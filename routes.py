from models import Survey, User, db
from config import app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

import forms


@app.route('/register', methods = ['POST', 'GET'])
def register() :
    form = forms.RegisterForm()

    return render_template('register.html', form = form)


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
    if form.validate_on_submit():
        surv.question = form.question.data if form.question.data else surv.question
        surv.variant_1 = form.variant_1.data if form.variant_1.data else surv.variant_1
        surv.variant_2 = form.variant_2.data if form.variant_2.data else surv.variant_2

        db.session.commit()

        return redirect(url_for('detail', id=id))

    return render_template('detail.html', form=form, survey=surv)
