# Generated by Django 3.2.5 on 2022-06-03 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_alter_expertise_fuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('qbid', models.AutoField(primary_key=True, serialize=False)),
                ('admin_programming_language', models.CharField(choices=[('1', 'Python'), ('2', 'C++'), ('3', 'Java')], max_length=100)),
                ('level', models.CharField(choices=[('1', 'Beginner'), ('2', 'Intermediate'), ('3', 'Expert')], max_length=100)),
                ('aid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]