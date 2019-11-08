# Generated by Django 2.2.7 on 2019-11-08 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20191103_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='comment',
        ),
        migrations.AddField(
            model_name='project',
            name='branch',
            field=models.CharField(choices=[('CS', 'Computer Science'), ('IS', 'Information Science'), ('EC', 'Electronics'), ('CIVIL', 'Civil'), ('MECH', 'mechanical'), ('EEE', 'eee'), ('IE', 'ie')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='field_name',
            field=models.FileField(max_length=1000, null=True, upload_to='home/pfiles'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Project')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Student')),
            ],
        ),
    ]
