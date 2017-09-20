# -*- coding:utf-8 -*-
"""模型"""
from mongoengine import Document, StringField, IntField, URLField, DateTimeField,ListField,ReferenceField,EmbeddedDocumentListField

class web_user(Document):
    username = StringField(required=True)
    pwd = StringField(max_length=100)
    role = StringField(max_length=500)

    def __str__(self):
        return self.username

class chi_booklist(Document):
    classid = IntField(required=True)
    name = StringField(required=True)
    author = StringField()
    publisher = StringField()

    def __str__(self):
        return self.name

class web_homework(Document):
    urlid = IntField(required=True)
    classof = IntField(required=True, default=int(0))   # 0,作业；1,通知；3,儿歌
    title = StringField(required=True, min_length=1, max_length=200)
    author = StringField(required=True)
    course = StringField()
    urllink = StringField()
    datestr = StringField(required=True)
    content = StringField(min_length=5)
    orderid = IntField()

    def __str__(self):
        return self.title

class web_html(Document):
    urlid = IntField(required=True)
    title = StringField(required=True)
    author = StringField()
    typeval = StringField()
    datestr = StringField()
    urllink = URLField()
    content = StringField()
    homework = ListField()
    # hw = EmbeddedDocumentListField()

    def __str__(self):
        return self.title

class web_user(Document):
    tid = IntField()
    tname = StringField()
    course = StringField()

    def __str__(self):
        return self.tname
