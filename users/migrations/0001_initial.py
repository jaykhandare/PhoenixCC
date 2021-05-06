# Generated by Django 3.2 on 2021-05-06 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('pin_code', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=15)),
                ('managed_by', models.CharField(max_length=20)),
                ('date_of_registration', models.DateField(auto_now_add=True)),
                ('pan_number', models.CharField(max_length=11)),
                ('aadhar_number', models.CharField(max_length=20)),
                ('unique_code', models.CharField(default='NOT_ASSIGNED', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Personal_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('pin_code', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=15)),
                ('date_of_joining', models.DateField(auto_now_add=True)),
                ('position', models.CharField(max_length=15)),
                ('direct_manager', models.CharField(max_length=20)),
                ('email_verified', models.BooleanField()),
            ],
        ),
    ]
