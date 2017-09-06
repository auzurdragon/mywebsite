# -*- coding:utf-8 -*-
"""模型"""
from mongoengine import Document, StringField, IntField, URLField, DateTimeField

class web_user(Document):
    username = StringField(required=True)
    pwd = StringField(max_length=100)
    role = StringField(max_length=500)

    def __str__(self):
        return self.username

class web_html(Document):
    title = StringField(required=True)
    orderid = IntField()
    typeval = StringField()
    urlid = IntField()
    urllink = URLField()
    datestr = DateTimeField()
    author = StringField()

    def __str__(self):
        return self.title
