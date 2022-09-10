# -*- coding: utf-8 -*-
"""
    @File   :   fakes.py
    @Usage  :   伪造数据文件
    @Author :   Ray
    @Version:   1.0
"""

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date, time

from myroom.extensions import db
from myroom.models import Building,Room,Department,Course,User,Event,OpenCourse

fake = Faker('zh_CN')


## 指定概率生成函数
def random_professional(choice_list, rate_list):
    # 检验大小是否相等
    if len(choice_list) != len(rate_list):
        print("Two list should be of the same size.")
        return choice_list[0]
    
    sum = 0
    sum_list = []
    for rate in rate_list:
        sum = sum + rate
        sum_list.append(sum)
    
    num = random.uniform(0,sum)
    for i in range(0,len(choice_list)):
        if num <= sum_list[i]:
            return choice_list[i]
    return choice_list[-1]


## 生成教学楼(6)
def fake_building():
    count = 6
    name_list = ['安楼','博楼','南楼','诚楼','复楼','北楼']
    location_list = ['四平校区','嘉定校区','嘉定校区']

    for i in range(1,count+1):
        building = Building(
            id = i,
            name = name_list[i-1],
            location = location_list[i%3]
        )
        db.session.add(building)
    db.session.commit()


## 生成教室(360)
def fake_room():
    count = 360
    avlb_clist = [True, False]
    avlb_rlist = [90,10]
    type_clist = ['all','class','rest','meeting','lab','study']
    type_rlist = [150,10,10,20,20,20]

    for i in range(count):
        room_number = 1 + (i%60)%20 + 100*((i%60)//20+1)
        room = Room(
            number = str(room_number),
            available = random_professional(avlb_clist,avlb_rlist),
            type = random_professional(type_clist,type_rlist),
            size = random.randrange(30,140,20),
            building_id = 1 + (i//60)
        )
        db.session.add(room)
    db.session.commit()


## 生成院系(6+1)
def fake_department():
    count = 6
    name_list = ['None','电子与信息工程学院',
        '艺术与传媒学院','机械与能源工程学院',
        '土木工程学院','外国语学院','软件学院']
    
    for i in range(0,count+1):
        department = Department(
            id = i,
            name = name_list[i]
        )
        db.session.add(department)
    db.session.commit()


## 生成课程(1000)
def fake_course():
    count = 1000
    cred_clist = [16,8,4,3,2,1,0]
    cred_rlist = [1,2,8,10,15,10,2]
    type_clist = ['GF','GE','SA','SF']
    type_rlist = [40,80,80,160]

    for i in range(count):
        if i % 100 == 0:
            print("-Generating Course",i)

        course = Course(
            number = fake.bothify(text='########'),
            name = fake.sentence(nb_words=4).replace('.',''),
            credit = random_professional(cred_clist, cred_rlist),
            type = random_professional(type_clist, type_rlist),
            department_id = random.randint(1, Department.query.count()-1)
        )
        db.session.add(course)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


## 生成管理员账号(1)
def fake_admin():
    admin = User(
        id = 0,
        number = '1952100',
        admin = True,
        name = 'RayHuC',
        sex = 'male',
        type = 'Admin',
        department_id = 0
    )
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()


## 生成用户账号(150+250)
def fake_user():
    t_count = 150
    s_count = 250
    dep_count = Department.query.count() - 1

    # 生成老师数据150条
    for i in range(t_count):    #id: 1~150
        if i % 10 == 0:
            print("-Generating Teacher",i)

        user = User(
            id = i + 1,
            number = fake.bothify(text='#####'),
            admin = False,
            name = fake.name(),
            sex = random.choice(['male','female']),
            type = 'Teacher',
            department_id = random.randint(1,dep_count)
        )
        user.set_password('20220310')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    # 生成学生数据250条
    for i in range(s_count):    #id: 151~400
        if i % 10 == 0:
            print("-Generating Student",i)

        user = User(
            id = t_count + i + 1,
            number = fake.bothify(text='#######'),
            admin = False,
            name = fake.name(),
            sex = random.choice(['male','female']),
            type = 'Student',
            department_id = random.randint(1,dep_count)
        )
        user.set_password('20220310')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


## 生成开课信息(2300)
def fake_open_course():
    count = 2300
    room_count = Room.query.count()
    start_time_list = [time(8,0,0),time(10,0,0),time(13,30,0),time(15,30,0),time(19,0,0),time(19,0,0)]
    finish_time_list = [time(9,35,0),time(11,35,0),time(15,5,0),time(17,5,0),time(20,35,0),time(21,25,0)]

    for i in range(count):
        if i % 100 == 0:
            print("-Generating OpenCourse",i)

        while True:
            time_index = random.randint(0,5)
            open_course = OpenCourse(
                weekday = random.randint(1,5),
                start_time = start_time_list[time_index],
                finish_time = finish_time_list[time_index],
                note = fake.text(max_nb_chars=100),
                room_id = random.randint(1, room_count),
                user_id = random.randint(1, 150),
                course_id = i % 100 + 1
            )
            if open_course.is_avaiable_to_open():
                db.session.add(open_course)
                break
    db.session.commit()


## 生成借用事件(50)
def fake_event():
    count = 50
    room_count = Room.query.count()

    bool_clist = [True, False]
    esti_rlist = [5,35]
    pass_rlist = [30,5]
    start_time_list = [time(x,0,0) for x in range(6,22)]
    finish_time_list = [time(x,0,0) for x in range(7,23)]

    for i in range(count):
        if i % 10 == 0:
            print("-Generating event",i)

        while True:
            #时间数据生成
            b_date = fake.date_between(start_date=date(2022,2,21), end_date=date(2022,6,1))     #借用日期
            submit_time = fake.date_time_between(start_date=date(2022,2,20), end_date=b_date)   #提交时间
            diff = b_date - datetime.today().date()   #借用日期和今天的差值
            end_data = 0
            if int(diff.days) > 0:  #借用日期是未来, 在今天之前审核完就行
                end_data = 'now'
            else:   #借用日期是过去, 在借用日期之前应该审核完
                end_data = b_date
            examine_time = fake.date_time_between(start_date=submit_time, end_date=end_data) #审核时间

            time_index = random.randint(0,len(start_time_list)-1)
            start_time = start_time_list[time_index]
            finish_time = finish_time_list[random.randint(time_index,len(start_time_list)-1)]

            #事件数据生成
            est_bool = random_professional(bool_clist,esti_rlist)
            if est_bool:#已审核
                event = Event(
                    start_date = date(2022,2,21),
                    submit_time = submit_time,
                    date = b_date,
                    start_time = start_time,
                    finish_time = finish_time,
                    note = fake.text(max_nb_chars=50),
                    estimated = True,
                    passed = random_professional(bool_clist,pass_rlist),
                    comment = fake.text(max_nb_chars=50),
                    examine_time = examine_time,
                    room_id = random.randint(1, room_count),
                    user_id = random.randint(1,400)
                )
                if event.is_avaiable():
                    db.session.add(event)
                    break
            
            else:       #未审核
                event = Event(
                    start_date = date(2022,2,21),
                    submit_time = submit_time,
                    date = b_date,
                    start_time = start_time,
                    finish_time = finish_time,
                    note = fake.text(max_nb_chars=50),
                    room_id = random.randint(1, room_count),
                    user_id = random.randint(1,400)
                )
                if event.is_avaiable():
                    db.session.add(event)
                    break

    db.session.commit()
