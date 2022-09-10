# -*- coding: utf-8 -*-
"""
    @File   :   forms.search.py
    @Usage  :   搜索表单
    @Author :   Ray
    @Version:   1.0
"""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import StringField, SelectField, SubmitField, IntegerField, DateField, TimeField


class SingleRoomForm(FlaskForm):
    name = SelectField('楼名',choices=['安楼','博楼','诚楼','复楼','南楼','北楼'], validators=[DataRequired()])  #楼宇名称
    number = StringField('教室号',validators=[DataRequired(), Length(3, 3)])   #教室号
    week = IntegerField('课程周',validators=[DataRequired(), NumberRange(1, 17)])   #课程周
    submit = SubmitField("查询")


class ClassForm(FlaskForm):
    num = StringField('课程编号',validators=[Length(-1,10)])
    type = SelectField('课程类型',choices=['公共基础','公共选修','专业基础','专业选修'])
    c_name = StringField('课程名',validators=[Length(-1,40)])
    t_name = StringField('教师名',validators=[Length(-1,20)])
    submit = SubmitField("查询")


class AllRoomForm(FlaskForm):
    b_name = SelectField('楼名',choices=['安楼','博楼','诚楼','复楼','南楼','北楼'])
    type = SelectField('类型',choices=['普通','教室','休息室','会议室','实验室','自习室'])
    size = IntegerField('容量',validators=[NumberRange(1,130)])
    r_num = StringField('教室号',validators=[Length(3, 3)])
    date = DateField('查询日期')
    s_time = TimeField('开始时间')
    e_time = TimeField('结束时间')
    submit = SubmitField("查询")
