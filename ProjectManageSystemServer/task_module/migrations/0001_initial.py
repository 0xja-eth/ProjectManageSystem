# Generated by Django 2.2.5 on 2019-10-06 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_module', '0001_initial'),
        ('project_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[('BE', 'BE'), ('FI', 'FI'), ('PA', 'PA'), ('RU', 'RU')], default=0)),
                ('level', models.PositiveSmallIntegerField(choices=[('ONE', 'ONE'), ('TWO', 'TWO'), ('THR', 'THR')], default=0)),
                ('progress', models.PositiveSmallIntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='task_module.Task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_module.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_module.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_module.User')),
            ],
        ),
        migrations.CreateModel(
            name='TaskProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.SmallIntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('result', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('result_time', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_module.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_module.User')),
            ],
        ),
        migrations.CreateModel(
            name='PrevTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prevtask', to='task_module.Task')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currtask', to='task_module.Task')),
            ],
        ),
    ]
