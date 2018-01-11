# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)
from conf import settings

from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

student_m2m_class = Table(
    "student_m2m_class", Base.metadata,
    Column("class_id", Integer, ForeignKey("class.id")),
    Column("stu_qq", String(32), ForeignKey("student.qq"))
)

teacher_m2m_class = Table(
    "teacher_m2m_class", Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teacher.id")),
    Column("class_id", Integer, ForeignKey("class.id"))
)

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    classes = relationship("Class", secondary=teacher_m2m_class, backref="teachers")

    def __repr__(self):
        return self.name

class Student(Base):
    __tablename__ = 'student'
    qq = Column(String(32), primary_key=True)
    name = Column(String(64))

    classes = relationship("Class", secondary=teacher_m2m_class, backref="students")

    def __repr__(self):
        return self.name

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __repr__(self):
        return self.name

class Score(Base):
    __tablename__ = 'score'
    stu_qq = Column(String(32), ForeignKey("student.qq"), primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)
    class_count = Column(Integer, primary_key=True)
    score = Column(String(32))

    student_obj = relationship("Student", backref="score")
    class_obj = relationship("Class", backref="score")

    def __repr__(self):
        return "课程名：%s, 分数：%s" %(self.class_obj.name, self.score)

# 获取数据库连接信息
conn_cursor = "mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}".format(
                            user=settings.User,
                            password=settings.Password,
                            host=settings.Host,
                            database=settings.Database,
                            charset=settings.Charset
                        )

engine = create_engine(conn_cursor,
                       encoding='utf-8',
                       echo=True
                       )
Base.metadata.create_all(engine)

