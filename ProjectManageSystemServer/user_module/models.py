from django.db import models


# Create your models here.
# class user(models.Model):
#
class User(models.Model):
    HIGHSCHOOL = 'HS'
    BACHELORDEGREE = 'BD'
    MASTERDEGREE = 'MD'
    DOCTORALDEGREE = 'DD'
    ONLINE = 'OL'
    OFFLINE = 'OFL'
    BUSY = 'BY'
    WRITEOFF = 'WO'
    CLOAKING = 'CK'
    USER_EDUCATIONS = ((HIGHSCHOOL, 'Highschool'), (BACHELORDEGREE, 'Bachelordegree'), (MASTERDEGREE, 'Masterdegree'),
                       (DOCTORALDEGREE, 'Doctoraldegree'),)
    USER_STATUSES = ((OFFLINE, 'Offline'), (ONLINE, 'Online'), (BUSY, 'Busy'), (WRITEOFF, 'WO'), (CLOAKING, 'CK'),)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    name = models.CharField(blank=True, max_length=12)
    gender = models.BooleanField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    city = models.CharField(blank=True, max_length=16)
    education = models.PositiveSmallIntegerField(default=0, choices=USER_EDUCATIONS)
    duty = models.CharField(blank=True, max_length=16)
    contact = models.CharField(blank=True, max_length=16)
    description = models.CharField(blank=True, max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(default=0, choices=USER_STATUSES)
    is_deleted = models.BooleanField(default=False)


class Friend(models.Model):
    subject = models.ForeignKey(to='User', related_name='subject', on_delete=models.CASCADE)
    object = models.ForeignKey(to='User', related_name='object', on_delete=models.CASCADE)
    send_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)







