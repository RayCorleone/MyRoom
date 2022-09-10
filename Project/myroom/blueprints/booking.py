# -*- coding: utf-8 -*-
"""
    @File   :   booking.py
    @Usage  :   借用教室视图函数
    @Author :   Ray
    @Version:   1.0
"""

from datetime import date, datetime
from flask_login import current_user, login_required
from flask import render_template, flash, request, Blueprint

from myroom.extensions import db
from myroom.utils import redirect_back
from myroom.forms.booking import EventForm
from myroom.models import Event, Room, Building, Event
from myroom.decorators import not_admin_required_flash

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/', methods=['GET', 'POST'])
@login_required             #登录
@not_admin_required_flash   #不是管理员
def index():
    ## 新提交
    form = EventForm()
    if form.validate_on_submit():
        u_date = form.use_date.data
        s_time = form.s_time.data
        e_time = form.e_time.data
        b_name = form.b_name.data
        r_num = form.r_num.data
        note = form.note.data

        building = Building.query.filter_by(name=b_name).first()
        room = Room.query.filter_by(number=r_num, building_id=building.id).first()
        if room is not None:
            event = Event(
                start_date = date(2022,2,21),
                submit_time = datetime.now(),
                date = u_date,
                start_time = s_time,
                finish_time = e_time,
                note = note,
                room_id = room.id,
                user_id = current_user.id
            )
            if event.is_avaiable():
                db.session.add(event)
                db.session.commit()
                flash('Application posted.', 'success')
            else:
                flash('Time conflicts.', 'warning')
        else:
            flash('Invalid room number.', 'warning')

    ## 历史提交管理
    filter_rule = request.args.get('filter', 'all')  # 'all', 'reviewed', 'waiting'
    page = request.args.get('page', 1, type=int)
    per_page = 10
    if filter_rule == 'reviewed':
        filtered_events = Event.query.filter_by(estimated=True, user_id=current_user.id)
    elif filter_rule == 'waiting':
        filtered_events = Event.query.filter_by(estimated=False, user_id=current_user.id)
    else:
        filtered_events = Event.query.filter_by(user_id=current_user.id)

    pagination = filtered_events.order_by(Event.submit_time.desc()).paginate(page, per_page=per_page)
    events = pagination.items

    return render_template('booking/booking.html', form=form, events=events, pagination=pagination)


@booking_bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
@not_admin_required_flash   #不是管理员
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Application deleted.', 'success')
    return redirect_back()
