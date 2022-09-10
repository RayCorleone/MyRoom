# -*- coding: utf-8 -*-
"""
    @File   :   search.py
    @Usage  :   查找视图函数
    @Author :   Ray
    @Version:   1.0
"""

from datetime import datetime, date, time
from sqlalchemy import or_, and_
from flask import Blueprint, flash, render_template, request

from myroom.models import Room, Building, OpenCourse, Course, User, Event
from myroom.forms.search import SingleRoomForm, ClassForm, AllRoomForm

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET', 'POST'])
@search_bp.route('/singleroom', methods=['GET', 'POST'])
def index():
    weekday_list = [1,2,3,4,5,6,7]
    finish_time_list = [time(9,35,0),time(11,35,0),time(15,5,0),time(17,5,0),time(20,35,0),time(21,25,0)]

    # 要展示的课程表
    class_info = []
    start_time = ["08:00-09:35","10:00-11:35","13:30-15:05","15:30-17:05","19:00-20:35","20:40-21:25"]
    info_line = [0,0,0,0,0,0,0]
    for i in range(0,6):
        temp = [start_time[i]] + info_line
        class_info.append(temp)

    # 表单和提交表单后动作
    form = SingleRoomForm()
    if form.validate_on_submit():
        b_name = form.name.data
        r_num = form.number.data
        week = form.week.data

        building = Building.query.filter_by(name=b_name).first()
        room = Room.query.filter_by(number=r_num,building_id=building.id).first()
        if room is not None:
            i_index = 0
            j_index = 1
            r_id = room.id
            for ft in finish_time_list:
                j_index = 1
                for wd in weekday_list:
                    temp_oc = OpenCourse.query.filter_by(finish_time=ft,weekday=wd,room_id=r_id).first()
                    if temp_oc is not None:
                        class_info[i_index][j_index] = temp_oc.course
                    else:
                        class_info[i_index][j_index] = 0
                    j_index = j_index + 1
                i_index = i_index + 1
        else:
            flash('Invalid room number.', 'warning')

    return render_template('search/singleroom.html', form=form, class_info=class_info)


@search_bp.route('/class', methods=['GET', 'POST'])
def search_class():
    # 分页
    page = request.args.get('page', 1, type=int)
    per_page = 2400
    class_result = OpenCourse.query.filter_by(start_week=18)

    # 表单和提交表单后动作
    form = ClassForm()
    if form.validate_on_submit():
        class_result = OpenCourse.query
        page = 1

        if form.t_name.data:
            t_name = form.t_name.data
            class_result = class_result.join(User.query.filter(User.name.like('%'+t_name+'%'),User.type=='Teacher'))
        if form.num.data:
            num = form.num.data
            class_result = class_result.join(Course.query.filter_by(number=num))
        if form.c_name.data:
            c_name = form.c_name.data
            class_result = class_result.join(Course.query.filter(Course.name.like('%'+c_name+'%')))

        t_type = form.type.data
        if t_type == '公共基础':
            t_type = 'GF'
        elif t_type == '公共选修':
            t_type = 'GE'
        elif t_type == '专业选修':
            t_type = 'SA'
        else:
            t_type = 'SF'
        class_result = class_result.join(Course.query.filter_by(type=t_type))

    pagination = class_result.order_by(OpenCourse.id.desc()).paginate(page, per_page=per_page)
    class_info = pagination.items
    return render_template('search/class.html', form=form, class_info=class_info)#, pagination=pagination)


@search_bp.route('/allroom', methods=['GET', 'POST'])
def search_all():
    # 分页
    page = request.args.get('page', 1, type=int)
    per_page = 1000
    room_result = Room.query.filter_by(id=0)
    room_use = []

    # 表单和提交表单后动作
    flag = False
    form = AllRoomForm()
    if request.method == 'POST':
        flag = False

        # 判断搜索分级
        flag_1 = False  #一级搜索
        flag_2 = False  #二级搜索

        if form.b_name.data or form.type.data or form.size.data or form.r_num.data:
            flag_1 = True
        if flag_1 and form.date.data and form.s_time.data and form.e_time.data:
            flag_2 = True

        # 分级操作
        if not flag_1:
            flash('Invalid filters.', 'warning')
        else:
            # 获取公共数据
            b_name = form.b_name.data
            building = Building.query.filter_by(name=b_name).first()
            r_type = form.type.data   #['普通','教室','休息室','会议室','实验室','自习室']
            if r_type == '教室':
                r_type = 'class'
            elif r_type == '休息室':
                r_type = 'rest'
            elif r_type == '会议室':
                r_type = 'meeting'
            elif r_type == '会议室':
                r_type = 'meeting'
            elif r_type == '实验室':
                r_type = 'lab'
            elif r_type == '自习室':
                r_type = 'study'
            else:
                r_type = 'all'
            room_result = Room.query.filter_by(building_id=building.id,type=r_type)
            if form.r_num.data:
                room_result = room_result.filter_by(number=form.r_num.data)
            if form.size.data:
                room_result = room_result.filter(Room.size>=form.size.data)

            if not flag_2:
                flag = False
            else:
                flag = True
                room_use.clear()
                t_date = form.date.data
                s_time = form.s_time.data
                e_time = form.e_time.data
                # 计算日期对应周几
                start_date = date(2022,2,21)
                b_weekday = int((t_date - start_date).days) % 7 + 1
                if b_weekday < 0 or b_weekday > 17*7:
                    b_weekday = 0

                for room in room_result:
                    event1 = room.events.filter(
                        Event.date == t_date,     #当天
                        Event.passed == True,   #已经通过
                        or_(and_(#开始时间在查询之间
                        Event.start_time > s_time,    
                        Event.start_time < e_time),
                            and_(#结束时间在查询之间
                        Event.finish_time > s_time,
                        Event.finish_time < e_time))
                        ).first()
                    open_course1 = room.open_courses.filter(
                        OpenCourse.weekday == b_weekday,    #当日
                        or_(and_(#开始时间在查询之间
                        OpenCourse.start_time > s_time,    
                        OpenCourse.start_time < e_time),
                            and_(#结束时间在查询之间
                        OpenCourse.finish_time > s_time,
                        OpenCourse.finish_time < e_time))
                        ).first()
                    
                    if event1 is not None:
                        room_use.append(1)
                    elif open_course1 is not None:
                        room_use.append(2)
                    else:
                        room_use.append(0)

    pagination = room_result.paginate(page, per_page=per_page)
    room_info = pagination.items
    room_use.append(len(room_use))

    return render_template('search/allroom.html', form=form, room_info=room_info, flag=flag, room_use=room_use)
