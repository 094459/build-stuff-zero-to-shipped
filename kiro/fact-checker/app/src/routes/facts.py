# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.src.extensions import db
from app.src.models.fact import Fact
from app.src.models.vote import Vote
from app.src.models.category import Category
from datetime import datetime

bp = Blueprint('facts', __name__, url_prefix='/facts')


@bp.route('/<int:fact_id>')
@login_required
def view(fact_id):
    fact = Fact.query.get_or_404(fact_id)
    user_vote = Vote.query.filter_by(fact_id=fact_id, user_id=current_user.id).first()
    vote_counts = fact.get_vote_counts()
    return render_template('facts/view.html', fact=fact, user_vote=user_vote, vote_counts=vote_counts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        supporting_url = request.form.get('supporting_url')
        supporting_info = request.form.get('supporting_info')
        
        fact = Fact(
            user_id=current_user.id,
            category_id=category_id,
            content=content,
            supporting_url=supporting_url,
            supporting_info=supporting_info
        )
        db.session.add(fact)
        db.session.commit()
        
        flash('Fact created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    categories = Category.query.all()
    return render_template('facts/create.html', categories=categories)


@bp.route('/<int:fact_id>/vote', methods=['POST'])
@login_required
def vote(fact_id):
    vote_type = request.form.get('vote_type')
    
    if vote_type not in ['fact', 'fake']:
        flash('Invalid vote type', 'error')
        return redirect(url_for('facts.view', fact_id=fact_id))
    
    existing_vote = Vote.query.filter_by(fact_id=fact_id, user_id=current_user.id).first()
    
    if existing_vote:
        existing_vote.vote_type = vote_type
        existing_vote.created_at = datetime.utcnow()
    else:
        new_vote = Vote(fact_id=fact_id, user_id=current_user.id, vote_type=vote_type)
        db.session.add(new_vote)
    
    db.session.commit()
    flash('Vote recorded!', 'success')
    return redirect(url_for('facts.view', fact_id=fact_id))


@bp.route('/<int:fact_id>/update-info', methods=['POST'])
@login_required
def update_info(fact_id):
    fact = Fact.query.get_or_404(fact_id)
    supporting_info = request.form.get('supporting_info')
    
    fact.supporting_info = supporting_info
    fact.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Supporting information updated!', 'success')
    return redirect(url_for('facts.view', fact_id=fact_id))
