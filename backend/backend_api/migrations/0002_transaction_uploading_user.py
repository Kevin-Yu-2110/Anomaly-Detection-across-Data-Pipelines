# Generated by Django 5.0.2 on 2024-04-02 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='uploading_user',
            field=models.CharField(default='Alice839', max_length=100),
            preserve_default=False,
        ),
    ]
