# -*- coding: utf-8 -*-
"""
    @File   :   Models.py
    @Usage  :   数据库表结构文件
    @Author :   Ray
    @Version:   1.0
"""

from sqlalchemy import or_, and_
from flask_login import UserMixin
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash, check_password_hash

from myroom.extensions import db


## 教学楼
class Building(db.Model):
    # 主键-Int
    id = db.Column(db.Integer, primary_key=True)
    # 属性
    name = db.Column(db.String(20), nullable=False)     #楼名
    location = db.Column(db.String(20), nullable=False) #校区
    open_time = db.Column(db.Time, nullable=False, default=time(6,0,0))     #开楼时间
    close_time = db.Column(db.Time, nullable=False, default=time(22,0,0))   #闭楼时间

    # 关系
    rooms = db.relationship('Room', back_populates='building', cascade='all, delete-orphan')


## 教室
class Room(db.Model):
    # 主键-自增主键
    id = db.Column(db.Integer, primary_key=True)
    # 属性
    number = db.Column(db.String(5), nullable=False, index=True)    #房间号
    available = db.Column(db.Boolean, nullable=False, default=True) #是否可借用
    type = db.Column(db.String(10), nullable=False, default='all')  #教室类型(all,class,rest,meeting,lab,study)
    size = db.Column(db.Integer, nullable=False, default=40)        #教室容量(0~130)

    # 外键
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))  #所在教学楼
    # 关系
    building = db.relationship('Building', back_populates='rooms')
    events = db.relationship('Event', back_populates='room', cascade='all, delete-orphan',lazy='dynamic')
    open_courses = db.relationship('OpenCourse', back_populates='room', cascade='save-update, merge',lazy='dynamic')


## 院系
class Department(db.Model):
    # 主键-Int
    id = db.Column(db.Integer, primary_key=True)
    # 属性
    name = db.Column(db.String(20), nullable=False, unique=True)    #院系名

    # 关系
    courses = db.relationship('Course', back_populates='department', cascade='all, delete-orphan')    
    users = db.relationship('User', back_populates='department', cascade='save-update, merge')    


## 课程
class Course(db.Model):
    # 主键-自增主键
    id = db.Column(db.Integer, primary_key=True)
    # 属性
    number = db.Column(db.String(10), nullable=False, unique=True, index=True)
    name = db.Column(db.String(40), nullable=False) #课程名
    credit = db.Column(db.Integer, nullable=False)  #学分
    type = db.Column(db.String(3), nullable=False, default='GF')    #类型(GF,GE,SA,SF)

    # 外键
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))   #所属学院
    # 关系
    department = db.relationship('Department', back_populates='courses')
    open_courses = db.relationship('OpenCourse', back_populates='course', cascade='all, delete-orphan')


## 用户(老师、学生、管理员)
class User(db.Model, UserMixin):
    # 主键-自增主键(Admin=0)
    id = db.Column(db.Integer, primary_key=True)
    # 属性
    number = db.Column(db.String(10),nullable=False,unique=True,index=True) #工号/学号
    password_hash = db.Column(db.String(128))   #密码(加密后)
    admin = db.Column(db.Boolean, nullable=False, default=False)    #是否是管理员
    name = db.Column(db.String(20), nullable=False)                     #姓名
    sex = db.Column(db.String(7), nullable=False, default='male')       #性别(male,female)
    type = db.Column(db.String(10), nullable=False, default='Student')  #类型(Student,Teacher,Admin)

    # 外键
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))   #所属学院
    # 关系
    department = db.relationship('Department', back_populates='users')
    events = db.relationship('Event', back_populates='user', cascade='all, delete-orphan')
    open_courses = db.relationship('OpenCourse', back_populates='user', cascade='save-update, merge')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.admin


## 开课信息
class OpenCourse(db.Model):
    # 主键-自增主键
    id = db.Column(db.Integer, primary_key=True)
    # 属性
    start_date = db.Column(db.Date, default=date(2022,2,21))    #开学日期
    start_week = db.Column(db.Integer, default=1)   #开课周
    finish_week = db.Column(db.Integer, default=17) #结课周
    weekday = db.Column(db.Integer, nullable=False, index=True) #上课日(星期一到日: 1~7)
    start_time = db.Column(db.Time, nullable=False, index=True) #上课时间
    finish_time = db.Column(db.Time, nullable=False, index=True)#下课时间
    note = db.Column(db.Text, default='Test')       #课程备注

    # 外键
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))       #教室
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       #老师
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))   #课程
    # 关系
    room = db.relationship('Room', back_populates='open_courses')
    user = db.relationship('User', back_populates='open_courses')
    course = db.relationship('Course', back_populates='open_courses')

    #当前时段/房间是否可以开课
    def is_avaiable_to_open(self):
        open_courses = OpenCourse.query.filter_by(
            room_id = self.room_id,         #同一房间
            weekday = self.weekday,         #同一日子
            start_time = self.start_time    #同一开始时间
            ).first()
        if open_courses is not None:
            print("--Generating open_course failed")
            return False
        return True


## 借用/审核事件
class Event(db.Model):
    # 主键-自增主键
    id = db.Column(db.Integer, primary_key=True)
    # 借用属性
    start_date = db.Column(db.Date, default=date(2022,2,21))    #开学日期
    submit_time = db.Column(db.DateTime, default=datetime.now(), index=True)    #提交时间
    date = db.Column(db.Date, default=date.today()) #借用日期
    start_time = db.Column(db.Time, nullable=False) #借用开始时间
    finish_time = db.Column(db.Time, nullable=False)#借用结束时间
    note = db.Column(db.Text, nullable=False)       #借用备注
    # 审核属性
    estimated = db.Column(db.Boolean, default=False)#是否已审核
    passed = db.Column(db.Boolean, default=False)   #是否已通过
    comment = db.Column(db.Text)                    #审核备注
    examine_time = db.Column(db.DateTime)           #审核时间

    # 外键
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))   #所用教室
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #借用人员
    # 关系
    room = db.relationship('Room', back_populates='events')
    user = db.relationship('User', back_populates='events')

    def approve(self, comment="None"):
        if self.is_avaiable:
            self.estimated = True
            self.passed = True
            self.comment = comment
            db.session.commit()

    def reject(self, comment="None"):
        self.estimated = True
        self.passed = False
        self.comment = comment
        db.session.commit()

    @property
    def is_estimated(self):
        return self.estimated

    @property
    def is_passed(self):
        return self.passed
    
    @property
    def is_rejected(self):
        return (self.estimated is True) and (self.passed is False)

    #当前时段/房间是否可以借用
    def is_avaiable(self):
        # 查看教室可不可以借用
        room1 = Room.query.filter(
            Room.id == self.room_id,#同一房间
            Room.available == True  #可以借用
            ).first()
        if room1 is None:
            print("--Generating event failed")
            return False

        # 计算借用日期对应周几
        b_weekday = int((self.date - self.start_date).days) % 7 + 1
        if b_weekday < 0 or b_weekday > 17*7:
            b_weekday = 0

        # 筛选 同一天+同一教室+时间有重叠 的课程
        open_course1 = OpenCourse.query.filter(
            OpenCourse.room_id == self.room_id, #同一房间
            OpenCourse.weekday == b_weekday,    #同一日子
            or_(and_(#活动开始时间在课程之间
            OpenCourse.start_time < self.start_time,    
            OpenCourse.finish_time > self.start_time),
                and_(#活动结束时间在课程之间
            OpenCourse.start_time < self.finish_time,
            OpenCourse.finish_time > self.finish_time))
            ).first()
        if open_course1 is not None:
            print("--Generating event failed")
            return False

        # 筛选 同一天+同一教室+已经通过+时间有重叠 的活动
        event1 = Event.query.filter(
            Event.room_id == self.room_id,  #同一房间
            Event.date == self.date,        #同一日子
            Event.passed == True,           #已经通过
            or_(and_(#活动开始时间在活动之间
            Event.start_time < self.start_time,    
            Event.finish_time > self.start_time),
                and_(#活动结束时间在活动之间
            Event.start_time < self.finish_time,
            Event.finish_time > self.finish_time))
            ).first()
        if event1 is not None:
            print("--Generating event failed")
            return False
        return True
