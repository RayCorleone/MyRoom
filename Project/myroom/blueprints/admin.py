# -*- coding: utf-8 -*-
"""
    @File   :   admin.py
    @Usage  :   管理员界面视图函数
    @Author :   Ray
    @Version:   1.0
"""

from flask_login import login_required
from flask import render_template, flash, request, Blueprint

from myroom.utils import redirect_back
from myroom.models import Event, Event
from myroom.decorators import admin_required_flash

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
@admin_required_flash
def index():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'reviewed', 'waiting'
    page = request.args.get('page', 1, type=int)
    per_page = 20
    if filter_rule == 'reviewed':
        filtered_events = Event.query.filter_by(estimated=True)
    elif filter_rule == 'waiting':
        filtered_events = Event.query.filter_by(estimated=False)
    else:
        filtered_events = Event.query

    pagination = filtered_events.order_by(Event.submit_time.desc()).paginate(page, per_page=per_page)
    events = pagination.items

    return render_template('admin/manage.html', events=events, pagination=pagination)


@admin_bp.route('/<int:event_id>/approve', methods=['POST'])
@login_required
@admin_required_flash
def approve_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.approve()
    flash('Event approved.', 'success')
    return redirect_back()


@admin_bp.route('/<int:event_id>/reject', methods=['POST'])
@login_required
@admin_required_flash
def reject_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.reject()
    flash('Event rejected.', 'success')
    return redirect_back()
