# Generated by Django 5.1.3 on 2024-11-27 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_designrequest_comment_alter_designrequest_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='designrequest',
            name='comment',
        ),
    ]