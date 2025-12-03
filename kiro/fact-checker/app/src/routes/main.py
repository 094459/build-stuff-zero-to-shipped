# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from flask import Blueprint, render_template
from flask_login import login_required
from app.src.models.fact import Fact

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    facts = Fact.query.order_by(Fact.created_at.desc()).all()
    return render_template('dashboard.html', facts=facts)
