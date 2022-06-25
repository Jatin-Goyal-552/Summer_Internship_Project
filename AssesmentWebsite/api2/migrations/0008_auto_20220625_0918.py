# Generated by Django 3.2.5 on 2022-06-25 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api2', '0007_alter_expertise_last_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_time',
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('question_read_time', models.IntegerField(null=True)),
                ('code_read_time', models.IntegerField(null=True)),
                ('fcfid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api2.code')),
                ('ffevid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api2.evaluation')),
            ],
        ),
    ]
