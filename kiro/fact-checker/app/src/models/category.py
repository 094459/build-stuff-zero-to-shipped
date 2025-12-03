# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from app.src.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    facts = db.relationship('Fact', backref='category', lazy=True)
