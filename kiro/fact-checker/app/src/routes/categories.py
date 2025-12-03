# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.src.extensions import db
from app.src.models.category import Category

bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if Category.query.filter_by(name=name).first():
            flash('Category already exists', 'error')
            return redirect(url_for('categories.create'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('categories/create.html')
