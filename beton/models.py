from django.contrib import admin
from django.db import models
from datetime import date


# Create your models here.
class Userinfo(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    emailID = models.CharField(max_length=30)
    balance = models.IntegerField(default=0)
    def __str__(self):
        return self.username


class Topics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)
    creator_name = models.ForeignKey(Userinfo, on_delete = models.SET(0))
    start_date = models.DateField("Date")
    end_date = models.DateField("Date")
    date_of_creation = models.DateField("Date", default=date.today)
    winning_option = models.CharField(max_length=100, default="not declared")
    def __str__(self):
        return self.topic_name


class BetInfo(models.Model):
    bet_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topics, on_delete = models.SET(0))
    option = models.CharField(max_length=20, default = "Null")
    total_amount = models.IntegerField(default = 0)
    total_users = models.IntegerField(default = 0)
    def __str__(self):
        return str(self.topic_id) + str(self.option)


class Bets(models.Model):
    bet_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topics, on_delete = models.SET(0))
    username = models.ForeignKey(Userinfo, on_delete = models.SET(0))
    option = models.CharField(max_length=20, default = "Null")
    amount = models.IntegerField(default = 0)
    date_of_placing_bet = models.DateField("Date", default=date.today)

    def __str__(self):
        return str(self.username) + ':' + str(self.topic_id) + '-' + str(self.option)


class BetOnAdmins(models.Model):
    admin_identity = models.CharField(primary_key= True, max_length= 40)
    secret_key = models.CharField(max_length=20, null=False)
    login_time = models.DateTimeField("login", null= True)
    last_active_time = models.DateTimeField("lastactive", null= True)
    password = models.CharField(max_length=20)

class ClosedBets(models.Model):
    bet_id = models.IntegerField(primary_key=True)
    topic_id = models.IntegerField(default = 0)
    username = models.CharField(max_length=20)
    option = models.CharField(max_length=20, default = "Null")
    amount = models.IntegerField(default = 0)
    date_of_placing_bet = models.DateField("Date", default=date.today)
    win = models.IntegerField(default = 0)
    win_lose_amount = models.FloatField(default = 0.0)

    def __str__(self):
        return str(self.username) + ':' + str(self.topic_id) + '-' + str(self.option)

class ClosedTopics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)
    creator_name = models.CharField(max_length=20)
    start_date = models.DateField("Date")
    end_date = models.DateField("Date")
    date_of_creation = models.DateField("Date", default=date.today)
    winning_option = models.CharField(max_length=100, default="not declared")
    total_amount = models.IntegerField(default = 0)
    winning_amount = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    def __str__(self):
        return self.topic_name

admin.site.register(Userinfo)
admin.site.register(Topics)
admin.site.register(BetInfo)
admin.site.register(Bets)
admin.site.register(BetOnAdmins)
admin.site.register(ClosedBets)
admin.site.register(ClosedTopics)


