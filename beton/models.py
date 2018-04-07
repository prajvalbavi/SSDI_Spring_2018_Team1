from django.contrib import admin
from django.db import models
from datetime import date

# Create your models here.
class Userinfo(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    emailID = models.CharField(max_length=30)
    def __str__(self):
        return self.username

class Topics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)
    creator_name = models.CharField(max_length=20)
    start_date = models.DateField("Date")
    end_date = models.DateField("Date")
    date_of_creation = models.DateField("Date", default=date.today)
    def __str__(self):
        return self.topic_name

class BetInfo(models.Model):
    bet_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topics, on_delete = models.SET(0))
    option = models.CharField(max_length=20, default = "Null")
    total_amount = models.IntegerField(default = 0)
    total_users = models.IntegerField(default = 0)
    def __str__(self):
        return str(self.bet_id)


admin.site.register(Userinfo)
admin.site.register(Topics)
admin.site.register(BetInfo)