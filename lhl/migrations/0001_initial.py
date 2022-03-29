# Generated by Django 4.0.3 on 2022-03-29 17:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=8)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=20)),
                ('pay_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imgurl', models.CharField(max_length=2000)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lhl.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('imgurl', models.CharField(max_length=2000)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=8)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=8)),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhl.member')),
            ],
        ),
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('is_complete', models.BooleanField(default=False)),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhl.member')),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhl.properties')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=2000)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhl.member')),
                ('reservation_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lhl.reservations')),
            ],
        ),
    ]
