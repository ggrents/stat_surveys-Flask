from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


from config import db


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(320), unique=False, nullable=False)
    variant_1 = db.Column(db.String(320), unique=False, nullable=False)
    variant_2 = db.Column(db.String(320), unique=False, nullable=False)
    variant_3 = db.Column(db.String(320), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('surveys', lazy=True))

    def __init__(self, question, variant_1, variant_2, variant_3, user):
        self.question = question
        self.variant_1 = variant_1
        self.variant_2 = variant_2
        self.variant_3 = variant_3
        self.user = user


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
