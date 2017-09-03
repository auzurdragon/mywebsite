# -*- coding:utf-8 -*-
from mongoengine import *

class web_user(Document):
    username = StringField(required=True)
    pwd = StringField(max_length=100)
    role = StringField(max_length=500)

    def __str__(self):
        return self.username

class web_html(Document):
    title = StringField(required=True)
    classof = StringField()
    url = StringField()

    def __str__(self):
        return self.title
