# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from app.src.extensions import db
from datetime import datetime


class Vote(db.Model):
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    fact_id = db.Column(db.Integer, db.ForeignKey('facts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        db.CheckConstraint("vote_type IN ('fact', 'fake')", name='check_vote_type'),
    )
