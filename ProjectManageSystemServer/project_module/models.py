from django.db import models

# Create your models here.
class Project(models.Model):
    # 项目类型都有哪些
    PROJECT_TYPES = ()
    name = models.CharField(max_length=16)
    type = models.PositiveSmallIntegerField(default=0, choices=PROJECT_TYPES)
    description = models.CharField(blank=True, max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Role(models.Model):
    name = models.CharField(max_length=8)
    description = models.CharField(blank=True, max_length=48)


class Participation(models.Model):
    user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE)
    join_time = models.DateTimeField(auto_now_add=True)


class ParticipationRole(models.Model):
    participation=models.ForeignKey(to='Participation', on_delete = models.CASCADE)
    role=models.ForeignKey(to='Role', on_delete = models.CASCADE)

class Notice(models.Model):
    title=models.CharField(max_length=32)
    content=models.CharField(blank=True, max_length=512)
    project=models.ForeignKey(to='Project', on_delete = models.CASCADE)
    create_time=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

class NoticeReceive(models.Model):
    user=models.ForeignKey(to='user_module.User', on_delete = models.CASCADE)
    notice=models.ForeignKey(to='Notice', on_delete = models.CASCADE)
    read_time=models.DateTimeField(null=True, blank=True)
