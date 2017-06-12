from django.db import models
from infernoWeb.models import User
import datetime
# 要取得會員的model要這樣寫

# Create your models here.
class Course(models.Model):
    """docstring for Course"""
    name = models.CharField(max_length=10)
    ctype = models.CharField(max_length=10,default='')# 課程是通識必修還是選修
    dept = models.CharField(max_length=20, default='')
    avatar = models.ImageField(default='') # 大頭貼照片
    teacher = models.CharField(max_length=10)
    school = models.CharField(max_length=10)
    book = models.CharField(max_length=50)
    feedback_amount = models.PositiveIntegerField(default=0)
    feedback_freedom = models.FloatField(default=0)
    feedback_FU = models.FloatField(default=0)
    feedback_easy = models.FloatField(default=0)
    feedback_GPA = models.FloatField(default=0)
    feedback_knowledgeable = models.FloatField(default=0)
    benchmark = models.CharField(max_length=60, default='')
    attendee = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Comment(models.Model):
    course = models.ForeignKey(Course)
    author = models.ForeignKey(User)
    create = models.DateTimeField(default=datetime.datetime.now)
    raw = models.CharField(max_length=500)
    like = models.PositiveSmallIntegerField(default=0)
    emotion = models.CharField(
        max_length=7,
        choices=(
            ('neutral', 'neutral'),
            ('pos', 'pos'),
            ('neg', 'neg'),
        ),
        default='neutral',
    )
    def __str__(self):
        return self.raw

class LikesFromUser(models.Model):
    comment = models.ManyToManyField(Comment)
    course = models.ManyToManyField(Course)
    author = models.OneToOneField(User)
    def __str__(self):
        return self.author.name

class PageLog(models.Model):
    user = models.ForeignKey(LikesFromUser)
    course = models.OneToOneField(Course)
    create = models.DateTimeField(default=datetime.datetime.now)