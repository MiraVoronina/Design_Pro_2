# Generated by Django 5.1.3 on 2024-11-28 13:27

import accounts.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_designrequest_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='designrequest',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='designrequest',
            name='completed_image',
            field=models.ImageField(blank=True, null=True, upload_to='completed_requests/'),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='requests/', validators=[accounts.models.validate_image]),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='status',
            field=models.CharField(choices=[('new', 'Новая'), ('in_progress', 'Принято в работу'), ('completed', 'Выполнено')], default='new', max_length=20),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='design_requests', to='accounts.category'),
        ),
    ]