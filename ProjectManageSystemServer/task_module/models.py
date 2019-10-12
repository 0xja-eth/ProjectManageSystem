from django.db import models


# Create your models here.
class Task(models.Model):
    BEGIN = 'BE'
    FINISH = 'FI'
    PAUSE = 'PA'
    RUNNING = 'RU'
    ONE = 'ONE'
    TWO = 'TWO'
    THREE = 'THR'
    TASK_STATUSES = ((BEGIN, 'BE'), (FINISH, 'FI'), (PAUSE, 'PA'), (RUNNING, 'RU'),)
    TASK_LEVELS = ((ONE, 'ONE'), (TWO, 'TWO'), (THREE, 'THR'),)
    name = models.CharField(max_length=24)
    description = models.CharField(blank=True, max_length=128)
    project = models.ForeignKey(to='project_module.Project', on_delete=models.CASCADE)
    parent = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=0, choices=TASK_STATUSES)
    level = models.PositiveSmallIntegerField(default=0, choices=TASK_LEVELS)
    progress = models.PositiveSmallIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)



class PrevTask(models.Model):
    task = models.ForeignKey(to='Task', related_name='currtask', on_delete=models.CASCADE)
    prev = models.ForeignKey(to='Task', related_name='prevtask', on_delete=models.CASCADE)


class TaskTake(models.Model):
    user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
    task = models.ForeignKey(to='Task', on_delete=models.CASCADE)


class TaskProgress(models.Model):
    user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
    task = models.ForeignKey(to='Task', on_delete=models.CASCADE)
    progress = models.SmallIntegerField(default=0)
    description = models.CharField(blank=True, max_length=128)
    result = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    result_time = models.DateTimeField(null=True, blank=True)
