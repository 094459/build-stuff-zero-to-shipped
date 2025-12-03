# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from app.src.extensions import db
from datetime import datetime


class Fact(db.Model):
    __tablename__ = 'facts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    supporting_url = db.Column(db.Text)
    supporting_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    
    votes = db.relationship('Vote', backref='fact', lazy=True)
    
    def get_vote_counts(self):
        fact_votes = sum(1 for v in self.votes if v.vote_type == 'fact')
        fake_votes = sum(1 for v in self.votes if v.vote_type == 'fake')
        return {'fact': fact_votes, 'fake': fake_votes}
