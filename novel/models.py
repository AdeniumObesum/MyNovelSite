from django.db import models
from mongoengine import *
import time
SEARCHORDERBY={"title":"书名","author":"作者",}
NOVELMODELDISPLAY=['show_img','title','author','tags','score','id',]
# Create your models here.
class NovelModel(Document):
    meta = {
        'collection': 'novels',
    }
    show_img = BooleanField(default=True,name='显示封面')
    title = StringField(max_length=64)

    author = StringField(max_length=64)

    publish_date = DateTimeField(name='发布日期',default=time.ctime())

    tags = ListField(StringField(max_length=30),name='分类')
#  http://xiaoshuo.vlcms.com/Uploads/Picture/2018-03-16/5aab3521827b6.jpg     小说封面图
#
    img_url = StringField(max_length=2048,default='/images/')

    img_content = BinaryField(name='封面')

    score = IntField(name='赞',default=0)
    content = StringField(name="小说正文",default='')
    @queryset_manager
    def show_newest(self, queryset):
        return queryset.order_by('-publish_date')

    pass
