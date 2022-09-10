# -*- coding: utf-8 -*-
"""
    @File   :   forms.booking.py
    @Usage  :   借用表单
    @Author :   Ray
    @Version:   1.0
"""

from datetime import time
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms import StringField, SelectField, SubmitField, DateField, TimeField, TextAreaField


def st_right(form,field):
    t1 = time(6,0,0)
    t2 = time(21,0,0)
    if field.data < t1 or  field.data > t2:
        raise ValidationError('Must be between 6:00 and 21:00.')


def et_right(form,field):
    t1 = time(7,0,0)
    t2 = time(22,0,0)
    if field.data < t1 or  field.data > t2:
        raise ValidationError('Must be between 7:00 and 22:00.')
    if form.s_time.data > field.data:
        raise ValidationError('End time must be later than start time.')
    time_bt = (field.data.hour - form.s_time.data.hour)*60 + field.data.minute - form.s_time.data.minute
    if time_bt < 60:
        raise ValidationError('At least 1 hour.')


class EventForm(FlaskForm):
    use_date = DateField('借用日期',validators=[DataRequired()])    #借用日期
    s_time = TimeField('开始时间',validators=[DataRequired(),st_right])  #开始时间
    e_time = TimeField('结束时间',validators=[DataRequired(), et_right])  #结束时间
    b_name = SelectField('楼名',choices=['安楼','博楼','诚楼','复楼','南楼','北楼'], validators=[DataRequired()])  #楼宇名称
    r_num = StringField('教室号',validators=[DataRequired(), Length(3, 3)])   #教室号
    note = TextAreaField('申请备注',validators=[DataRequired(), Length(10, -1)])#备注
    submit = SubmitField("提交")