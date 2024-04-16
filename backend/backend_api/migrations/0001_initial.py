# Generated by Django 5.0.2 on 2024-04-15 14:04

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploading_user', models.CharField(max_length=100)),
                ('time_of_transfer', models.CharField(max_length=100)),
                ('cc_num', models.IntegerField()),
                ('merchant', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('amt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('city', models.CharField(max_length=100)),
                ('job', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('is_flagged', models.BooleanField(default=False)),
                ('anomalous', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StandardUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('cc_num', models.IntegerField(unique=True)),
                ('groups', models.ManyToManyField(related_name='standard_users_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='standard_users_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
