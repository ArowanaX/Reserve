# Generated by Django 4.0.4 on 2022-05-01 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Supplier', '0001_initial'),
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now_add=True)),
                ('date_in', models.DateField()),
                ('date_out', models.DateField()),
                ('person_num', models.IntegerField()),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ReserveRoom', to='Supplier.service')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ReserveUser', to='Customer.user')),
            ],
        ),
    ]
