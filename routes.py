import os

from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from models import Survey, User, db, Votes
from config import app, login_manager, custom_logger, cache
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort

from flask_basicauth import BasicAuth

# from flask_cache import Cache

import forms

from flask_admin import Admin

admin = Admin()
admin.init_app(app)

admin.add_view(ModelView(Survey, db.session))
admin.add_view(ModelView(User, db.session))


@app.errorhandler(404)
def page_404(error):
    return render_template('404page.html'), 404


@app.errorhandler(403)
def page_403(error):
    return render_template('403page.html'), 403


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = forms.RegisterForm()
    if request.method == "POST":

        is_user = User.query.filter_by(username=form.username.data).first()

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password1.data

            user = User(username=username, email=email, password=password, image_path='uploads/anonuser_image.jpg')

            if form.image.data:
                file = form.image.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                user.image_path = 'uploads/' + filename

            db.session.add(user)
            db.session.commit()

            custom_logger.info(f"user {username} has registered")
            return redirect(url_for('main'))
        else:
            if form.password1.data != form.password2.data:
                flash("Passwords are not same!")

            if len(form.password1.data) < 8:
                flash("Passwords are not same!")

            if is_user:
                flash("User with such a username already exists")

            else:
                flash("kakayo-to hueta!")

    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@cache.cached(timeout=60)
@app.route('/', methods=['POST', 'GET'])
def main():

    if request.method == "POST" :
        pass

        votes = Votes.query.filter_by(id)
        #some logic
        votes.nums_of_1


    page_num = request.args.get('page', 1, type=int)
    surveys = Survey.query.paginate(per_page=6, page=page_num, error_out=True)
    return render_template('main_page.html', surveys=surveys)


@app.route('/detail/<int:id>', methods=["POST", "GET", "DELETE"])
def detail(id):
    surv = Survey.query.get_or_404(id)

    if surv.user.id != current_user.id:
        flash('You have no access to modify')
        return redirect(url_for("main"))

    form = forms.SurveyUpdateform()

    if request.method == "POST":

        if form.validate_on_submit():
            surv.question = form.question.data if form.question.data != '' else surv.question
            surv.variant_1 = form.variant_1.data if form.variant_1.data != '' else surv.variant_1
            surv.variant_2 = form.variant_2.data if form.variant_2.data != '' else surv.variant_2

            db.session.commit()

            return redirect(url_for('detail', id=id))

    context = {
        'form': form,
        'survey': surv
    }

    return render_template('detail.html', **context)


@login_required
@app.route('/delete/<int:id>')
def delete(id):
    surv = Survey.query.get_or_404(id)

    db.session.delete(surv)
    db.session.commit()

    return redirect(url_for('main'))


@login_required
@app.route('/profile/')
def profile():
    surveys = Survey.query.filter_by(user=current_user)
    return render_template('profile.html', surveys=surveys)


@login_required
@app.route('/profile/edit/', methods=['POST', 'GET'])
def profile_edit():
    form = forms.UserUpdateForm()

    if request.method == "POST":

        if form.validate_on_submit():
            current_user.username = form.username.data if form.username.data != '' else current_user.username
            current_user.email = form.email.data if form.email.data != '' else current_user.email
            print(form.image)
            if 'image' in request.files:
                file = request.files['image']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    # Далее, вы можете использовать filename по вашему усмотрению
                    # Например, записать путь к файлу в базу данных или переменную пользователя
                    current_user.image_path = 'uploads/' + filename

            db.session.commit()

            return redirect(url_for('main'))

    return render_template('edit_profile.html', form=form)


@app.route('/login/', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)

                custom_logger.info(f"user {username} logged in")
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

            question = form.question.data
            variant_1 = form.variant_1.data
            variant_2 = form.variant_2.data
            user = User.query.filter_by(id=current_user.id).first()
            survey = Survey(question=question, variant_1=variant_1, variant_2=variant_2, user=user)

            if form.image.data:
                file = form.image.data
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                survey.image_path = 'uploads/' + filename

            db.session.add(survey)
            db.session.commit()

            return redirect(url_for('main'))
        else:
            flash('something went wrong(')
    return render_template('create_surv.html', form=form)


@login_required
@app.route('/logout/')
def logout():
    response = redirect(url_for("main"))
    response.delete_cookie('username')

    custom_logger.info(f"user {current_user.username} logged out")
    logout_user()

    return response
