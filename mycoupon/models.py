from django.db import models

# Create your models here.
from mongoengine import Document, StringField, IntField, URLField, DateTimeField,ListField,ReferenceField,EmbeddedDocumentListField

class tb_coupon(Document):
    pid = StringField(required=True)
    title = StringField(required=True)
    seller = StringField()
    seller_nick = StringField()
    price = StringField()
    volume = IntField()
    commission_rate = StringField()
    commission = StringField()
    url_item = StringField()
    url_pic = StringField()
    url_tk = StringField()
    url_coupon = StringField()
    coupon_info = StringField()
    coupon_total_count = IntField()
    coupon_remain_count = IntField()
    coupon_start_time = StringField()
    coupon_end_time = StringField()
    
    def __str__(self):
        return self.title
    def read_xls(self):
        import xlrd
        t = xlrd.open_workbook('20180204.xls')
        t = t.sheets()[0]
        td = []
        for i in range(1, t.nrows):
            tmp = t.row_values(i)
            td.append({
                'pid':tmp[0],
                'title':tmp[1],
                'seller':tmp[4],
                'seller_nick':tmp[9],
                'price':tmp[5],
                'volume':int(tmp[6]),
                'commission_rate':tmp[7],
                'commission':tmp[8],
                'url_item':tmp[3],
                'url_pic':tmp[2],
                'url_tk':tmp[11],
                'url_coupon':tmp[18],
                'coupon_info':'' if tmp[15] == '无' else tmp[15],
                'coupon_total_count':int(tmp[13]),
                'coupon_remain_count':int(tmp[14]),
                'coupon_start_time':tmp[16],
                'coupon_end_time':tmp[17],
            })
